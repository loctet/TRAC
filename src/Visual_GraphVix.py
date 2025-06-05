import json
from graphviz import Digraph


def generate_visual_fsm(json_file_path, output_file_path):
    output_file_path = output_file_path.replace(".png", "")
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract FSM details from the JSON data
    initial_state = data['initialState']
    final_states = data['finalStates']

    # Create a directed graph using Graphviz
    fsm_graph = Digraph('FSM', filename=output_file_path, format='png')

    # Add nodes and transitions to the graph
    for transition in data['transitions']:
        from_state = transition['from']
        to_state = transition['to']
        label = transition['actionLabel']

        # Add nodes and labeled edge to the graph
        fsm_graph.node(from_state, color='green' if from_state == initial_state else 'black')
        fsm_graph.node(to_state, color='red' if to_state in final_states else 'black')
        fsm_graph.edge(from_state, to_state, label=label)

    # Render the FSM diagram to a file
    fsm_graph.render()