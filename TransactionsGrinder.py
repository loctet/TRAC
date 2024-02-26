import json
import os
import traceback
from PathGenerator import PathGenerator
from TransitionProcessor import TransitionProcessor
from VariableDeclarationConverter import VariableDeclarationConverter 
from Logger import Logger
from Z3Runner import Z3Runner
from Fbuilder import Fbuilder
from Settings import s_json_path, s_txt_path, s_z3model_path

class TransactionsGrinder(Logger):
    def __init__(self, 
                 file_name, 
                 z3model_path = s_z3model_path, 
                 txt_path = s_txt_path, 
                 json_path = s_json_path, 
                 log = True, 
                 logTime = False, non_stop = True, time_out = 0) -> None:
        
        Logger.__init__(self, log, non_stop)
        if '/' in file_name or '\\' in file_name:
            path, file_name = os.path.split(file_name)
            txt_path = os.path.join(txt_path, path)
            json_path = os.path.join(json_path, path)
            z3model_path = os.path.join(z3model_path, path)

        self.z3model_path = z3model_path
        self.txt_path = txt_path
        self.json_path = json_path
        self.file_name = file_name
        self.log = log
        self.transition_processor = None
        self.non_stop = non_stop
        self.output = ""
        self.logTime = logTime
        self.time_out = time_out
        self.info = {
            "t_participants": 0,
            "t_non_determinism": 0,
            "t_a_consistency": 0,
            "t_building" : 0,
            "t_total": 0,
            "nb_path" : 0,
            "is_time_out": False
        }
        os.makedirs(txt_path, exist_ok=True)
        os.makedirs(json_path, exist_ok=True)
        os.makedirs(z3model_path, exist_ok=True)
        
    def set_fsm_data(self, fsm):
        self.fsm = fsm

    def pre_process_fsm(self):
        for key in range(len(self.fsm['transitions'])):
            results = VariableDeclarationConverter.convert_to_z3_declarations(self.fsm['transitions'][key]['input'], [], {}, False)
            self.fsm['transitions'][key]['newParticipants'].update(results[3])
            self.fsm['transitions'][key]['newParticipants_from_param'] = results[3] 
            
    def get_full_json_path(self):
        return os.path.join(self.json_path, f"{self.file_name}.json")
    
    def get_full_txt_path(self):
        return os.path.join(self.txt_path, f"{self.file_name}.txt")
    
    def get_full_z3model_path(self, check = "_formness"):
        return os.path.join(self.z3model_path, f"{self.file_name}{check}.py")
    
    def group_transactions(self, transitions):
        # Create a dictionary to store transitions grouped by "to" state
        transitions_by_to_state = {}
        # Group transitions by "to" state
        for transition in transitions:
            to_state = transition["from"]
            if to_state not in transitions_by_to_state:
                transitions_by_to_state[to_state] = []
            transitions_by_to_state[to_state].append(transition)
        return transitions_by_to_state

    def get_json_from_file(self):
        input_path = self.get_full_json_path()
        with open(input_path, 'r') as file:
            input_text = file.readlines()
        self.fsm = json.loads(''.join(input_text))
        return input_text

    def get_grouped_transaction(self, transitions):
        grouped_transitions = self.group_transactions(transitions)
        grouped_transitions_copy = grouped_transitions.copy()
        return [grouped_transitions, grouped_transitions_copy ]   

    def get_transition_processor(self)->TransitionProcessor:
        if self.transition_processor is None:
            self.transition_processor = TransitionProcessor(self.fsm, self.log, self.non_stop, self.time_out)
    
        return self.transition_processor
    
    def update_data(self, data):
        self.info["t_participants"] += self.transition_processor.infos["participants"] 
        self.info["t_non_determinism"] += self.transition_processor.infos["non_determinism"] 
        self.info["t_a_consistency"] += self.transition_processor.infos["a_consistency"] 
        self.info["t_building"] += self.get_time() - data[0]
        self.info["nb_path"] += self.transition_processor.infos["nb_path"] 
        self.info["is_time_out"] = self.transition_processor.infos["is_time_out"]
    
    def tr_grinding(self, run = True):
        try:
            self.start_time()
            fsm = self.fsm 
            transitions = fsm['transitions']
            # Example usage
            declarations_str = fsm['statesDeclaration']
            
            self.logIt("Checking the well formness of the model----\n")
            self.transition_processor = self.get_transition_processor()
            log = self.log
            if not self.non_stop:
                self.log = False

            result, deploy_init_var_val, var_names, _ = VariableDeclarationConverter.convert_to_z3_declarations(declarations_str, self.transition_processor.deploy_init_var_val, self.transition_processor.var_names, True)
            
            setattr(self.transition_processor, 'deploy_init_var_val', deploy_init_var_val)
            setattr(self.transition_processor, 'var_names', var_names)
            
            self.transition_processor.append(result)
            grouped_transitions, grouped_transitions_copy = self.get_grouped_transaction(transitions)
            data = grouped_transitions_copy.pop("_", [])

            while data:
                for transition in data:
                    outgoingTransitions = grouped_transitions.get(transition['to'], [])
                    self.transition_processor.process(transition, outgoingTransitions)
                    s_t = self.get_time()
                    Fbuilder.build_z3_formulas_model_and_save(self, self.get_full_z3model_path(), True)
                    self.update_data([s_t])
                    
                    if not self.non_stop and (self.should_stop_if_time_out(self) or self.should_stop(self.get_full_z3model_path(), transition, self)):  
                        return
                    
                    if transition['to'] not in grouped_transitions and transition['to'] not in fsm['finalStates']:
                        self.logIt(f"Warning: {transition['to']} is not a final state but has no trasitions from {transition['to']}")
                
                _, data = grouped_transitions_copy.popitem() if len(grouped_transitions_copy) > 0 else ["", []]

            if run and self.non_stop:
                self.log = log
                Fbuilder.build_z3_formulas_model_and_save(self, self.get_full_z3model_path(), False)
                Z3Runner.execute_model(self,self.get_full_z3model_path())
            if not self.non_stop: 
                print("(!) Verdict: Well Formed\n")
            
            self.logIt("End----\n\n")
        except Exception as e:  
            traceback.print_exc()
            raise Exception(f"Error while grinding: {e}")


    def check_independant_sat(self):
        try:
            fsm = self.fsm 
            transitions = fsm['transitions']
            # Example usage
            declarations_str = fsm['statesDeclaration']
            self.logIt("Checking independent statisfiability of the model----\n\n")
            self.transition_processor = self.get_transition_processor()
            result, deploy_init_var_val, var_names, _ = VariableDeclarationConverter.convert_to_z3_declarations(declarations_str, self.transition_processor.deploy_init_var_val, self.transition_processor.var_names)

            setattr(self.transition_processor, 'deploy_init_var_val', deploy_init_var_val)
            setattr(self.transition_processor, 'var_names', var_names)
            self.transition_processor.append(result)
            
            grouped_transitions, _ = self.get_grouped_transaction(transitions)
            
            for key in grouped_transitions:
                for transition in grouped_transitions[key]:
                    outgoingTransitions = grouped_transitions.get(transition['to'], [])
                    self.transition_processor.process(transition, outgoingTransitions)
                    self.update_data()
                    self.should_stop(transition)

                    if transition['to'] not in grouped_transitions and transition['to'] not in fsm['finalStates']:
                        self.logIt(f"Warning: {transition['to']} is not a final state but has no trasitions from {transition['to']}")
                        
            self.execute_model_and_save(f"{self.file_name}_indep_sat")
            self.logIt("End----\n\n")
        except Exception as e:  
            raise Exception(f"Error in check_independant_sat : {e}")

    def check_path_sat(self):
        fsm = self.fsm 
        self.logIt("Checking Path statisfiability of the model----\n\n")
        PathGenerator.check_path_satisfiability(fsm, self.file_name)

        self.logIt("End----\n\n")
