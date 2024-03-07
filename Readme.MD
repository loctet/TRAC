# TRAC Tool README

## Introduction to TRAC

TRAC is a tool designed to enhance the development and verification of coodination protocols. It focuses on analyzing the well-formedness of DAFSMs, ensuring the consistency of the model. This tool is instrumental in identifying potential issues early in the development lifecycle, making it a valuable asset for developers and researchers aiming to validate the logical consistency within a protocol.

## Folder architecture
The `TRAC` folder architecture is organized as follows:
|-- docker/                            Constains docker configuration files <br/>
|-- docs/                                 Contains documentation files. <br/>
|   |-- html/                            HTML format documentation files. <br/>
|-- ExperimentalData/         Directory for experimental data. <br/>
|   |-- tests_dafsm_1/   	Contains data for experimental tests of the paper. <br/>
|-- images/                             Directory for images used in the readme or documentation. <br/>
|-- src/                                     Contains source code files. <br/>
|   |-- Examples/                    Directory for example files. <br/>
|   |   |-- dafsm_txt/              Holds DAFSM model text files for manual execution. <br/>
|   |   |-- jsons/                       Stores JSON files. <br/>
|   |   |-- random_json/         Stores randomly generated JSON files. <br/>
|   |   |-- random_txt/            Contains randomly generated DAFSM model text files. <br/>
|   |-- GraphGen/                    `.jar` for graph visualization. <br/>
|   |-- Z3_models/                  Directory for storing Z3 model files. <br/>

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

