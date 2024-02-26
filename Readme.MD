# TRAC Tool README

## Introduction to TRAC

TRAC is a tool designed to enhance the development and verification of coodination protocols. It focuses on analyzing the well-formedness of DAFSMs, ensuring that only one transition within a group can be satisfied at a time. This tool is instrumental in identifying potential issues early in the development lifecycle, making it a valuable asset for developers and researchers aiming to validate the logical consistency within a protocol. TRAC's flexibility across different operating systems makes.

## Docker Installation and Running Instructions

To install and run TRAC using Docker:

1. Pull the Docker image:
   ```bash
   docker pull loctet/trac_dafsms:v1
   ```
2. Run the container:
   ```bash
   docker run -it loctet/trac_dafsms:v1
   ```
This command downloads the TRAC Docker image and starts a container with an interactive terminal. 

If Docker is not installed on your system, follow the official Docker installation instructions for Ubuntu at [Docker's official documentation](https://docs.docker.com/engine/install/ubuntu/). This guide provides a comprehensive step-by-step process to get Docker set up and running on your machine.

TRAC can also be cloned directly from its GitHub repository for those who prefer working with the source code. Visit [TRAC's GitHub page](https://github.com/loctet/TRAC) and follow the instructions in the README for setup and usage. This method is ideal for users looking for the latest version or interested in contributing to the project.

## Installation Instructions

Before installing TRAC, ensure Python 3.6 or later is installed on your system. TRAC relies on several Python packages for its operation. Use the following pip commands to install the necessary dependencies:

```bash
pip install z3-solver
pip install matplotlib
pip install numpy
pip install plotly
```
Also make sure the java JDK is installed to run the java command. This is used to hava a visual view of the DAFSMs

These commands install the Z3 SMT solver, Matplotlib for plotting, and NumPy for numerical computations, which are essential for TRAC's functionality. Ensure all commands are executed successfully to avoid any issues while running TRAC.

## Running a Predefined Example: "Simple Market Place"

To run the "simplemarket_place" example with TRAC:

1. **Prepare the Environment**: Ensure TRAC and its dependencies are installed as per the installation instructions.
2. **Navigate to the TRAC Directory**: Open a terminal and change directory to where `TRAC/src` is located.
3. **Locate the Example**: The `simplemarket_place` example is already within designated examples directory, typically named `Examples/dafsms_txt`. All manually executed examples should be kept in the folder `Examples` you can create subdirs, just be assured to give the exact path to the command `Main.py`.
4. **Execute the Example**:
   - Use `Main.py` to run the example. The command syntax is:
     ```bash
     python3 Main.py --filetype txt "azure/simplemarket_place"
     ```
   This command tells TRAC to process and verify the "simplemarket_place" example.

    Follow these steps to successfully run and analyze the "simplemarket_place" example, utilizing TRAC's verification capabilities.
    The result of this should be `(!) Verdict: Well Formed`
5. **Execute the Example**:
    Now that your firt example is completed you can design some DAFSMs and play around with the command by just changing the name of the file in the previous command 

The `Main.py`, can take some configurations as follows:

- `file_name`: Specifies the name of the file (JSON or TXT) to process, without its extension. This is the primary input for TRAC to analyze.
- `check_type`: Optional. Defines the type of check to perform on the input file. It can be one of four options:
  - `1` for Well-Formedness Check,
  - `2` for solate Function Check, // on progress
  - `3` for runing from Path Check, // On progress
  - `fsm` for printing the Finite State Machine (FSM). The default is `1`.
- `--filetype`: Optional. Indicates the type of the input file, either `json` or `txt`. The default is `json`.
- `--non_stop`: Optional. Determines the mode of checking, where `1` (default) continues checking even after errors are found, and `2` stops immediately when an error is detected.
- `--time_out`: Optional. Sets a timeout for the operation in seconds. The default is `0`, meaning no timeout.
This detailed explanation provides a comprehensive guide on how to utilize `Main.py` for different operations within the TRAC tool.

## Generating Examples
To generate DAFSM examples with `Generate_examples.py`, follow these steps:

1. **Navigate to TRAC Directory**: Ensure you're in the root directory of TRAC.
2. **Run Generate_examples.py**: Use the command below, adjusting parameters as needed.
   ```bash
   python3 Generate_examples.py --directory your_directory_name --num_tests 100
   ```
   Replace `your_directory_name` with the desired directory to store test files and adjust `--num_tests` to the number of examples you wish to generate.

3. **Parameters**:
    The parameters for `Generate_examples.py` enable customization of the DAFSM example generation process. If not specified, values for these parameters are generated randomly:

    - `--directory`: Specifies the directory to save generated examples.
    - `--num_tests`: The number of tests to generate.
    - `--num_states`: The number of states per test.
    - `--num_actions`: The number of actions.
    - `--num_vars`: The number of variables.
    - `--max_num_transitions`: The maximum number of transitions.
    - `--max_branching_factor`: The maximum branching factor.
    - `--num_participants`: The number of participants.
    - `--incremental_gen`: Enables incremental generation.
    - `--merge_only_csv`: Merges results into a single CSV without generating new tests.
    - `--steps`: The increment steps for generating tests.
    - `--num_example_for_each`: The number of examples to generate for each configuration.

4. **Output**: Examples are created in a subdirectory within `Examples/random_txt`. A CSV at the root of this directory contains metadata for each generated example, including paths, number of states, actions, variables, branching factors, and timings.

This process allows for the automated generation and analysis of DAFSM examples, facilitating comprehensive testing and verification of DAFSMs with TRAC.


## Running Sets of Examples

To execute multiple examples with `Random_exec.py`, the command format and parameters are as follows:
```bash
python3 Random_exec.py --directory <subdir> --merge_csv --add_path --number_test_per_cpu <num> --number_runs_per_each <runs> --time_out <nanoseconds>
```

- `--directory`: Specifies a subdirectory in `Examples/random_txt` where the examples and `list_of_files_info.csv` are located.
- `--merge_csv`: Merges individual CSV results into `merged_list_of_files_info.csv`.
- `--add_path`: Just count the number_path to each test in the CSV.
- `--number_test_per_cpu`: Determines how many tests are run in parallel per CPU.
- `--number_runs_per_each`: Specifies how many times to run each test.
- `--time_out`: Sets a timeout limit for each test.

The process splits tests for parallel execution, outputs results to CSV files, and merges them upon completion. Results are stored in a subdirectory within `Examples/random_txt/<subdir>` to preserve data. Execution time varies with the test suite size.

## Plotting Results

To plot results using `Plot_data.py`, follow these command-line instructions, customizing them based on your needs:

```bash
python3 Plot_data.py <directory> --shape <shape> --file <file_name> --fields <fields_to_plot> --pl_lines <lines_to_plot> --type_plot <plot_type>
```

- `<directory>`: The directory where the test data CSV is located, relative to `./examples/random_txt/` where the `merged_list_of_files_info.csv` is.
- `--shape`: Choose the plot shape: `lines`, `3d`, or `4d`.
- `--file`: Specify the CSV file name without the extension, defaulting to `merged_list_of_files_info`.
- `--fields`: Set the column(s) to plot against time, default is `num_states`.
- `--pl_lines`: Define which time metric to plot, with defaults including participants time, non-determinism time and a-consistency-time.
- `--type_plot`: Choose the type of 2D plot, with `line` as the default.

This command allows for versatile plotting configurations, adjusting for different dimensions and aspects of the data captured in the CSV file. All plots are saved the directory directly.

## Reminder

All commands provided, such as running tests, generating examples, executing multiple examples, and plotting results with various scripts like `Main.py`, `Generate_examples.py`, `Random_exec.py`, and `Plot_data.py`, come equipped with a `--help` option. Utilizing `--help` will display detailed usage instructions and available options for each command, aiding users in understanding and effectively utilizing the tool's features.