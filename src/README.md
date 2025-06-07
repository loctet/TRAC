# TRAC (Transition-based Reachability Analysis for Contracts)

TRAC is a powerful tool for analyzing and verifying Distributed Abstract Finite State Machine (DAFSM) specifications. It provides both command-line and web-based interfaces for validating the well-formedness of coordination protocols and smart contracts.

## Features

- **DAFSM Validation**: Checks well-formedness of DAFSM specifications including:
  - Participant consistency
  - Non-determinism
  - Action consistency
  - Path reachability
- **Visualization**: Generates interactive graph visualizations of DAFSMs
- **Multiple Interfaces**:
  - Command-line interface for batch processing and automation
  - Web interface for interactive validation and visualization
- **Support for Complex Specifications**:
  - Variable declarations and assignments
  - Guard conditions
  - Role-based participant management
  - Array and basic type support
  - If statements in assignment blocks

## Architecture

```
TRAC/
├── src/                    # Source code
│   ├── Examples/           # Example DAFSM specifications
│   │   ├── dafsm_txt/      # Text-based DAFSM examples
│   │   ├── jsons/          # JSON representations
│   │   └── random_txt/     # Generated test cases
│   ├── GraphGen/           # Graph visualization tools
│   ├── Z3_models/          # Z3 solver model files
│   ├── WebExamples/        # Web app generated files
│   ├── templates/          # Web interface templates
│   └── azure/              # Azure blockchain examples
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Dependencies
```bash
pip install -r requirements.txt
```

Required packages (will be installed by the previous command):
- z3-solver: For constraint solving
- flask: Web application framework
- flask-cors: Cross-origin resource sharing
- networkx: Graph operations
- matplotlib: Plotting
- numpy: Numerical operations
- box: Configuration management


## Usage

TRAC can be used in two modes: command-line and web interface.

```bash
cd src
```

### 1. Command-Line Interface


#### Basic Usage
```bash
.\trac [options] <file_name>
```

#### Options
- `--filetype [json|txt|dafsm]`: Input file type (default: dafsm)
- `--check_type [1|2|3|fsm]`: 
  - 1: Well-formedness check (default)
  - 2: Individual function check
  - 3: Path check
  - fsm: Generate FSM visualization
- `--non_stop [1|2]`: 
  - 1: Continue checking after errors (default)
  - 2: Stop on first error
- `--time_out <seconds>`: Set timeout for checks

#### Examples

1. Basic well-formedness check:
```bash
.\trac--filetype txt "Examples/dafsm_txt/azure/simplemarket_place"
```

2. Generate FSM visualization:
```bash
.\trac --filetype txt "Examples/dafsm_txt/azure/simplemarket_place" fsm
```

3. Path check with timeout:
```bash
.\trac --filetype txt "Examples/dafsm_txt/azure/simplemarket_place" 3 --time_out 30
```

### 2. Web Interface

#### Starting the Web Server
```bash
python web_app.py
```
Then open `http://localhost:5000` in your browser.

#### Web Interface Features
- Text input for DAFSM specifications
- Real-time validation
- Interactive graph visualization
- Error reporting
- JSON transition view

#### Using the Web Interface
1. Enter your DAFSM specification in the text area
2. Click "Validate DAFS" to process
3. View results:
   - Validation status
   - Generated FSM graph
   - JSON representation of transitions
   - Any error messages

## DAFSM Specification Format

### Basic Structure
```
roles O B                    // Role declarations
dafsm ContractName(param1, param2) by role caller    // Contract header
{
    // Variable declarations and assignments
    type var1;
    type var2 := value;
    if condition
}           // Initial state
[State1] {guard} (any|new Role) p > op(params) {assignments} [State2]    // Transitions
```

### Supported Types
- Basic types: `int`, `string`, `bool`
- Arrays: `array Int`, `array String`
- Role types: Any declared role name

### Example
```
roles O B
dafsm Marketplace(string _desc, int _price) by O o
{
    string description;
    int price := _price;
    if _price > 0
}
[S0]
[S0] {price > 0} new B b > makeOffer(int _offer) {offer := _offer} [S1]
[S1] {True} o > acceptOffer() {} [S2+]
```

## Performance Evaluation

TRAC includes tools for performance evaluation:

1. Generate test cases:
```bash
python Generate_examples.py --directory test_dir --num_tests 100
```

2. Run performance tests:
```bash
python Random_exec.py test_dir --number_test_per_cpu 5 --number_runs_per_each 10
```

3. Plot results:
```bash
python Plot_data.py test_dir --shape 2d --type_plot scatter
```

## Error Handling

TRAC provides detailed error reporting for:
- Syntax errors in DAFSM specifications
- Well-formedness violations
- Participant consistency issues
- Non-deterministic transitions
- Action consistency problems
- Path reachability issues
