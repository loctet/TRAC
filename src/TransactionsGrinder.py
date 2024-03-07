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
    """
    Processes transactions from a JSON file to generate Z3 models, handling pre-processing,
    grouping transactions, and executing Z3 models for verification.

    Inherits from Logger for logging capabilities.
    """
    def __init__(self, 
                 file_name, 
                 z3model_path = s_z3model_path, 
                 txt_path = s_txt_path, 
                 json_path = s_json_path, 
                 log = True, 
                 logTime = False, non_stop = True, time_out = 0) -> None:
        """
        Initializes the TransactionsGrinder with file paths and logging settings.

        :param file_name: The name of the file to process.
        :type file_name: str
        :param z3model_path: Path to save the generated Z3 model files.
        :type z3model_path: str
        :param txt_path: Path to save text outputs.
        :type txt_path: str
        :param json_path: Path to JSON input files.
        :type json_path: str
        :param log: Enables logging if True.
        :type log: bool
        :param logTime: Enables timing logging if True.
        :type logTime: bool
        :param non_stop: Continues processing on errors if True.
        :type non_stop: bool
        :param time_out: Timeout limit for processing.
        :type time_out: int
        """

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
        os.makedirs(txt_path+"/images", exist_ok=True)
        os.makedirs(json_path, exist_ok=True)
        os.makedirs(z3model_path, exist_ok=True)
        
    def set_fsm_data(self, fsm):
        """
        Sets the finite state machine data for processing.

        :param fsm: The finite state machine data as a dictionary.
        :type fsm: dict
        """

        self.fsm = fsm

    def pre_process_fsm(self):
        """
        Pre-processes the DAFSM by converting variable declarations to Z3 declarations
        and updating transitions with new participants.
        """
        for key in range(len(self.fsm['transitions'])):
            results = VariableDeclarationConverter.convert_to_z3_declarations(self.fsm['transitions'][key]['input'], [], {}, False)
            self.fsm['transitions'][key]['newParticipants'].update(results[3])
            self.fsm['transitions'][key]['newParticipants_from_param'] = results[3] 
            
    def get_full_json_path(self):
        """
        Constructs the full path to the JSON file based on the base JSON path and file name.

        :return: The full path to the JSON file.
        :rtype: str
        """
        return os.path.join(self.json_path, f"{self.file_name}.json")
    
    def get_full_png_path(self):
        """
        Constructs the full path to the PNG file based on the base Txt path and file name.

        :return: The full path to the PNG file.
        :rtype: str
        """
        return os.path.join(self.txt_path,"images", f"{self.file_name}.png")
    
    def get_full_txt_path(self):
        """
        Constructs the full path to the TXT file based on the base TXT path and file name.

        :return: The full path to the TXT file.
        :rtype: str
        """
        return os.path.join(self.txt_path, f"{self.file_name}.txt")
    
    def get_full_z3model_path(self, check = "_formness"):
        """
        Constructs the full path to the Z3 model file based on the base Z3 model path, file name,
        and an optional suffix for the file name.

        :param check: Optional suffix for the Z3 model file name.
        :type check: str
        :return: The full path to the Z3 model file.
        :rtype: str
        """

        return os.path.join(self.z3model_path, f"{self.file_name}{check}.py")
    
    def group_transactions(self, transitions):
        """
        Groups transactions by their "to" state for processing.

        :param transitions: A list of transactions to group.
        :type transitions: list
        :return: A dictionary of transactions grouped by "to" state.
        :rtype: dict
        """

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
        """
        Loads DAFSM data from a JSON file specified by the constructed full JSON path.

        :return: The content of the JSON file as a list of strings.
        :rtype: list
        """

        with open(self.get_full_json_path(), 'r') as file:
            input_text = file.readlines()
        self.fsm = json.loads(''.join(input_text))
        return input_text

    def get_grouped_transaction(self, transitions):
        """
        Groups transactions and creates a copy for processing.

        :param transitions: A list of transactions to group.
        :type transitions: list
        :return: A tuple containing the grouped transactions and a copy of them.
        :rtype: tuple
        """

        grouped_transitions = self.group_transactions(transitions)
        grouped_transitions_copy = grouped_transitions.copy()
        return [grouped_transitions, grouped_transitions_copy ]   

    def get_transition_processor(self)->TransitionProcessor:
        """
        Gets or creates a TransitionProcessor instance for processing DAFSM transitions.

        :return: An instance of TransitionProcessor.
        :rtype: TransitionProcessor
        """

        if self.transition_processor is None:
            self.transition_processor = TransitionProcessor(self.fsm, self.log, self.non_stop, self.time_out)
    
        return self.transition_processor
    
    def update_data(self, data):
        """
        Updates processing information with data from the transition processor.

        :param data: Data to update the processing information with.
        """

        self.info["t_participants"] += self.transition_processor.infos["participants"] 
        self.info["t_non_determinism"] += self.transition_processor.infos["non_determinism"] 
        self.info["t_a_consistency"] += self.transition_processor.infos["a_consistency"] 
        self.info["t_building"] += self.get_time() - data[0]
        self.info["nb_path"] += self.transition_processor.infos["nb_path"] 
        self.info["is_time_out"] = self.transition_processor.infos["is_time_out"]
    
    def tr_grinding(self, run = True):
        """
        Main method for processing transactions, building Z3 model files, and optionally running Z3 verification.

        :param run: If True, runs Z3 verification after processing.
        :type run: bool
        """

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
                    self.update_data([0])
                    if not self.non_stop and (self.should_stop_if_time_out(self) or self.should_stop(self.get_full_z3model_path(), transition, self)):  
                        return
                    
                    if transition['to'] not in grouped_transitions and transition['to'] not in fsm['finalStates']:
                        self.logIt(f"Warning: {transition['to']} is not a final state but has no trasitions from {transition['to']}")
                
                _, data = grouped_transitions_copy.popitem() if len(grouped_transitions_copy) > 0 else ["", []]

            if run and self.non_stop:
                self.log = log
                s_t = self.get_time()
                Fbuilder.build_z3_formulas_model_and_save(self, self.get_full_z3model_path(), False)
                self.info["t_building"] += self.get_time() - s_t
                Z3Runner.execute_model(self,self.get_full_z3model_path())
            if not self.non_stop: 
                print("(!) Verdict: Well Formed\n")
            
            self.logIt("End----\n\n")
        except Exception as e:  
            traceback.print_exc()
            raise Exception(f"Error while grinding: {e}")


    def check_independant_sat(self):
        """
        Checks the independent satisfiability of the model by verifying each transaction separately.
        """
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
        """
        Checks path satisfiability of the model by verifying the satisfiability of different paths through the DAFSM.
        """
        fsm = self.fsm 
        self.logIt("Checking Path statisfiability of the model----\n\n")
        PathGenerator.check_path_satisfiability(fsm, self.file_name)

        self.logIt("End----\n\n")
