import csv
import os
import glob
import argparse
import concurrent.futures
import pandas as pd
from random import choice, randint, seed
from string import ascii_lowercase
from Random_exec import RandomTransitionsExecuter
from Settings import *
from Helpers import write_csv, run_parallel_generations

def generate_secure_seed() -> int:
    """
    Generates a secure seed for random number generation using os.urandom.

    :return: A securely generated seed that can be used for initializing a random number generator.
    :rtype: int
    """
    # Generate a seed using 8 bytes from os.urandom
    seed = int.from_bytes(os.urandom(8), 'big')
    return seed


def generate_random_type_variables(num_vars):
    """
    Generates a list of variables with random types, intended for use in transition generation.

    :param num_vars: The number of variables to generate. Each variable will have a randomly assigned type.
    :type num_vars: int
    :return: A list of tuples, each containing the type and name of a generated variable.
    :rtype: list
    """

    variables = []
    for _ in range(num_vars):
        var_type = choice(['int', 'int'])
        var_name = '_'.join(choice(ascii_lowercase) for _ in range(2))  # 1-2 character variable name
        variables.append((var_type, var_name))
    return variables

def generate_actions(max_actions):
    """
    Generates a list of unique action names, up to a specified maximum number.

    :param max_actions: The maximum number of unique action names to generate. The actual number of generated action names may be less than this maximum if the specified number exceeds the practical limit for unique names.
    :type max_actions: int
    :return: A list containing unique action names.
    :rtype: list
    """
    return ['a' + str(i) for i in range(1, min(max_actions, 20) + 1)]

def generate_parameters(max_params):
    """
    Generates a list of action parameters with random types, up to a specified maximum number.

    :param max_params: The maximum number of parameters to generate. The actual number of generated parameters may be less than this maximum.
    :type max_params: int
    :return: A list of tuples, each containing the type and name of a generated parameter.
    :rtype: list
    """
    params = []
    for i in range(randint(0 , max_params)):
        param_type = choice(['int', 'int'])
        param_name = '_' + ''.join(choice(ascii_lowercase) for _ in range(randint(1, 2)))  # Parameter name starts with "_"
        params.append((param_type, param_name))
    return params

def generate_z3_condition(variables, params, complexity):
    """
    Generates a Z3 solver condition string based on provided variables, parameters, and specified complexity.

    :param variables: A list of state variables available for generating the condition. Each element is a tuple containing the variable type and name.
    :type variables: list
    :param params: A list of parameters available for condition generation. Each element is a tuple containing the parameter type and name.
    :type params: list
    :param complexity: An integer indicating the complexity level of the generated condition. Higher values result in more complex conditions.
    :type complexity: int
    :return: A string representing the generated Z3 solver condition.
    :rtype: str
    """
    conditions = []
    all_vars = variables + params  # Combine state variables and parameters for precondition
    for i in range(randint(1, len(all_vars))):
        for _ in range(complexity):
            var_type, var_name = choice(all_vars)
            if var_type == 'bool':
                conditions.append(var_name if randint(0, 1) else f"Not({var_name})")
            elif var_type == 'int':
                conditions.append(f"{var_name} > {randint(0, 100)}")

    
    # Simplifying complexity handling
    if complexity == 1:
        return choice(conditions)
    elif complexity == 2:
        data = conditions[0:randint(2,len(conditions))]
        if data :
            joins = " , ".join(data)
            return f"And({joins})"
        else:
            return ""
    else:
        data = conditions[0:randint(3,len(conditions))]
        if data :
            joins = " , ".join(data)
            return f"And({joins})"
        else:
            return ""


