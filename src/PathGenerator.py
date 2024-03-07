import os
from Extension import replace_assertion
from SafeVariableAssignment import SafeVariableAssignment
from TransitionProcessor import TransitionProcessor
from VariableDeclarationConverter import VariableDeclarationConverter


class PathGenerator :
    """
    Generates and checks the satisfiability of paths within a DAFSM based on a given JSON representation of transitions.
    """

    @staticmethod
    def find_paths(graph, start, end, path=[]):
        """
        Recursively finds all paths from start to end node in a graph.

        :param graph: The graph represented as a dictionary.
        :type graph: dict
        :param start: The starting node.
        :param end: The ending node.
        :param path: The current path (used in recursive calls).
        :type path: list
        :return: A list of paths, where each path is a list of nodes.
        :rtype: list[list]
        """

        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]['to']:
            if node not in path:
                new_paths = PathGenerator.find_paths(graph, node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    @staticmethod
    def group_transactions(transition_json):
        """
        Groups transitions from the JSON representation of a DAFSM into paths from the initial to final states.

        :param transition_json: The JSON representation of the DAFSM's transitions.
        :type transition_json: dict
        :return: A dictionary where keys are string representations of paths and values are lists of transitions for each path.
        :rtype: dict
        """

        graph = {}
        for transition in transition_json['transitions']:
            from_state = transition['from']
            to_state = transition['to']
            if from_state not in graph:
                graph[from_state] = {'to': []}
            graph[from_state]['to'].append(to_state)

        initial_state = transition_json['transitions'][0]['from']
        final_states = transition_json['finalStates']

        grouped_transactions = {}
        for final_state in final_states:
            paths = PathGenerator.find_paths(graph, initial_state, final_state)
            for path in paths:
                path_str = ' -> '.join(path)
                formatted_transitions = []
                for i in range(len(path) - 1):
                    from_state = path[i]
                    to_state = path[i + 1]
                    transition = PathGenerator.find_transition(transition_json['transitions'], from_state, to_state)
                    #formatted_transition = PathGenerator.format_transition(transition)
                    formatted_transitions.append(transition)

                grouped_transactions[path_str] = formatted_transitions

        return grouped_transactions

    @staticmethod
    def find_transition(transitions, from_state, to_state):
        """
        Finds a transition between two states.

        :param transitions: A list of all transitions.
        :type transitions: list[dict]
        :param from_state: The starting state of the transition.
        :param to_state: The ending state of the transition.
        :return: The found transition or None if not found.
        :rtype: dict or None
        """

        for transition in transitions:
            if transition['from'] == from_state and transition['to'] == to_state:
                return transition
        return None

    @staticmethod
    def format_transition(transition):
        """
        Formats a single transition into a string representation.

        :param transition: The transition to format.
        :type transition: dict
        :return: The formatted string representing the transition.
        :rtype: str
        """

        pre_condition = transition['preCondition']
        input_params = transition['input']
        action_label = transition['actionLabel']
        post_condition = transition['postCondition']

        formatted_transition = f"{pre_condition}|{input_params}|{action_label} -> {post_condition}"
        return formatted_transition
    
    @staticmethod
    def check_path_satisfiability(fsm, file_name):
        """
        Checks the satisfiability of each path within the DAFSM and outputs the results to a Python file for execution.

        :param fsm: The finite state machine representation.
        :type fsm: dict
        :param file_name: The base name for the output file where Z3 code will be generated.
        :type file_name: str
        """

        file_name = f'./Z3_models/{file_name}'
        result = PathGenerator.group_transactions(fsm)
        for path, transitions in result.items():
            print(f"Path: {path}")
            temp = TransitionProcessor(fsm)
            result, deploy_init_var_val, var_names, participants = VariableDeclarationConverter.convert_to_z3_declarations(fsm['statesDeclaration'], temp.deploy_init_var_val, temp.var_names, True)
            setattr(temp, 'deploy_init_var_val', deploy_init_var_val)
            setattr(temp, 'var_names', var_names)
            temp.append(result)
            temp.append("solver = z3.Solver()\ncheck = True\nsolver.push()")
            
            for transition in transitions:
                pre = replace_assertion(transition['preCondition'])
                sVarUpdate, global_vars  = SafeVariableAssignment.safe_variable_assignment(transition['postCondition'], 'solver')
                sparams, init_var_val, var_names, participants = VariableDeclarationConverter.convert_to_z3_declarations(transition['input'], [])
                temp.append(f"{sparams}\n\n## {transition['actionLabel']}\n\nsolver.add({pre})\ncheck = check and solver.check() == z3.sat\nsolver.pop()\nsolver.push()\n{sVarUpdate}")
                
            temp.append("\nprint(f'=>{check}')\n\n")    
            temp.str_code = temp.str_code.replace("        ", "____").replace("    ",'').replace("____", "    ")
            # Specify the file name with a .py extension
            file_name = f"{file_name}_path.py"

            # Open the file for writing and write the code
            with open(file_name, "w") as file:
                file.write(f"from z3 import *\n# setting path\nsys.path.append('../') \nfrom Extension import *\n\n{temp.str_code}")
            #exec
            try:
                os.system(f'python {file_name}')
            except FileNotFoundError:
                print(f"Error: The file '{file_name}' does not exist.")
            
        print(f"\n(Check the generated file  {file_name}_path.py to fine the z3 code generated)\n") 
            