def _():
    """
    This file defines various settings and labels for reporting and analyzing the performance and characteristics of DAFSM. 
    It includes configurations for CSV headers to structure output data, time metrics to measure different phases of processing or verification, labels for more human-readable reporting, and default values for generating or testing DAFSMs. 
    Additionally, it specifies paths for model storage and example directories, along with parameters to control the generation and testing process, such as the number of tests, states, actions, variables, and the branching factor. 
    This setup is essential for systematic analysis, benchmarking, and documentation of DAFSM behaviors, performance, and verification outcomes.
    """
    pass

# CSV headers for data storage
s_csv_headers = ["path", "num_states", "num_actions", "num_vars", "max_branching_factor", "num_participants", "num_transitions", "seed_num", "min_param_num", "average_param_num", "max_param_num", "min_bf_num", "average_bf_num", "max_bf_num", "num_paths",  "verdict", "participants_time", "non_determinism_time", "a_consistency_time", "f_building_time", "building_time", "z3_running_time", "total", "is_time_out"]

# Time metrics for analysis
s_time_metrics = ['participants_time', 'non_determinism_time', 'a_consistency_time', 'z3_running_time']

# Labels for data analysis
s_labels = {
    'num_states' : "Number of states",
    'average_bf_num' : "Average branching factor",
    'num_transitions' : "Number of transitions",
    'num_paths': "Number of paths",
    'participants_time': "Caller check time",
    'non_determinism_time': "Non det formula build time",
    'a_consistency_time' : "Consistency build time",
    'z3_running_time' : "Z3 running time",
    'f_building_time' : "Time to build formulae"
}

# Message indicating a well-formed DAFSM
s_well_formed_message = "(!) Verdict: Well Formed"

# Paths for file handling
s_z3model_path = "./Z3_models/"
s_txt_path = "./Examples/dafsm_txt/"
s_json_path = "./Examples/jsons/"

# Default settings for processing
s_non_stop = 1
s_time_out = 300000000000

# Default parameters for global randomizer
s_num_tests = None
s_num_states = None
s_num_actions = None
s_num_vars = None
s_max_num_transitions = None
s_max_branching_factor = None
s_num_participants = None
s_incremental_gen = None
s_merge_only_csv = None
s_steps = None

# Default values for the random generator
s_number_per_bacth = 5
s_steps = 5
s_number_runs_per_each = 10
s_max_branching_factor = 5
s_num_example_for_each = 5
s_number_test_per_cpu = 5

