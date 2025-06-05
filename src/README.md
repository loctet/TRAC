# DAFS Validator Web Application

This web application provides a user-friendly interface for validating DAFS (Distributed Abstract Finite State Machine) specifications. It allows users to input DAFS text, validate it, and visualize the resulting state machine graph.

## Features

- Text input for DAFS specifications
- Real-time validation of DAFS syntax and semantics
- Interactive graph visualization of the state machine
- Modern and responsive user interface

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Java Runtime Environment (JRE) for graph generation

## Installation

1. Clone the repository and navigate to the `src` directory:
   ```bash
   cd src
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure you're in the `src` directory and your virtual environment is activated.

2. Start the Flask server:
   ```bash
   python web_app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Enter your DAFS specification in the text area on the left side of the page.
2. Click the "Validate DAFS" button to process the specification.
3. The results will be displayed on the right side:
   - Validation status (success or error)
   - Interactive graph visualization of the state machine

## Graph Visualization

The graph visualization is interactive:
- Drag nodes to rearrange the layout
- Hover over nodes to see details
- The graph automatically adjusts to the container size

## Error Handling

The application provides clear error messages for:
- Invalid DAFS syntax
- Semantic errors
- Processing errors

## Notes

- The application uses temporary files to process the DAFS specification
- All temporary files are automatically cleaned up after processing
- The graph visualization uses D3.js for smooth and interactive rendering 