import json
import re
import networkx as nx
import matplotlib.pyplot as plt


def generate_fsm_graph(fsmTextJson):
    fsm = json.loads(fsmTextJson)

    states = fsm['states']
    initial_states = fsm['initialState']
    final_states = fsm['finalStates']
    transitions = fsm['transitions']

    # Create a directed graph
    graph = nx.DiGraph()

    # Add states as nodes
    for state in states:
        node_attributes = {}

        if state in initial_states:
            node_attributes['initial'] = True
        if state in final_states:
            node_attributes['final'] = True

        matches = re.findall(r"I(\d+)", state)
        if matches:
            node_attributes['external'] = True

        if state == "_":
            node_attributes['open'] = True

        if state not in initial_states and state not in final_states and 'external' not in node_attributes and 'open' not in node_attributes:
            node_attributes['normal'] = True
   
        graph.add_node(state, **node_attributes)

    # Add transitions as edges
    for transition in transitions:
        graph.add_edge(transition['from'], transition['to'], action=transition['actionLabel'])

    return graph

def draw_fsm_graph(graph):
    # Set node positions using Kamada-Kawai layout
    pos = nx.kamada_kawai_layout(graph)

    # Get node attributes for final and initial states
    final_states = [state for state, attrs in graph.nodes(data=True) if 'final' in attrs]
    initial_states = [state for state, attrs in graph.nodes(data=True) if 'initial' in attrs]
    normal_states = [state for state, attrs in graph.nodes(data=True) if 'normal' in attrs]
    external_states = [state for state, attrs in graph.nodes(data=True) if 'external' in attrs]
    init_states = [state for state, attrs in graph.nodes(data=True) if 'open' in attrs]

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=20, nodelist=init_states, node_color='white', edgecolors='white')
    nx.draw_networkx_nodes(graph, pos, node_size=500, nodelist=external_states, node_color='black', edgecolors='black')
    nx.draw_networkx_nodes(graph, pos, node_size=500, nodelist=final_states, node_color='red', edgecolors='black')
    nx.draw_networkx_nodes(graph, pos, node_size=500, nodelist=initial_states, node_color='green', edgecolors='black')
    nx.draw_networkx_nodes(graph, pos, node_size=500, nodelist=normal_states, node_color='#e5e7eb', edgecolors='black')

    # Draw edges
    nx.draw_networkx_edges(graph, pos, arrows=True, edge_color='black', connectionstyle="arc3,rad=0.1")

    # Draw labels
    labels = nx.get_edge_attributes(graph, 'action')
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    # Prevent edge overlap
    plt.tight_layout()

    # Display the graph
    plt.axis('off')
    plt.show()