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

    def get_a_consistency_formula(self, pre, _postC_A, otherPrecs, inputs):
        hypothesis = f"And({pre},{_postC_A})"
        thesis = f'Or({",".join([self.quantifier_closure(otherPrecs[i], self.get_vars_names_from_input(inputs[1][i]), "Exists") for i in range(len(otherPrecs))])})' if len(otherPrecs) > 0 else "True"
        sformula = f'Not(Implies({hypothesis}, {thesis}))'
        
        return sformula
    
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
    
    """
    Add an assertion to the solvers data structure based on provided conditions and inputs.

    Parameters:
    - current transition
    - list of out going transitions

    Returns:
    dict: A dictionary containing information about the added assertion.

    The function processes the given conditions and inputs, replaces variables with "_old" versions, and generates Z3-compatible formulas for the assertion. It also handles the addition of the assertion to the solvers data structure.

    """
    def process(self, transition, outgoingTransitions):
        # Select the first action (currect transition's action)
        preC = transition['preCondition']
        action = transition['actionLabel']
        otherPrecs = [item['preCondition'] for item in outgoingTransitions]
        inputs = [transition["input"], [item['input'] for item in outgoingTransitions]]
        postC = transition['postCondition']
        
        self.start_time()
        formula_for_participant_check = self.fsmGraph.is_caller_introduced(transition)
        self.infos["participants"] = self.get_ellapsed_time()
        self.infos['nb_path'] = self.fsmGraph.nb_path
        self.infos["is_time_out"] = self.fsmGraph.timed_out
        self.should_stop(formula_for_participant_check, transition, transition["caller"])

        # Check and handle special cases in the pre and post conditions
        PatternChecker.pre_condition_not_having_old_vars(preC, postC)

        postC = PatternChecker.append_old_to_vars_and_return_updated(postC, self.var_names)

        # Extract Z3-compatible post conditions
        _postC_A, _post_variable = PatternChecker.z3_post_condition(postC, self.var_names)


        # Replace variables in pre with their "_old" versions
        data = PatternChecker.replace_var_with_old_in_pre(preC, _post_variable, self.var_names)
        # change the precondition to the updatd one
        preC = data[0]

        # Update the inputs with the new "_old" variables
        inputs = (";".join(inputs[0].split(';') + data[1]), inputs[1])
        inputs = (
            self.add_old_var_from_precs_and_inputs([postC], [inputs[0]])[0],
            self.add_old_var_from_precs_and_inputs(otherPrecs, inputs[1])
        )

        # Initialize or get the data associated with the current action
        data = self.solvers.get(action, [])
        if not data:
            self.solvers[action] = []

        # Replace assertion in pre
        preC = replace_assertion(preC)
        otherPrecs = [ replace_assertion(otherPrecs[i]) for i in range(len(otherPrecs))]

        # Generate safe variable updates and global variables
        _ , global_vars = SafeVars.safe_variable_assignment(postC, f'solver__{action}_{len(self.solvers[action])}')

        # Convert variables and declarations to Z3 format
        converted_declarations = VarDefConv.convert_to_z3_declarations(";".join([x for x in (inputs[1]+[inputs[0]]) if x != ""]))

        self.start_time()
        thesis_non_eps = self.get_formula_for_determinism_at_stage(transition, outgoingTransitions, [otherPrecs, inputs[1]])
        self.infos["non_determinism"] = self.get_ellapsed_time()

        self.start_time()
        # Create the hypothesis and thesis for the assertion
        sformula = self.get_a_consistency_formula(preC, _postC_A, otherPrecs, inputs)
        self.infos["a_consistency"] = self.get_ellapsed_time()


        # Create a unique name for the function
        name_func = f'_{action}_{len(self.solvers[action])}'
        # Prepare the result 
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
        self.solvers[action].append(result)
        self.latest = result
        
        return result