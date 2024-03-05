import json
import re

class The_Validator:
    """
    Validates and converts textual representations of transitions into a structured JSON format.
    This class specifically handles parsing of deploy and action transitions defined in a textual
    format and constructs a corresponding JSON object that represents the contract structure.
    """

    def __init__(self):
        """
        Initializes The_Validator with regex patterns for deploy and action transitions.
        """
        self.contract_id = ""
        self.initialStage = ""
        # Define the regex patterns for each type of transition
        # Define the regex pattern for the deploy transition
        self.deploy_pattern = re.compile(
            r'_(\s*){(.*)}\s+(\w+):(\w+)\s+>\s+starts\((\w+)(?:,\s*(.*))?\)\s*{(.*)}\s*{(.*)}\s+(\w+)(\+?)'
        )
        # Define the regex pattern for the other transitions
        self.action_pattern = re.compile(
            r'(\w+)\s*{(.*)}\s+(any\s+)?(\w*):?(\w*)\s+>\s+(\w+)\.(\w+)\((.*)\)\s*{(.*)}\s+(\w+)(\+?)'
        )

    def parse_transition(self, line):
        """
        Parses a single line of text representing a transition into a structured dictionary.

        :param line: A line of text representing a transition.
        :type line: str
        :return: A tuple containing a dictionary representation of the transition and an
                optional string of state variables declarations (if present).
        :rtype: tuple[dict, str]
        """

        
        # Check for deploy transition
        match = self.deploy_pattern.match(line)
        if match:
            _, pre_condition, participant, role, self.contract_id, params, post_condition, states_variables_declaration, to_stage, final_marker = match.groups()
            # Params are optional in the deploy transition
            params = params.strip() if params else ""
            self.initialStage = to_stage.rstrip('+')
            transition = {
                "from": "_",
                "to": self.initialStage,
                "initialStates": [self.initialStage],
                "finalStates": [self.initialStage] if final_marker else [],
                "newParticipants": {participant: role},
                "caller": {participant: []},
                "actionLabel": "starts",
                "preCondition": pre_condition,
                "postCondition": post_condition,
                "input": params,
                "externalAction": False
            }
            return transition, states_variables_declaration

        # Check for other types of transitions
        match = self.action_pattern.match(line)
        if match:
            from_stage, pre_condition, any_keyword, participant, role, contract_id, action, params, post_condition, to_stage, final_marker = match.groups()
            transition = {
                "from": from_stage,
                "to": to_stage.rstrip('+'),
                "initialStates": [],
                "finalStates": [to_stage.rstrip('+')] if final_marker else [],
                "newParticipants": {participant: role} if role and not any_keyword else {},
                "caller": {participant: [role] if any_keyword else []},
                "actionLabel": action,
                "preCondition": pre_condition,
                "postCondition": post_condition,
                "input": params,
                "externalAction": False
            }
            return transition, None

        return None, None

    # Main function to convert the transitions text to JSON format
    def transitions_to_json(self, transitions_txt_path, json_output_path):
        """
        Converts a text file containing transitions into a structured JSON format.

        :param transitions_txt_path: The file path for the text file containing transitions.
        :type transitions_txt_path: str
        :param json_output_path: The output file path for the resulting JSON.
        :type json_output_path: str

        This method reads transitions from a text file, parses them, and constructs a JSON
        object that represents the entire contract structure including transitions, states,
        and participants.
        """


        contract_structure = {
            "id": "",  
            "initialState": "",  # Update as necessary
            "statesDeclaration": "",
            "states": [],
            "finalStates": [],
            "transitions": [],
            "rPAssociation": []  # Update as necessary if associations are provided
        }

        # Read transitions from a text file and parse them
        with open(transitions_txt_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                transition, states_declaration = self.parse_transition(line.strip())
                if transition:
                    contract_structure['transitions'].append(transition)
                    if transition['from'] and transition['from'] != "_":
                        contract_structure['states'].append(transition['from'])
                    contract_structure['states'].append(transition['to'])
                    contract_structure['finalStates'].extend(transition['finalStates'])
                    if states_declaration:  # Only the deploy transition will have this
                        contract_structure['statesDeclaration'] = states_declaration

        # Remove duplicates and sort states and final states
        contract_structure['states'] = sorted(set(filter(None, contract_structure['states'])))
        contract_structure['finalStates'] = sorted(set(contract_structure['finalStates']))
        contract_structure['id'] = self.contract_id
       
        contract_structure['initialState'] = self.initialStage
        
        

        # Write the JSON structure to a file
        with open(json_output_path, 'w') as json_file:
            json.dump(contract_structure, json_file, indent=4)