def generate_a_transition(state_variables, params, participant, role, to_state, from_state, action):
    """
    Generates a textual representation of a transition based on the specified parameters.

    :param state_variables: A list of tuples representing the state variables involved in the transition, where each tuple contains the variable type and name.
    :type state_variables: list
    :param params: A list of tuples representing the parameters involved in the transition, where each tuple contains the parameter type and name.
    :type params: list
    :param participant: The name of the participant involved in the transition.
    :type participant: str
    :param role: The role of the participant in the transition.
    :type role: str
    :param to_state: The name of the destination state for the transition.
    :type to_state: str
    :param from_state: The name of the source state from which the transition occurs.
    :type from_state: str
    :param action: The name of the action associated with the transition.
    :type action: str
    :return: A textual representation of the generated transition.
    :rtype: str
    """
    params_declaration = ', '.join([f'{t} {n}' for t, n in params])
    complexity = randint(1, 3)
    pre_condition = generate_z3_condition(state_variables, params, complexity)
    post_conditions = []

    # Ensuring post conditions update state variables potentially with parameters, maintaining type consistency
    for var_type, var_name in state_variables:
        if var_type == 'int':
            if complexity == 1:
                post_conditions.append(f'{var_name} := {randint(0, 100)}')  # Example update, could be more complex
            elif complexity == 2:
                post_conditions.append(f"{var_name} := {randint(0, 100)} {f'+ {var_name}_old' if randint(0,1) == 0 else f'- {var_name}_old'}")  # Example update, could be more complex
            else:
                post_conditions.append(f"{var_name} := {randint(0, 100)} {f'+ {var_name}_old' if randint(0,1) == 0 else f'- {var_name}_old'} {f'+ {var_name}_old' if randint(0,1) == 0 else f'- {var_name}_old'}")  # Example update, could be more complex
            
        elif var_type == 'bool':
            if complexity == 1:
                post_conditions.append(f"{var_name} := {choice(['True', 'False'])}")
            else :
                post_conditions.append(f"{var_name} := {randint(0, 100)} {f'> {randint(0, 100)}' if randint(0,1) == 0 else f'< {randint(0, 100)}'}")  # Example update, could be more complex
            

    participantStr = ""
    randPart = randint(0, 10)
    if randPart == 1 :
        participantStr = f"any {participant}:{role}"
    elif randPart == 6 : 
        participantStr = f"{participant}:{role}"
    else:
        participantStr = f"{participant}"

    post_condition = ' & '.join(post_conditions)
    return f'{from_state} {{{pre_condition}}} {participantStr} > c.{action}({params_declaration}) {{{post_condition}}} {to_state}' + ("+" if randint(0, 10) == 2 else "")

def get_generated_stuffs(actions, states, participants, num_vars, roles):
    """
    Selects random elements from provided lists to construct a transition.

    :param actions: A list of available actions for transitions.
    :type actions: list
    :param states: A list of available states in the FSM.
    :type states: list
    :param participants: A list of available participants involved in the FSM.
    :type participants: list
    :param num_vars: The number of variables involved in transition conditions.
    :type num_vars: int
    :param roles: A list of available roles that participants can have.
    :type roles: list
    :return: A tuple containing randomly selected action, state, participant, parameters, and role for constructing a transition.
    :rtype: tuple
    """
    action = choice(actions)
    state = choice(states)
    participant = choice(participants)
    params = generate_parameters(num_vars)  # Generate random parameters for the action  
    return (action, state, participant, params, choice(roles))

