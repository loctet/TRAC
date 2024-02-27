import copy
from collections import defaultdict
import hashlib
from PatternChecker import *
from Extension import replace_assertion
from SafeVariableAssignment import SafeVariableAssignment as SafeVars
from VariableDeclarationConverter import VariableDeclarationConverter as VarDefConv
from FSMGraph import FSMGraph
from MiniTimer import *
  
  
class TransitionProcessor(MiniTimer):
    def __init__(self, data, log = True, non_stop = True, time_out = 0):
        self.str_code = ""
        self.solvers = {}
        self.deploy_init_var_val = {}
        self.var_names = {}
        self.solvers['start'] = []
        self.solvers['starts'] = [] 
        self.fsmGraph = FSMGraph(data, log, time_out)
        self.non_stop = non_stop
        self.log = log
        self.infos = {}
        self.non_det_formula = {}
        self.time_out = time_out
        
    #Append to the global Code Model
    def append(self, str):
       self.str_code += str + "\n"
       
    def quantifier_closure(self, formula, variables = [], quantifier = "ForAll"):
        return f"{quantifier}([{','.join(variables)}], {formula})" if len(variables) > 0 else formula
    
    
    def get_vars_names_from_input(self, input_c):
        resuls  = VarDefConv.convert_to_z3_declarations(input_c)
        return resuls[2]
    
    def add_old_var_from_precs_and_inputs(self, otherPrecs, inputs): 
        for i in range(len(otherPrecs)):
            try:
                inputs[i] = ";".join([ item for item in inputs[i].split(";") if item.strip() != ""] + [ f"{self.var_names[item.replace('_old', '')]} {item}"  for item in PatternChecker.get_all_old_variables(otherPrecs[i])])
            except Exception as e:
                print(f"KeyError: {e}")
                exit()
        return inputs

    # AConsistencyCheck formula gen
    def get_a_consistency_formula(self, preC, _postC_A, otherPrecs, inputs):
        hypothesis = f"And({preC},{_postC_A})"
        thesis = f'Or({",".join([self.quantifier_closure(otherPrecs[i], self.get_vars_names_from_input(inputs[1][i]), "Exists") for i in range(len(otherPrecs))])})' if len(otherPrecs) > 0 else "True"
    
        return f'Not(Implies({hypothesis}, {thesis}))'
    
    #NDetCheck formula gen
    def get_formula_for_determinism_at_stage(self, curent_transition, other_transitions, processed_data):
        other_precs, inputs = processed_data
        to_state = curent_transition['to']

        if to_state in self.non_det_formula :
            return self.non_det_formula[to_state]
        
        indexes = defaultdict(list)
        actions = []

        # we group transitions by labels and participants
        for transition in other_transitions:
            caller = list(transition['caller'].keys())[0]  # Assuming there's a single caller for simplicity
            callerRoles = transition['caller'][caller]

            # remove all added participant from parameter
            transition['newParticipants'] = {key: value for key, value in transition['newParticipants'].items() if key not in transition['newParticipants_from_param']}
            if caller.strip() == "":
                actions.append(transition['actionLabel'])
            elif len(transition['newParticipants'].keys()) == 0 :
                if len(callerRoles) != 0 :
                    actions.append(hashlib.md5(f"{transition['actionLabel']}_{callerRoles[:]}".encode()).hexdigest())
                else :
                    actions.append(transition['actionLabel'])
            else:
                actions.append(hashlib.md5(f"{transition['actionLabel']}".encode()).hexdigest())

        for i, action in enumerate(actions):
            indexes[action].append(i)

        result = []

        # for each groups we build the formula
        for action, indices in indexes.items():
            if len(indices) == 1:
                continue

            for i, index in enumerate(indices):
                grouped = copy.deepcopy(indices)
                hypothesis = other_precs[index]
                grouped.pop(i)
                var_in = self.get_vars_names_from_input(inputs[index])
                implication_part = f'And(Not({") , Not(".join([other_precs[j] for j in grouped])}))'
                result.append(f"Not(Implies({hypothesis}, {implication_part}))")

        self.non_det_formula[to_state] = f'Or({",".join(result)})' if result else "Not(True)"
        return self.non_det_formula[to_state]

    def should_stop(self, formula, transition, participant):
        if formula == "False":
            print(f"Error from this transitions:{transition['from']}_{transition['actionLabel']}({transition['input']})_{transition['to']}")
            print(f"Participant: {participant} not introduced")
            if self.non_stop:
                return True
            else: 
                exit()
    
   
    def process(self, transition, outgoingTransitions):
        # Initialize necessary variables from the current transition and collect inputs and preconditions from all outgoing transitions.
        preC = transition['preCondition']
        action = transition['actionLabel']
        otherPrecs = [item['preCondition'] for item in outgoingTransitions]
        inputs = [transition["input"], [item['input'] for item in outgoingTransitions]]
        postC = transition['postCondition']
        
        # Start timing for performance metrics.
        self.start_time()
        
        # Perform a check to ensure the caller of the transition is allowed, #CALLERCHECK
        formula_for_participant_check = self.fsmGraph.is_caller_introduced(transition)
        self.infos["participants"] = self.get_ellapsed_time()
        self.infos['nb_path'] = self.fsmGraph.nb_path
        self.infos["is_time_out"] = self.fsmGraph.timed_out
        # Decision point to potentially halt execution based on participant verification.
        self.should_stop(formula_for_participant_check, transition, transition["caller"])

        # Handling of special cases in pre and post conditions to ensure no outdated variables are used and to append '_old' to variables.
        PatternChecker.pre_condition_not_having_old_vars(preC, postC)
        postC = PatternChecker.append_old_to_vars_and_return_updated(postC, self.var_names)

        # Extracting and preparing post conditions for Z3 solver compatibility.
        _postC_A, _post_variable = PatternChecker.z3_post_condition(postC, self.var_names)

        # Update preconditions with "_old" versions of variables for state consistency.
        data = PatternChecker.replace_var_with_old_in_pre(preC, _post_variable, self.var_names)
        preC = data[0]

        # Update inputs to include "_old" versions of variables where applicable.
        inputs = (";".join(inputs[0].split(';') + data[1]), inputs[1])
        inputs = (
            self.add_old_var_from_precs_and_inputs([postC], [inputs[0]])[0],
            self.add_old_var_from_precs_and_inputs(otherPrecs, inputs[1])
        )

        # Initialize or retrieve solver data for the current action.
        data = self.solvers.get(action, [])
        if not data:
            self.solvers[action] = []

        # Replace assertions within preconditions to ensure correctness and safety.
        preC = replace_assertion(preC)
        otherPrecs = [replace_assertion(otherPrecs[i]) for i in range(len(otherPrecs))]

        # Generate variable assignments ensuring they are safe and declare global variables for use within the solver.
        _, global_vars = SafeVars.safe_variable_assignment(postC, f'solver__{action}_{len(self.solvers[action])}')

        # Convert variable declarations to Z3-compatible format.
        converted_declarations = VarDefConv.convert_to_z3_declarations(";".join([x for x in (inputs[1]+[inputs[0]]) if x != ""]))

        # Timing and checking for non-determinism within the transitions. # NDETCHECK
        self.start_time()
        thesis_non_eps = self.get_formula_for_determinism_at_stage(transition, outgoingTransitions, [otherPrecs, inputs[1]])
        self.infos["non_determinism"] = self.get_ellapsed_time()

        # Timing and checking for action consistency within the transitions.  # AConsistencyCheck
        self.start_time()
        sformula = self.get_a_consistency_formula(preC, _postC_A, otherPrecs, inputs)
        self.infos["a_consistency"] = self.get_ellapsed_time()

        # Generate a unique identifier for the function related to the current action and solver iteration.
        name_func = f'_{action}_{len(self.solvers[action])}'
        
        # Prepare the final result with all necessary information for the solver to process.
        result = {
            'sname': f'solver_{action}',
            'snameF': name_func,
            'sparams': "\n    ".join(converted_declarations[0].split('\n')),
            'spre': preC,
            'sglobalVars': global_vars,
            'sformula': sformula,
            'sparticipants': formula_for_participant_check,
            'epsformula': thesis_non_eps
        }
        # Append the result to the solvers dictionary for the current action, and update the latest processed transition.
        self.solvers[action].append(result)
        self.latest = result