If Docker is not installed on your system, follow the official Docker installation instructions in [Docker's official documentation](https://docs.docker.com/engine/install/ubuntu/). This guide provides a comprehensive step-by-step process to get Docker set up and running on your machine.

TRAC can also be cloned directly from its GitHub repository for those who prefer working with the source code.

## Installation Instructions

Before installing TRAC, ensure Python 3.6 or later is installed on your system. TRAC relies on several Python packages for its operation. Use the following pip command to install the necessary dependencies:

```bash
pip install z3-solver matplotlib numpy plotly pandas networkx
```
Also make sure the `java JRE` is installed to run the `java` command. This is used to show a visual view of the DAFSMs.

## Running  "Simple Marketplace" example

To run the `Simple Marketplace` examples example with TRAC:

1. **Navigate to the TRAC Directory**: Open a terminal and change directory `cd TRAC/src`.

2. **Locate the Example**: The `simplemarket_place` example taken from [Azure repository](https://github.com/Azure-Samples/blockchain/tree/master/blockchain-workbench/application-and-smart-contract-samples/simple-marketplace) is already in `src/Examples/dafsms_txt/azure` directory as well as [other Azure blockchain-workbench examples](https://github.com/Azure-Samples/blockchain/tree/master/blockchain-workbench/application-and-smart-contract-samples) 

   All manually executed examples should be kept in the folder  `src/Examples/dafsms_txt` you can create subdirs, just be assured to give the exact path to the command `Main.py`.

3. **Execute the Example**:

   - Use `Main.py` to run the example. The command syntax is:
     ```bash
     python3 Main.py --filetype txt "azure/simplemarket_place"
     ```
   - This command tells TRAC to check the well-formedness of `simplemarket_place` model.


    The output of the command should be `(!) Verdict: Well Formed`

   ____________________

```
_ {True} o:O > starts(c,string _description, int _price) \
        {description := _description & price := _price} \
        {string description, int price, int offer} S0
S0 {_offer > 0} b:B > c.makeOffer(int _offer) {offer := _offer} S1
S1 {True} o > c.acceptOffer() {} S2+
S1 {True} o > c.rejectOffer() {} S01
S01 {_offer > 0} any b:B > c.makeOffer(int _offer) {offer := _offer} S1
S01 {_offer > 0} b:B > c.makeOffer(int _offer) {offer := _offer} S1
```

hereafter called `SMP`.


In general, a transition consists of

   - a source and a target state; a trailing `+` denotes final states (like `S2+` above)
   - a guard specified in the notation of `Z3`
   - a qualified participant `p : P` corresponding to <em><i>&#x3BD;</i></em> p : P, `any p : P`, or just `p` 
   - a call to an operation of the contract
   - a list of `&`-separate assignments.

The first line of `SMP` is a special transition corresponding to the edge entering the initial state in Example 1 barred for

- the fact that the source state is `_` is used to identify the initial state
- the additional `_description` parameter, omitted in the paper for readability

The guard `True` in the transition is the *precondition* while the list of assignments `{description := _description & price := _price}` is followed by an explicit declaration of the contract variables, the transition introduces a fresh participant `o` with role `O` which renders the object-oriented mechanism.

Conventionally, parameters start with `_` to distinguish them from contract variables. 

To visualise the `SPM` model we can execute the following command:

 ```bash
 python3 Main.py --filetype txt "azure/simplemarket_place" fsm
 ```

The later command will open a window with and interactive image.


![Simplemarket_place TRAC DAFSMs](./images/fsm_simplemarke_place.png)

## Non-well-formed example

In `SMP`, modify transition `S1 {True} o > c.rejectOffer() {} S01` to `S1 {False} o > c.rejectOffer() {} S01`
and transition `S1 {True} o > c.acceptOffer() {} S01` to `S1 {False} o > c.acceptOffer() {} S01`.
The modification created a new DAFSMs where from `S1` there is no reachable outgoing transition. 

After running the check, we have the following output: 

```
Error from this transitions:S01_makeOffer(int _offer)_S1

--For _makeOffer_0:   Check result ::  False
--- A-Consistency: False

Simplification of the of the negation of the formula:  Not(And(Not(_offer <= 0), offer == _offer))  ::  True

(!) Verdict: Not Well Formed
```
telling that the consistency rule is violated with transition `S01_makeOffer(int _offer)_S1` reaching `S1`.

--------

To check a model the following command can be run:

```
python3 Main.py --filetype txt "file_name"
```

Where `fime_name` is the name of the txt file containing the model. 

By default, the model should be stored `src/Examples/dafsms_txt`. 

Further models can be found in `src/Examples/other_tests`.

Settings of `TRAC` can be configured in the file `src/Settings.py`. This includes default directories where models are stored and default values of parameters for `TRAC's`commands. For more detailed information about these settings, refer to the [full documentation](#further-information).

## Main.py configuration

The `Main.py`, can take some configurations as follows:

- `file_name`: Specifies the name of the file (JSON or TXT) to process, without its extension. This is the primary input for TRAC to analyze.
- `check_type`: Optional. Defines the type of check to perform on the input file. It can be one of four options:
  - `1` for Well-Formedness Check,
  - `fsm` for printing the Finite State Machine (FSM). The default is `1`.
- `--filetype`: Optional. Indicates the type of the input file, either `json` or `txt`. The default is `json`.
- `--non_stop`: Optional. Determines the mode of checking, where `1` (default) continues checking even after errors are found, and `2` stops immediately when an error is detected.
- `--time_out`: Optional. Sets a timeout for the operation in seconds. The default is `0`, meaning no timeout.
This detailed explanation provides a comprehensive guide on how to utilize `Main.py` for different operations within the TRAC tool.

## Commands for performance evaluation

To evaluate the performances of `TRAC`, we created a randomizer that contains a generator of random models in our DSL, a program that applies `TRAC` on the generated models, and a visualiser to plot data from `csv` files. In the following, we explain how to perform each step.

The following command generates 100 random models, saves them in the directory `src/Examples/random_txt/your_sub_dir_name`, checks for the well-formedness of the models, and collects performance data in `csv` files:

```bash
python3 Generate_examples.py --directory your_sub_dir_name --num_tests 100
```

The generation process can be customised setting optional parameters of `Generate_examples.py`; if not specified, all but the last four parameters default to randomly generated values:

- `--num_tests <num>` the number of tests to generate
- `--num_states <num>` the number of states per test
- `--num_actions <num>` is the number of actions
- `--num_vars <num>` is the number of variables
- `--max_num_transitions <num>` is the maximal number of transitions that should be at least the number of states (minus 1) 
- `--max_branching_factor <num>` is the maximum branching factor that should be greater or equal to 1; in corner cases, the branching factor is predominant and may lead to exceeding the maximum number of transitions
- `--num_participants <num>` is the maximum number of participant variables
- `--steps <num>` the increment steps for generating tests (meaningful only if `--incremental_gen` below is set to true; default: `10`)
- `--incremental_gen [True|False]` enables/disables incremental generation of models (default: `False`)
- `--merge_only_csv [True|False]` if set to `True` merges results into a single `csv` file; all other parameters are ignored when this is flag is used (default: `False`)
- `--num_example_for_each <num>` is the number of models to generate for each configuration (default:`5`).

Well-formedness check of the models starts immediately after the generation phase is completed. The results of each check are stored in a `csv` file together with metadata for the performance evaluation. (The full description of the metadata is in [section below](#further-information).)


It is possible to check existing generated models stored in `src/Examples/random_txt/<subdir>` with the following command

```bash
python3 Random_exec.py <subdir> --number_test_per_cpu 5 --number_runs_per_each 10\
	--time_out 300000000000
```

where 

   - `--number_test_per_cpu <num>` determines how many tests are to run in parallel per CPU (default: `5`)
   - `--number_runs_per_each <num>` specifies how many times to run each model check (default: `10`)
   - `--time_out <num>` sets a timeout limit to perform each model check (default: `300000000000`).

The command above reads the metadata in `src/Examples/random_txt/<subdir>/list_of_files_info.csv`, allocates 5 models to each CPU, and performs the check. Each CPU will output a `csv` file `src/Examples/random_txt/<subdir>/list_of_files_info_<id>.csv` for each set of models' `<id>` assigned to the CPU. All `csv` files are merged into the file `src/Examples/random_txt/<subdir>/merged_list_of_files_info.csv` upon completion of the evaluation.

The checking process can be customized by setting the following optional parameters:

   - `--merge_csv [True|False]` if set to `True`, merges THE generated `csv` files into `src/Examples/random_txt/<subdir>/merged_list_of_files_info.csv` (default: `False`)
   - `--add_path [True|False]` if set to `True`, counts the number path for each model in the `src/Examples/random_txt/<subdir>/list_of_files_info.csv` (default: `False`)

To preserve data `Random_exec.py` stores results in `src/Examples/random_txt/<subdir>/<time>` where `<time>` is the time when the execution started.


Data are plotted using `Plot_data.py`

```bash
python3 Plot_data.py <directory> --shape <shape> [--file <file_name>] [--fields <fields_to_plot>]\
	[--pl_lines <lines_to_plot>] [--type_plot <plot_type>]
```

where

   - `<directory>` is the sub-directory of `src/Examples/random_txt/<subdir>/` containing the `csv` files
   - `--shape [2d|3d]` sets the plot shape
   - `--file <str>` specify the name of the `csv` file (without the extension) (default: `merged_list_of_files_info`)
   - `--fields <list>` sets the column(s) in the `csv` file to plot (default: `num_states`)
   - `--pl_lines <list>` defines a comma-separated list of performance indicators to plot against the list set in `--fields` (default: `participants_time, non-determinism_time, a-consistency-time`)
   - `--type_plot [line|scatter|bar]` chooses the type of 2D plot (default: `line`)
   - `--scale [log|linear]` scale of the y-axis (default: `log`).

To generate the plots of Section 4<span style="-typora-class: textPaperPage;"> </span>, we ran the following commands:

```bash
python3 Plot_data.py tests_dafsms_1 --file merged_list_of_files_info\
	--field num_states,num_transitions,num_paths\
	--pl_lines participants_time,non_determinism_time,a_consistency_time,z3_running_time\
    --shape 2d --type_plot scatter --scale linear

python3 Plot_data.py tests_dafsms_1 --file merged_list_of_files_info\
	--field num_states,num_transitions,num_paths\
	--pl_lines participants_time,non_determinism_time,a_consistency_time,z3_running_time\
    --shape 2d --type_plot scatter --scale log
```

All generated plots are stored in the directory `src/Examples/random_txt/test_dafsms_1/`. 

## Further information

Below is the description of the header of the `csv` files:

   - `path` the path to the model file
   - `num_states` number of states 
   - `num_actions` number of actions
   - `num_vars` number of variables
   - `max_branching_factor` maximum branching factor
   - `num_participants` number of participants
   - `num_transitions` number of transitions
   - `seed_num` seed number used for randomization
   - `min_param_num` actual minimum number of parameters
   - `average_param_num` actual average number of parameters
   - `max_param_num` actual maximum number of parameters
   - `min_bf_num` actual minimum number of branching factors
   - `average_bf_num` actual average number of branching factors
   - `max_bf_num` actual maximum number of branching factors
   - `num_paths` number of paths
   - `verdict` verdict of the verification process
   - `participants_time` time taken for checking participants
   - `non_determinism_time` time taken for non-determinism check
   - `a_consistency_time` time taken for action consistency check
   - `f_building_time` time taken for formula building
   - `building_time` time taken for building
   - `z3_running_time` time taken for running Z3
   - `total` total time taken for the process
   - `is_time_out` indicates if there was a timeout during processing.


The complete documentation of `TRAC` includes detailed code explanations and usage instructions. After downloading, unzip the file to access the Sphinx-generated documentation. This documentation is available at [GitHub repository](https://github.com/loctet/TRAC/tree/main/docs/trac-html-doc.zip) and provides further insights on features of `TRAC`.

Commands  `Main.py`, `Generate_examples.py`, `Random_exec.py`, and `Plot_data.py` feature a `--help` option, e.g.,

```bash
   python3 Main.py --help
```

 prints a description of the available options and the usage of `Main.py`.