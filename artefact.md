## COORDINATION 2024: Artefact submission for the paper #8


This document specifies the instructions for the AEC of COORDINATION 2024 for the evaluation of our artefact submission. We set a `Docker` container for `TRAC` in order to simplify the work of the AEC (the `README` file at [https://github.com/loctet/TRAC](https://github.com/loctet/TRAC) contains the instructions for the manual installation procedure).


# Table of content 
- [1. Installation](#1-installation)
- [2. Reproducibility](#2-reproducibility)
   - [2.1 How table 1 has been created](#21-how-table-1-has-been-created)
   - [2.2 How to check well formedness of the Azure benchmarks](#22-how-to-check-the-well-formedness-of-the-azure-benchmarks)
   - [2.3 How to check the randomly generated models ](#23-how-to-check-the-randomly-generated-models)
- [3. Usage](#3-usage)
   - [3.1 Format of DAFSMs](#31-format-of-dafsms)
   - [3.2 Examples of non well-formed models](#32-examples-of-non-well-formed-models)
   - [3.3 Commands for performance evaluation](#33-commands-for-performance-evaluation)
   - [3.4 Run you own examples](#34-run-your-own-examples)
- [4. Documentation](#4-documentation)
- [5. Tips](#5-tips)

# 1. Installation
Follow the instructions at [https://docs.docker.com/](https://docs.docker.com/) to install `Docker` on your system.

To install and run TRAC using `Docker`:

1. Pull the `Docker` image:
   ```bash
   docker pull loctet/trac_dafsms:v1
   ```
2. Run the container:
   ```bash
   docker run -it loctet/trac_dafsms:v1
   ```
   (you might need to run the above commands as `root`). The former command downloads the `Docker` image of `TRAC` while the latter starts a container with an interactive terminal.


# 2. Reproducibility

## 2.1 How Table 1 has been created
We now describe how the information in Table 1 of our COORDINATION has
been determined. 
We recall that Table 1 reports how our framework captures the features of the smart contracts in the Azure repository described at the following links:
- [Hello Blockchain](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/hello-blockchain)
- [Simple Marketplace](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/simple-marketplace)
- [Basic Provenance](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/basic-provenance)
- [Digital Locker](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/digital-locker)
- [Refrigerated Transportation](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/refrigerated-transportation)
- [Asset Transfer](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/asset-transfer)
- [Room Thermostat](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/room-thermostat)
- [Defective Component Counter](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/defective-component-counter)
- [Frequent Flyer Rewards Calculator](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/frequent-flyer-rewards-calculator).

For each smart contract, the table below reports
- where the features are met in the `Solidity` implementation in the Azure repository
- the lines in the DAFSM model where the feature is captured (if at all) 


|Example (link to .sol )| Line in Code for the feature | How TRAC handle it |
|---|---|---|
|[Simple Marketplace](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/simple-marketplace/ethereum/SimpleMarketplace.sol)|BI :  Lines 21 & 44|BI:  [Line 1, 2 & 6](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/simplemarket_place.txt#L2) |
|[Hello Blockchain](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/hello-blockchain/HelloBlockchain.sol)|BI:  Lines 19 & 39|Bi:  [Line 1 & 3](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/hello_blockchain.txt) |
|[Bazaar](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/bazaar-item-listing/ethereum/BazaarItemListing.zip)|ICI:  BazaarItem (Line 78) ItemList(Line 40) <br/>BI :  BazaarItem (Line 76) ItemList(Line 33)| |
|[Ping Pong](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/ping-pong-game/ethereum/PingPongGame.sol) |BI :  Line 16 & 67<br/>ICI :  Lines 18, 29, 41, 47, 77, 82 & 88| |
|[Defective Component Counter](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/defective-component-counter/ethereum/DefectiveComponentCounter.sol)| BI:  Line 17<br>PP: Line 15 |BI: [Line 1](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/defective_component_counter.txt)<br/>PP: [Line 1](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/defective_component_counter.txt) |
|[Frequent Flyer Rewards Calculator](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/frequent-flyer-rewards-calculator/ethereum/FrequentFlyerRewardsCalculator.sol)| BI :  Line 20 <br/>PP :  Line 18 |BI:  [Line 1](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/frequent_flyer_rewards_calculator.txt)<br/>PP:  [Line 1](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/frequent_flyer_rewards_calculator.txt) |
|[Room Thermostat](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/room-thermostat/ethereum/RoomThermostat.sol)| PP :  Line 16 |PP:  [Line 1](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/room_thermostat.txt) |
|[Asset Transfer](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/asset-transfer/ethereum/AssetTransfer.sol)| BI :  Line 18, <br/>PP: Line 49<br/>RR :  Lines 97 & 171 |BI:  [Lines 1& 3](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/asset_transfer.txt)<br/>PP: [Lines 2& 7](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/asset_transfer.txt)<br/>RR: |
|[Basic Provenance](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/basic-provenance/ethereum/BasicProvenance.sol)| BI:  Line 19 <br/>PP:  Line 17, 26 <br/>RR :  Line 38, 51 |BI:  [Line 1](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/basic_provenance.txt)<br/>PP:  [Line 1, 2, 3](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/basic_provenance.txt)<br/>RR: |
|[Refrigerated Transportation](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/refrigerated-transportation/ethereum/RefrigeratedTransportation.sol)| BI:  Line 32 <br/>PP:  Line 28, 89 <br/>RR :  Line 118, 143 <br/>MRP :  Lines 33, 34, 119 & 142 |BI:  [Line 1](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/refrigirated_transport.txt)<br/>PP:  [Line 1, 5 & 9](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/refrigirated_transport.txt)<br/>RR:  <br/>MRP: |
|[Digital Locker](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/digital-locker/ethereum/DigitalLocker.sol)| BI :  Line 21 <br/>PP:  Lines 19, 68 <br/>RR :  Lines 102,126, 127, 139 & 149 <br/>MRP :  Lines 76, 91 |BI: [Line 1](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/digital_locker.txt)<br/>PP: [Line 1](https://github.com/loctet/TRAC/blob/main/src/Examples/dafsm_txt/azure/digital_locker.txt)<br/>RR:  <br/>MRP: |

## 2.2. How to check the well-formedness of the Azure benchmarks

The DAFSM models for each smart contract but for `Bazaar` and `Ping Pong` of the Azure repository can be found in the directory `Examples/dafsms_txt/azure`.

To check a model with `TRAC`, navigate to the directory `src` and execute the `Main.py` as done with the `Docker` commands below on the  [`simple-marketplace`](https://github.com/Azure-Samples/blockchain/tree/master/blockchain-workbench/application-and-smart-contract-samples/simple-marketplace) smart contract:
   ```bash
   cd src
   python3 Main.py --filetype txt "azure/simplemarket_place"
   ```
The latter command produces the following output
   ```tex
   --Parsing Txt to generate Json file

   Checking the well formness of the model----

   (!) Verdict: Well Formed
   ```
reporting that the DAFSMs for the `simplemarket_place` is well formed. For the other smart contracts it is enough to execute the python script on the corresponding DAFSM.


## 2.3. How to check the randomly generated models 

The 135 randomly generated models used in last part of Section 4 of our paper are in `src/Examples/random_txt/tests_dafsm_1` splitted in subfolders each containing 5 DAFSMs and a `list_of_files_info.csv` file with metadata on the DAFSMs (we detail the metadata). Our performance analysis can be reproduced by executing the following commands in the `Docker`:

   ```bash
   performancecd src
   python3 Random_exec.py tests_dafsms_1 --number_runs_per_each 10 --number_test_per_cpu 5 --time_out 300000000000  
   ```
Note that the results may vary due to different hardware/software configurations than those we used (cf. page 12 of the paper).
The latter command above specifies the target directory `tests_dafsms_1`, the number of repetitions for each experiment, the number of experiments analyzed by each cpu, and the time out in nanoseconds. While running the checks further `csv` files will be generated and finally merged into a single file called `src/Examples/random_txt/tests_dafsm_1/merged_list_of_files_info.csv`. Notice if the target directory in the command above is not changed, this `csv` file will be overwritten at each execution. The current content of the `csv` files when starting the `Docker` contains the values plotted in Figures 2 and 3 of our paper.

The plots can be obtained by executing 
```bash
python3 ./plot_data.py examples_1 --file merged_list_of_files_info --field num_states,num_transitions,num_paths --pl_lines participants_time,non_determinism_time,a_consistency_time,z3_running_time --shape 2d --type_plot scatter
```
in the `Docker`; the plots are `png` images saved in the directory `Examples/random_txt/tests_dafsms_1`.



# 3. Usage

## 3.1. Format of DAFSMs
The DAFSMs model (Definition 1 of our paper) is renderer in `TRAC` with a DSL which represents a DAFSM as sequences of lines, each specifying a transition of the DAFSM. We explain the format of transitions through the Simple Market Place contract (&#8594; following Example 1 of our paper), which in our DSL is

<pre style="font-size:10px; background-color:#f6f8fa; padding:10px">
_ {True} o:O > starts(c,string _description, int _price) {description := _description & price := _price} {string description, int price, int offer} S0
S0 {_offer > 0} b:B > c.makeOffer(int _offer) {offer := _offer} S1
S1 {True} o > c.acceptOffer() {} S2+
S1 {True} o > c.rejectOffer() {} S01
S01 {_offer > 0} any b:B > c.makeOffer(int _offer) {offer := _offer} S1
S01 {_offer > 0} b:B > c.makeOffer(int _offer) {offer := _offer} S1
</pre>

hereafter called `SMP`; the names of states in `SMP` differ from those in Example 1, but this is immaterial for the analysis.


In general a transition consists of

   - a source and a target state; a trailing `+` denotes final states (like `S2+` above)
   - a guard specified in the notation of `Z3`
   - a qualified participant `p : P` corresponding to <em><i>ν</i></em> p : P in the paper, `any p : P`, or just `p`
   - a call to an operation of the contract
   - a list of `&`-separate assignments.

The first line of `SMP` is a special transition corresponding to the edge entering the initial state in Example 1 barred for

- the fact that the source state is `_` is used to identify the initial state
- the additional `_description` parameter, omitted in the paper for readability

The guard `True` in the transition is the *precondition* while the list of assignments `{description := _description & price := _price}` is followed by  an explicit declaration of the contract variables to capture the assumption in the first item of Page 3 of the paper; the transition introduces a fresh participant `o` with role `O` which renders the object-oriented mechanism described just above Definition 1.

Conventionally, parameters start with `_` to distinguish them from contract variables. 

## 3.2. Examples of non well-formed models
As seen in [Section 2.2](#22-how-to-check-the-well-formedness-of-the-azure-benchmarks), `SMP` is well-formed; we now apply `TRAC` to detect non well-formed models. The file `azure/simplemarket_place_edit_1` contains a modified DAFSM obtained by replacing the `acceptOffer` transition of `SMP` with

<span style="color:red">`S1 {True} x > c.acceptOffer() {} S2+`</span> 

Executing in the `Docker`

```bash
python3 Main.py --filetype txt "azure/simplemarket_place_edit_1"
```

produces

```
The Path : _-starts-S0>S0-makeOffer-S1 does not contain the participant x : []
Error from this stage:S1_acceptOffer()_S2
--For _acceptOffer_0:   Check result ::  False
--- Participants       : False

(!) Verdict: Not Well Formed
```

stating that participant `x` has not been introduced. In fact, the `CallerCheck` finds a path to `S1` where  participant `x` is not introduced (first line of the output above) identified in the trasition from `S1` to `S2` with label `acceptOffer` (second line of the output). The last three lines of the output inform the user that well formedness does not hold for the use of a non introduced participant.

The file `azure/simplemarket_place_edit_2` modifies `SMP` by replacing the transitions `acceptOffer` and `rejectOffer` respectively with

<span style="color:red">`S1 {False} o > c.acceptOffer() {} S01`</span> and <span style="color:red">`S1 {False} o > c.rejectOffer() {} S01`</span> 

Executing now the command below in the `Docker` 

```bash
python3 Main.py --filetype txt "azure/simplemarket_place_edit_2"
```

produces

```
Error from this state:S01_makeOffer(int _offer)_S1
--For _makeOffer_0:   Check result ::  False
--- A-Consistency: False

   Simplify of the Not Formula:  Not(And(Not(_offer <= 0), offer == _offer))  ::  True
   
   (!) Verdict: Not Well Formed
```
which tells that consistency is violated by the transition 

```
S0 {_offer > 0} b:B > c.makeOffer(int _offer) {offer := _offer} S1
```

The simplification operated by `Z3` on the formula in the last but one line of the output yields (the formula) `True`.

The `Main.py` script used above accepts the `check_type <chk>` optional parameters where `<chk>` can take two qualifiers; `check_type` defaults to `1` which checks well-formedness and can be set to `fsm` to generate a visual representation of a DAFSM as a `png` file.

The image below for `SMP` is generated by invoking the `GraphStream` library ([https://graphstream-project.org/](https://graphstream-project.org/)) from our `GraphGen` component (cf. Figure 1 in the paper) 

![Simplemarket_place `TRAC` DAFSMs](./images/fsm_simplemarke_place.png) 

(labels are simplified for readability). The description in Section 3.1 of the paper wrongly states that `GraphGen` is "a third-party component", but in fact it should read that `GraphGen` is a wrapper to invoke `GraphStream`. Unfortunately, the image cannot be visualised from inside the `Docker` because `GraphGen` uses the functionality of `GraphStream` that displays the graph in an interactive window. So, to see the model it is necessary to use `TRAC` from outside the `Docker`.


## 3.3. Commands for performance evaluation
To evaluate the performances of `TRAC`, we created a randomizer that contains a generator of random models in our DSL, a program that applies `TRAC` on the generated models, and a visualiser to plot data from `csv` files. In the following, we explain how to perform each step.


### **Generating random examples**
The following command generates 100 random models and saves them in the directory `Examples/random_txt/your_sub_dir_name`:

```bash
python3 Generate_examples.py --directory your_sub_dir_name --num_tests 100
```

The generation process can be customised setting optional parameters of `Generate_examples.py`; if not specified, all but the last four parameters default to randomly generated values:
- `--num_tests <num>` the number of tests to generate
- `--num_states <num>` the number of states per test
- `--num_actions <num>` is the number of actions
- `--num_vars <num>` is the number of variables
- `--max_num_transitions <num>` is the maximal number of transitions that should be at least the number of states (minus 1) 
- `--max_branching_factor <num>` is the maximum branching factor should be greater or equal than 1; in corner cases, the branching factor is predominant and may lead to exceed the maximum number of transitions
- `--num_participants <num>` is the maximum number of participants variables
- `--steps <num>` the increment steps for generating tests (meaningful only if `--incremental_gen` below is set to true; default: `10`)
- `--incremental_gen [True|False]` enables/disables incremental generation of models (default: `False`)
- `--merge_only_csv [True|False]` if set to `True` merges results into a single `csv` file; all other parameters are ignored when this is flag is used (default: `False`)
- `--num_example_for_each <num>` is the number of models to generate for each configuration (default:`5`).

To generate the models used in Section 4 of the paper, we ran the following command:

```bash 
python3 Generate_examples.py --directory tests_dafsms_1 --steps 5 --num_example_for_each 5 --num_tests 30 --incremental_gen True
```
**Warning**: the directory `Examples/random_txt/tests_dafsms_1` in the `Docker` is populated with the models and `csv` files generated for the experiments reported in the paper. Executing the command above in the `Docker` would overwrite the files generated for the experiments in our paper.


---------------------------------------------------------

The `csv` file containing metadata of each generated example. [The full description of the metadata list can be found here](#4-documentation)

The check of the generated examples starts immediately after generation completion. This process allows the auto-generation and checking of DAFSMs examples, facilitating the evaluation of `TRAC`.


### **Running a set of examples**
The following command configuration allows you to check a set of examples in a given sub-repository `<subdir>` in `Examples/random_txt`:

```bash
python3 Random_exec.py --directory <subdir> --number_test_per_cpu 5 --number_runs_per_each 10 --time_out 300000000000
```
The latter command takes all the examples metadata information in file `list_of_files_info.csv` in the `<subdir>`, allocates 5 examples to each CPU, and checks each example 10 times to have an average measured time, each CPU will output a CSV file `list_of_files_info_{id}.csv` at the end, and all generated csvs will be merged into `merged_list_of_files_info.csv` upon completion of all the examples.
The checking process can be customized setting some parameters of `Random_exec.py`. The full list of available parameters follows: 

   - `--merge_csv`only merges individual CSV results into `merged_list_of_files_info.csv`
   - `--add_path` just count the number_path to each test in the `list_of_files_info.csv`
   - `--number_test_per_cpu` determines how many tests are to run in parallel per CPU
   - `--number_runs_per_each` specifies how many times to run each test
   - `--time_out` sets a timeout limit for each test

The checking process splits tests for parallel execution, each thread output results into a CSV file and merges them upon completion. Results are stored in a subdirectory within `Examples/random_txt/<subdir>` to preserve data.


### Plotting Results
To plot data using `Plot_data.py`, the following command can be customized with some given parameters below:

```bash
python3 Plot_data.py <directory> --shape <shape> --file <file_name> --fields <fields_to_plot> --pl_lines <lines_to_plot> --type_plot <plot_type>
```
   - `<directory>` the directory where the test data CSV is located, relative to `./Examples/random_txt/` where the `merged_list_of_files_info.csv` is
   - `--shape` choose the plot shape: `2d`, `3d`, or `4d`
   - `--file` specify the CSV file name without the extension, defaulting to `merged_list_of_files_info`
   - `--fields` set the column(s) to plot against time, default is `num_states`
   - `--pl_lines` define which time metric to plot against the fields, with defaults including participants' time, non-determinism time,and a-consistency-time
   - `--type_plot` choose the type of 2D plot, with `line`  (values `line`, `scatter`, `bar`)as the default
   - `--scale` Y scale function, with default `log` (values `log`, `linear`).

To generate the plots of section 4 of the paper, we ran the following commands:

```bash
python3 Plot_data.py tests_dafsms_1 --file merged_list_of_files_info --field num_states,num_transitions,num_paths --pl_lines participants_time,non_determinism_time,a_consistency_time,z3_running_time --shape 2d --type_plot scatter --scale linear

python3 Plot_data.py tests_dafsms_1 --file merged_list_of_files_info --field num_states,num_transitions,num_paths --pl_lines participants_time,non_determinism_time,a_consistency_time,z3_running_time --shape 2d --type_plot scatter --scale log
```

This command allows different plotting configurations, adjusting for different dimensions and aspects of the data captured in the CSV file. All plots are saved in the directory `<directory>`.


## 3.4. Run your own examples
Now that the check of some examples is completed, you can design some DAFSMs and check if they are well-formed by giving the name of the file to the following command (`python3 Main.py --filetype txt "xxxxxxxxx"`) 

/!\ All manually executed examples should be placed in the folder  `Examples/dafsms_txt`. You can create sub-dirs, just be assured to run the above command with the exact name to the example `<subdir>/<example>`. 

Some examples can be found in `Examples/other_tests` testing some scenarios which are not found in the Azure repository. 

______________________________

# 4. Documentation

 The full documentation in HTML format can be downloaded [in from the git repository](https://github.com/loctet/TRAC/tree/main/docs/trac-html-doc.zip)

   ## CSV Header Description
   - `path` the path of the file
   - `num_states` number of states in the FSM
   - `num_actions` number of actions in the FSM
   - `num_vars` number of variables in the FSM
   - `max_branching_factor` maximum branching factor in the FSM
   - `num_participants` number of participants in the FSM
   - `num_transitions` number of transitions in the FSM
   - `seed_num` seed number used for randomization
   - `min_param_num` minimum number of parameters
   - `average_param_num` average number of parameters
   - `max_param_num` maximum number of parameters
   - `min_bf_num` minimum number of branching factors
   - `average_bf_num` average number of branching factors
   - `max_bf_num` maximum number of branching factors
   - `num_paths` number of paths in the FSM
   - `verdict` verdict of the verification process
   - `participants_time` time taken for checking participants
   - `non_determinism_time` time taken for non-determinism check
   - `a_consistency_time` time taken for action consistency check
   - `f_building_time` time taken for formula building
   - `building_time` time taken for building
   - `z3_running_time` time taken for running Z3
   - `total` total time taken for the process
   - `is_time_out` indicates if there was a timeout during processing.


# 5. Tips
All commands provided, `Main.py`, `Generate_examples.py`, `Random_exec.py`, and `Plot_data.py`, come equipped with a `--help` option. Utilizing `--help` will display detailed usage instructions and available options for each command, aiding users in understanding and effectively utilizing the tool's features.
```bash
   python3 Main.py --help
```