def generate_transitions(num_states, num_actions, num_vars, max_branching_factor, num_participants, max_num_transitions):
    """
    Generates a list of textual transitions and associated statistical data based on specified parameters.

    :param num_states: The number of states in the FSM.
    :type num_states: int
    :param num_actions: The number of actions available for transitions.
    :type num_actions: int
    :param num_vars: The number of variables involved in the FSM.
    :type num_vars: int
    :param max_branching_factor: The maximum number of transitions from any given state.
    :type max_branching_factor: int
    :param num_participants: The number of participants involved in the FSM.
    :type num_participants: int
    :param max_num_transitions: The maximum number of transitions to be generated.
    :type max_num_transitions: int
    :return: A list containing the generated transitions and statistical data about the generation process.
    :rtype: list
    """

    seed_num = generate_secure_seed()
    seed(seed_num)  # Initialize the random number generator
    states = ['S' + str(i) for i in range(num_states)]
    actions = generate_actions(num_actions)
    state_variables = generate_random_type_variables(num_vars)
    transitions = []
    if num_participants <= 1 :
        participants = ["p1"]
        roles = ["R1"]
    else:
        participants = ['p' + str(i) for i in range(1, num_participants)]  # Example participants
        roles = ['R' + str(i) for i in range(1, num_participants)]  # Example role

    # Generate state variables declaration
    state_vars_declaration = '; '.join([f'{t} {n}' for t, n in state_variables])
    list_visited = set()
    list_not_visited = set()
    list_not_visited.add("S0")
    r_num_trans = 0
    max_bf_num = 1
    min_p_num = average_p_num = max_p_num = 0
    min_bf_num = 0
    for i in range(num_states-1):
        state = states[i]
        action, to_state, participant, params, role = get_generated_stuffs(actions, states, participants, num_vars, roles)
        from_state = states[i]
        to_state = states[i+1]
        list_visited.add(state)
        transitions.append(generate_a_transition(state_variables, params, participant, role, to_state, from_state, action))
    r_num_trans = num_states-1

    while r_num_trans <= max_num_transitions:
        from_state = list_not_visited.pop() if len(list_not_visited) > 0 else choice(states)
        list_visited.add(from_state)
        num_transitions = randint(1, max_branching_factor)
        min_bf_num = min(min_bf_num, num_transitions)
        max_bf_num = max(max_bf_num, num_transitions)
        r_num_trans += num_transitions

        for _ in range(num_transitions):
            action, to_state, participant, params, role= get_generated_stuffs(actions, states, participants, num_vars, roles)
            list_not_visited.add(to_state)
            num_params = len(params)
            min_p_num = min(min_p_num, num_params)
            max_p_num = max(max_p_num, num_params)
            average_p_num += num_params
            transitions.append(generate_a_transition(state_variables, params, participant, role, to_state, from_state, action))
    
    # Ensure deploy transition is generated last and includes all state variables declaration
    params_declaration =  ", " + (', '.join([f'{t} {n}' for t, n in params])) if params else ""
    deploy_transition = f'_ {{True}} {participants[0]}:{choice(role)} > starts(c{params_declaration}) {{}} {{{state_vars_declaration}}} {states[0]}'
    transitions.append(deploy_transition)
    return [transitions, num_states, seed_num, min_p_num, average_p_num / len(transitions), max_p_num, min_bf_num, len(transitions) / num_states, max_bf_num] 

def write_file(path, transitions):
    """
    Writes the generated transitions to a specified file.

    :param path: The file path where the transitions will be written.
    :type path: str
    :param transitions: A list of transitions to be written to the file.
    :type transitions: list
    """

    with open(path, 'w') as file:
        for transition in transitions:
            file.write(transition + "\n")
    print(f"Transitions have been written to {path}")
    

def genFile(directory, subdir_num, max_tests, num_states, num_actions, num_vars, max_branching_factor, num_participants, max_num_transitions):
    # make sure we create all needed sub dirs
    p_sud_dir = os.path.join("./examples/random_txt/",directory, str(subdir_num))
    os.makedirs(p_sud_dir, exist_ok=True)
    os.makedirs(os.path.join("./examples/random_json/",directory, str(subdir_num)), exist_ok=True)
    os.makedirs(os.path.join("./Z3_models/random_tests/",directory, str(subdir_num)), exist_ok=True) 
    paramsList = []
    for i in range(max_tests):
        path = os.path.join(p_sud_dir, f"test_gen_{i}.txt")
        transitions, g_num_states, seed_num, min_p_num, average_p_num, max_p_num, min_bf_num, average_bf_num, max_bf_num = generate_transitions(num_states, num_actions, num_vars, max_branching_factor, num_participants, max_num_transitions)
        transitions.insert(0,transitions.pop())
        paramsList.append([path, g_num_states, num_actions, num_vars, max_branching_factor, num_participants, len(transitions), seed_num, min_p_num, average_p_num, max_p_num, min_bf_num, average_bf_num, max_bf_num])
        write_file(path, transitions)

    write_csv(p_sud_dir+"/list_of_files_info.csv",  paramsList)
    return []

