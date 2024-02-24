# Readme.md - Running the Code for Z3 Temporal Logic Solver

This README file provides instructions on how to run the code that uses the Z3 Temporal Logic Solver. The code you provided is designed to check the satisfiability of temporal logic properties for a given Finite State Machine (FSM) described in a JSON file. To run the code successfully, follow these steps:

## Prerequisites

Before you can run the code, make sure you have the following prerequisites installed:

1. Python: The code is written in Python. You need Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

2. Z3: The code relies on the Z3 SMT solver. You can install Z3 using the following command:

   ```bash
   pip install z3-solver
   ```

## Running the Code

1. **Download the Code:** Ensure you have downloaded the code and saved it in a directory on your local machine.

2. **Input JSON File:** The code expects an input JSON file that describes the FSM and its properties. Make sure you have an input file in the same directory as the code. In your code, the `input_path` variable is set to `"./examples/simplemarket_place.json"`. You can either use this path or modify it to point to your input JSON file.

3. **Execute the Code:** Open a terminal or command prompt and navigate to the directory where you have saved the code and the input JSON file. Run the Python script using the following command:

   ```bash
   python .\Z3\Chercker.py
   ```

   Replace `Chercker.py` with the name of the Python script that contains the provided code. This will execute the code and attempt to check the satisfiability of temporal logic properties.

4. **Check the Result:** The code will generate solver code based on the input JSON file and execute it. If the `check_resut` variable is `True`, it means that the temporal logic properties are satisfiable. You will see the message "satisfiable" printed to the console. If `check_resut` is not `True`, it means that the properties are not satisfiable.

## Understanding the Output

The code generates solver code dynamically based on the input JSON file. If you are interested in the details of the solver code or the specific properties that were checked, you can inspect the printed `str_code` variable. This code is executed to check the properties.

## Troubleshooting

- If you encounter any errors or issues while running the code, ensure that your Python and Z3 installations are correct. Check for any syntax errors or missing dependencies.

- Make sure the input JSON file is correctly formatted and contains the FSM and property information.

- If you need help or have questions about specific properties or how the code works, feel free to reach out for assistance.

## Additional Information

Please refer to the specific FSM and property definitions in your input JSON file for more details on the properties being checked. If you have any questions or need further assistance related to this code, don't hesitate to contact me.

# JSON File Description for Finite State Machine (FSM)

Here is a description of the JSON file that defines the Finite State Machine (FSM) used in the provided code:

```json
{
    "id" : "c",
    "initialState" : "S0",
    "statesDeclaration" : "int a := 10 ; bool c := True; set B := 0; set M ",
    "states" : [ "S0", "S1", "S2" ],
    "finalStates" : [ "S1" ],
    "transitions" : [ {
      "from" : "_",
      "to" : "S1",
      "actionLabel" : "starts",
      "newParts" : [ {
        "role" : "O",
        "participants" : [ "o" ]
      } ],
      "existantParts" : {
        "role" : "",
        "participants" : [ ]
      },
      "preCondition" : "True",
      "postCondition" : "And(Or(False,True),True)",
      "input" : "",
      "varUpdate": "",
      "internal" : false,
      "externalCall" : true
    }, {
      "from" : "S1",
      "to" : "_",
      "actionLabel" : "f1",
      "newParts" : [ {
        "role" : "O",
        "participants" : [ "o" ]
      } ],
      "existantParts" : {
        "role" : "",
        "participants" : [ ]
      },
      "preCondition" : "And(Or(False,True),True)",
      "postCondition" : "",
      "input" : "",
      "varUpdate": "",
      "internal" : false,
      "externalCall" : false
    }, {
      "from" : "S1",
      "to" : "S2",
      "actionLabel" : "OK",
      "newParts" : [ {
        "role" : "O",
        "participants" : [ "o" ]
      } ],
      "existantParts" : {
        "role" : "",
        "participants" : [ ]
      },
      "preCondition" : "And(Or(False,True),a >= 10)",
      "postCondition" : "True",
      "input" : "",
      "varUpdate": "",
      "internal" : false,
      "externalCall" : false
    }],
    "rPAssociation" : [ {
        "role" : "O",
        "participants" : [ "o" ]
      }, {
        "role" : "B",
        "participants" : [ "b" ]
      }, {
        "role" : "D",
        "participants" : [ "d" ]
      } ]
}
```

**Description:**

- `"id"`: This is an identifier for the FSM, which is labeled as "c."

- `"initialState"`: The initial state of the FSM is "S0."

- `"statesDeclaration"`: This field contains variable declarations, including "int a := 10," "bool c := True," "set B := 0," and "set M." These variables are used to define the states of the FSM.

- `"states"`: The list of states in the FSM includes "S0," "S1," and "S2."

- `"finalStates"`: The final state is "S1."

- `"transitions"`: This section defines the transitions in the FSM. It includes transitions from the initial state to "S1" labeled as "starts," a self-transition in "S1" labeled as "f1," and a transition from "S1" to "S2" labeled as "OK." Each transition specifies preconditions, postconditions, and other details.

- `"rPAssociation"`: This section defines role-participant associations, including the roles "O," "B," and "D" associated with participants "o," "b," and "d," respectively.

- `"varUpdate"` : This is where to add how a function changes the state of vaiables

The JSON file provides the necessary information for the FSM and its properties, which is used by the code to check the satisfiability of temporal logic properties associated with the transitions in the FSM.