def _():
    """
    This file defines settings to customise TRAC. 
    """
    pass

# CSV headers metadata
s_csv_headers = ["path", "num_states", "num_actions", "num_vars", "max_branching_factor", "num_participants", "num_transitions", "seed_num", "min_param_num", "average_param_num", "max_param_num", "min_bf_num", "average_bf_num", "max_bf_num", "num_paths",  "verdict", "participants_time", "non_determinism_time", "a_consistency_time", "f_building_time", "building_time", "z3_running_time", "total", "is_time_out"]

# Time metrics for reporting
s_time_metrics = ['participants_time', 'non_determinism_time', 'a_consistency_time', 'z3_running_time']

# Labels for data repporting plots
s_labels = {
    'num_states' : "Number of states",  # Number of states in the DAFSM
    'average_bf_num' : "Average branching factor",  # Average branching factor of the DAFSM
    'num_transitions' : "Number of transitions",  # Number of transitions in the DAFSM
    'num_paths': "Number of paths",  # Number of paths in the DAFSM
    'participants_time': "Caller check time",  # Time taken for caller check
    'non_determinism_time': "Non det formula build time",  # Time taken for non-determinism formula build
    'a_consistency_time' : "Consistency build time",  # Time taken for consistency build
    'z3_running_time' : "Z3 running time",  # Time taken for Z3 running
    'f_building_time' : "Time to build formulae"  # Time taken to build formulae
}

# Message indicating a well-formed DAFSM
s_well_formed_message = "(!) Verdict: Well Formed"

# Message indicating a non well-formed DAFSM
s_non_well_formed_message = "(!) Verdict: Non Well Formed"

# Paths for file handling
s_z3model_path = "./Z3_models/"  # Path to store Z3 model files
s_txt_path = "./Examples/dafsm_txt/"  # Path to locate DAFSM text files
s_json_path = "./Examples/jsons/"  # Path to store generated JSON files

# Default settings for processing
s_non_stop = 1  # Flag to continue processing on errors
s_time_out = 300000000000  # Timeout limit for processing

# Default parameters for global randomizer. If set to None then they will be randomly generated
s_num_tests = None  # Number of tests to be generated
s_num_states = None  # Number of states in the DAFSM
s_num_actions = None  # Number of actions in the DAFSM
s_num_vars = None  # Number of variables in the DAFSM
s_max_num_transitions = None  # Maximum number of transitions in the DAFSM
s_max_branching_factor = None  # Maximum branching factor in the DAFSM
s_num_participants = None  # Number of participants in the DAFSM
s_incremental_gen = None  # Flag for incremental generation
s_merge_only_csv = None  # Flag to merge only CSV results
s_steps = None  # Steps for processing

# Default values for various parameters
s_number_per_bacth = 5  # Number per batch
s_steps = 5  # Steps for processing
s_number_runs_per_each = 10  # Number of runs per example
s_max_branching_factor = 5  # Maximum branching factor
s_num_example_for_each = 5  # Number of examples for each configuration
s_number_test_per_cpu = 5  # Number of model to alocate per CPU
