# INTRODUCTION 

TRAC is a tool designed to enhance the development and verification of coodination protocols. It focuses on analyzing the well-formedness of DAFSMs, ensuring the consistency of the model. This tool is instrumental in identifying potential issues early in the development lifecycle, making it a valuable asset for developers and researchers aiming to validate the logical consistency within a protocol.

## Features

- **DAFSM Validation**: Checks well-formedness of DAFSM specifications[(The full paper)](https://link.springer.com/chapter/10.1007/978-3-031-62697-5_13) including :
  - Participant consistency
  - Non-determinism
  - Action consistency
  - Path reachability
- **Visualization**: Generates interactive graph visualizations of DAFSMs
- **Multiple Interfaces**:
  - Command-line interface for batch processing and automation
  - Web interface for interactive validation and visualization


## Folder structure

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

1. **Python Installation**
   - Install Python 3.7 or higher from [python.org](https://www.python.org/downloads/)
   - For detailed installation instructions, refer to [Real Python's Installation Guide](https://realpython.com/installing-python/)
   - Ensure Python is added to your system's PATH during installation
   - Verify installation by running:
     ```bash
     python --version
     pip --version
     ```

2. **Graphviz Installation**
   - Required for graph visualization
   - Windows:
     - Download and install from [Graphviz Download Page](https://graphviz.org/download/)
     - Add Graphviz to system PATH
   - Linux:
     ```bash
     sudo apt-get install graphviz  # Ubuntu/Debian
     sudo yum install graphviz      # CentOS/RHEL
     ```
   - macOS:
     ```bash
     brew install graphviz
     ```
   - Verify installation:
     ```bash
     dot -V
     ```

3. **Java Runtime Environment (JRE)**
   - Required for graph generation
   - Download and install from [Oracle JRE](https://www.java.com/download/) or [OpenJDK](https://adoptium.net/)
   - Verify installation:
     ```bash
     java -version
     ```

### Environment Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/loctet/TRAC.git
   cd TRAC
   git checkout TRAC_v1
   ```

2. **Create and Activate Virtual Environment in repository**
   - Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**
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
- graphviz: Python bindings for Graphviz

### Verify Installation
1. **Test Web Interface**
   ```bash
   python web_app.py
   ```
   Then open `http://localhost:5000` in your browser.

2. **Test Command-Line Interface**
   ```bash
   .\trac --help
   ```
   This should display the help message with available options.



## Usage

TRAC can be used in two modes: web interface and command-line.

### 1. Web Interface

#### Web Interface Features
- Text input for DAFSM specifications
- Real-time validation 
- Graph visualization
- Error reporting
- Transitions view
- Import/Export functionality:
  - Import DAFSM specifications from text files
  - Download validated specifications
  - Export graph visualizations
  - Save JSON representations

#### Using the Web Interface
1. **Input Methods**:
   - Direct text input in the editor
   - Import from text file:
     - Click "Import" button
     - Select a .dafsm or .txt or .trac file
     - File content will be loaded into the editor
   - Paste from clipboard
2. Click *Validate* to process
3. **View results**:
   - Analysis result
   - Generated Visual representation of the FSM graph
   - Transition view
   - Any error messages
4. **Export Options**:
   - *Download* validated specification as .dafsm file


## DAFSM Specification Format

### Basic Structure
```
roles O B                    // Role declarations space separated
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
- Basic types: `int`, `string`, `bool`, `float`
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

### 2. Command-Line Interface

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



## Performance Evaluation
[View the main branch](https://github.com/loctet/TRAC/)

## Error Handling

TRAC provides detailed error reporting for:
- Syntax errors in DAFSM specifications
- Well-formedness violations
- Participant consistency issues
- Non-deterministic transitions
- Action consistency problems
- Path reachability issues