class RandomTransitionsGenerator:
    """
    Generates random transitions for FSM testing and stores them in files.
    
    Initialization parameters define the configuration for transition generation.
    """
    def __init__(self, num_tests, directory, num_states=None, num_actions=None, num_vars=None, max_branching_factor=None, num_participants=None, max_num_transitions = None, steps = s_steps, num_example_for_each = s_num_example_for_each):
        """
        Generates random transitions for Finite State Machine (FSM) testing and stores them in files.

        :param num_tests: The number of tests to generate.
        :type num_tests: int
        :param directory: The directory where the generated transitions will be stored.
        :type directory: str
        :param num_states: (Optional) The number of states in the FSM. Defaults to None.
        :type num_states: int or None
        :param num_actions: (Optional) The number of actions in the FSM. Defaults to None.
        :type num_actions: int or None
        :param num_vars: (Optional) The number of variables in the FSM. Defaults to None.
        :type num_vars: int or None
        :param max_branching_factor: (Optional) The maximum branching factor for transitions. Defaults to None.
        :type max_branching_factor: int or None
        :param num_participants: (Optional) The number of participants in the FSM. Defaults to None.
        :type num_participants: int or None
        :param max_num_transitions: (Optional) The maximum number of transitions. Defaults to None.
        :type max_num_transitions: int or None
        :param steps: (Optional) Steps for transition generation. Defaults to s_steps.
        :type steps: unknown_type or None
        :param num_example_for_each: (Optional) Number of examples for each step. Defaults to s_num_example_for_each.
        :type num_example_for_each: unknown_type or None

        :returns: None
        :rtype: NoneType
        """

        self.num_tests = num_tests if num_tests is not None else 1000
        self.directory = directory
        self.base_dir =  os.path.join('./examples/random_txt/', self.directory)
        self.num_states = num_states
        self.num_actions = num_actions
        self.num_vars = num_vars
        self.max_branching_factor = max_branching_factor
        self.num_participants = num_participants
        self.max_num_transitions = max_num_transitions
        self.paramsList = []
        self.steps = steps 
        self.num_example_for_each = num_example_for_each

    def appendToWork(self, works, i, number_elt):
        """
        Appends work items to the list for parallel execution.
        """
        # Select parameters randomly if not provided
        num_states = randint(2, 100) if self.num_states is None else self.num_states
        num_actions = randint(10, 20) if self.num_actions is None else self.num_actions
        num_vars = randint(1, 50) if self.num_vars is None else self.num_vars
        max_branching_factor = randint(2, 20) if self.max_branching_factor is None else self.max_branching_factor
        num_participants = randint(2, 10) if self.num_participants is None else self.num_participants
        max_num_transitions = randint(num_states, num_states*3) if self.max_num_transitions is None else self.max_num_transitions

        if max_num_transitions < num_states:
            max_num_transitions = randint(num_states, num_states*3)

        works.append([genFile, self.directory, i, number_elt, num_states, num_actions, num_vars, max_branching_factor, num_participants, max_num_transitions])
        return works
    
    
    def merge_and_delete(self):
        """
        Merges individual CSV files into one and cleans up the directory.
        """
                # Define the final CSV where the merged data will be stored
        merged_csv = os.path.join(self.base_dir, 'list_of_files_info.csv')

        if os.path.exists(merged_csv):
            os.remove(merged_csv)

        csv_files = glob.glob(os.path.join(self.base_dir, '**/*.csv'), recursive=True)        
        # Read and concatenate all CSV files into one DataFrame
        df = pd.concat((pd.read_csv(f) for f in csv_files))

        df.to_csv(merged_csv, index=False)


    # Running mode where we need to set parameters from command line
    def run(self):
        """
        Executes the transition generation process.
        """
        works = []
        number_elt = self.num_example_for_each
        for i in range(self.num_tests // number_elt):
            works = self.appendToWork(works, i + 1, number_elt)
        
        if self.num_tests % number_elt != 0 :
            works = self.appendToWork(works, self.num_tests // number_elt + 1, self.num_tests % number_elt)

        run_parallel_generations(works)

    # Running mode where fixed param
    def run2(self):
        """
        An alternative execution mode for generating transitions.
        """
        works = []
        number_elt = self.num_example_for_each
        for s in range(10, self.num_tests, 10): # stages eancreases
            for t in range(s, 3*s, self.steps): # stages eancreases
                self.num_states = s 
                self.max_num_transitions = t
                works = self.appendToWork(works, f"{s}_{t}", number_elt)
            
        run_parallel_generations(works) 

    


def main():
    """
    Main function to parse command-line arguments and trigger transition generation.
    """
    parser = argparse.ArgumentParser(description='Generate Random Transitions and Store Them in Files')
    parser.add_argument('--directory', type=str, required=True, help='Directory to store the test files')
    parser.add_argument('--num_tests', default= s_num_tests, type=int, help='Number of tests to generate')
    parser.add_argument('--num_states', default= s_num_states, type=int, help='Number of states (optional)')
    parser.add_argument('--num_actions', default= s_num_actions, type=int, help='Number of actions (optional)')
    parser.add_argument('--num_vars', default= s_num_vars, type=int, help='Number of variables (optional)')
    parser.add_argument('--max_num_transitions', default= s_max_num_transitions, type=int, help='Maximum number of transitions (optional)')
    parser.add_argument('--max_branching_factor', default= s_max_branching_factor, type=int, help='Maximum number of outgoing transitions (optional)')
    parser.add_argument('--num_participants', default= s_num_participants, type=int, help='Number of participants (optional)')
    parser.add_argument('--incremental_gen', default= s_incremental_gen, type=bool, help='Generate many examples gradually (optional)')
    parser.add_argument('--merge_only_csv', default= s_merge_only_csv, type=bool, help='Generate many examples gradually (optional)')
    parser.add_argument('--steps', default= s_steps, type=int, help='Generate many examples gradually (optional)')
    parser.add_argument('--num_example_for_each', default= s_num_example_for_each, type=int, help='Generate many examples gradually (optional)')
    
    args = parser.parse_args()

    generator = RandomTransitionsGenerator(
            num_tests=args.num_tests,
            directory=args.directory,
            num_states=args.num_states,
            num_actions=args.num_actions,
            num_vars=args.num_vars,
            max_branching_factor=args.max_branching_factor,
            num_participants=args.num_participants,
            max_num_transitions=args.max_num_transitions,
            steps = args.steps,
            num_example_for_each = args.num_example_for_each
        )

    #just merge all genereated csvs into one but keep those in sub directory
    if args.merge_only_csv :
        generator.merge_and_delete()
        print("Merge Done")
        exit()
    
    if not args.incremental_gen:
        generator.run()
        generator.merge_and_delete() 
        print("\n Executing Examples")
        rExec = RandomTransitionsExecuter(args.directory)
        rExec.process_all_txt_files()
        rExec.merge_and_delete()
    else:
        generator.run2()
        generator.merge_and_delete() 
        print("\n Executing Examples")
        rExec = RandomTransitionsExecuter(args.directory)
        rExec.process_all_txt_files()
        rExec.merge_and_delete()

if __name__ == "__main__":
    main()
