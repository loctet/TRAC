import networkx as nx
import time
from itertools import product
import hashlib
from MiniTimer import MiniTimer

class FSMGraph(MiniTimer):

    def __init__(self, data, log = True, time_out = 0 ):
        """
        Initializes the FSM graph with given JSON data.

        :param data: A dictionary containing FSM definitions, including states and transitions.
        """
        self.data = data
        self.graph = nx.MultiDiGraph()  # Using MultiDiGraph to support multiple edges between the same nodes
        self._construct_graph()
        self.log = log
        self.visited_path_for_paticipant = {}
        self.time_out = time_out
        self.timed_out = False
        self.nb_path = 0
        
    def _construct_graph(self):
        """
        Constructs the graph based on the initial data provided.
        """
        # Add states as nodes
        for state in self.data['states']:
            self.graph.add_node(state)

        # Add transitions as edges with metadata
        for transition in self.data['transitions']:
            self._add_transition(transition)

    def _add_transition(self, transition):
        """
        Adds a transition to the graph as an edge with metadata.

        :param transition: A dictionary containing transition details.
        """
        # Define a unique key for each transition to distinguish between multiple edges between the same nodes
        transition_key = f"{transition['actionLabel']}_{time.time_ns()}"

        # Add the transition as an edge with all its data as attributes
        self.graph.add_edge(transition['from'], transition['to'], key=transition_key, **transition)

    def get_outgoing_transitions(self, state):
        """
        Returns all outgoing transitions from a given state.

        :param state: The state from which to get the outgoing transitions.
        :return: A list of dictionaries, each representing an outgoing transition with its metadata.
        """
        outgoing_transitions = []
        for _, v, data in self.graph.out_edges(state, data=True):
            outgoing_transitions.append(data)
        return outgoing_transitions
    
    from itertools import product

    def get_number_of_paths(self, target_state):
        """
        Lists all paths from the "_" state to a given target state, considering each transition separately.

        :param target_state: The target state to find paths to.
        :return: A list of all possible paths, considering each transition separately.
        """
        
        all_simple_paths = list(nx.all_simple_paths(self.graph, source="_", target=target_state))
        return len(all_simple_paths)
    
    def is_caller_introduced(self, transition):
        """
        Checks if the caller of a given transition is introduced in every path from the "_" state to the 
        'from' state of the transition or in the current transition.

        :param fsm_graph: An instance of the FSMGraph class.
        :param transition: A dictionary representing the transition to check.
        :return: True if the caller is introduced in every path or in the current transition, False otherwise.
        """
        self.start_time()
        self.nb_path = 1
        from_state = transition['from']
        caller = list(transition['caller'].keys())[0]  # Assuming there's a single caller for simplicity
        callerRoles = transition['caller'][caller]

        #self.list_all_paths("S8")
        
        # Check if the caller is introduced in the current transition 
        if len(callerRoles) == 0 and caller in transition['newParticipants']:
            return True
        if len(transition['newParticipants'].keys()) > 0 and all(item in transition['newParticipants'][list(transition['newParticipants'].keys())[0]] for item in callerRoles):
            return True

        hasched_path_caller = hashlib.md5(f"{caller}_{callerRoles[:]}_{from_state}".encode()).hexdigest()

        if hasched_path_caller in self.visited_path_for_paticipant:
            return self.visited_path_for_paticipant[hasched_path_caller]
        
        self.visited_path_for_paticipant[hasched_path_caller] = self.is_in_all_paths(from_state, caller, callerRoles)

        return self.visited_path_for_paticipant[hasched_path_caller]


    def is_in_all_paths(self, target_state, caller, callerRoles) :

        # Directly iterate over each simple path without collecting them all at once
        for path in nx.all_simple_paths(self.graph, source="_", target=target_state):
            self.nb_path += 1
            # Collect all transitions for each step in the path
            
            if  self.time_out > 0 and ((self.get_ellapsed_time() > self.time_out) or   self.timed_out):
                self.timed_out = True
                return False
            
            transitions = []
            for i in range(len(path) - 1):
                from_state = path[i]
                to_state = path[i + 1]
                transitions_at_step = list(self.graph.get_edge_data(from_state, to_state).values())
                transitions.append(transitions_at_step)
            # Compute all combinations of transitions for the path
            for transition_combination in product(*transitions):
                detailed_path = list(zip(path[:-1], path[1:], transition_combination))
                if not self.is_in_a_path(detailed_path, caller, callerRoles):
                    return False
    
        return True  # Caller was introduced in every path or in the current transition

    def is_in_a_path(self, path, caller, callerRoles):
        caller_introduced = False
        pathRoles = []
        steps = 0
        for _, _, transition_data in path:
            newParticipants = transition_data.get('newParticipants', {})
            callerTransition = list(transition_data['caller'].keys())[0]
            callerRolesTransition = transition_data['caller'][callerTransition]
            steps += 1
            pathRoles = pathRoles +[transition_data['newParticipants'][key][:] for key in list(newParticipants.keys())]

            if len(newParticipants) == 0 and len(callerRolesTransition) > 0 and all(item in pathRoles for item in callerRolesTransition):
                transition_data['newParticipants'][callerTransition] = callerRolesTransition
                newParticipants = transition_data.get('newParticipants', {})

            if len(callerRoles) == 0 and caller in newParticipants:
                caller_introduced = True
                break  # Caller is introduced in this path, no need to check further
            
            
            if len(newParticipants) > 0 and len(callerRoles) > 0 and all(item in [newParticipants[i] for i in list(newParticipants.keys())] for item in callerRoles) > 0:
                caller_introduced = True
                break  # Caller is introduced in this path, no need to check further 
            
        if not caller_introduced:
            if self.log:
                print(f"The Path : {self.printPathTrace(path)} do not contain the participant {caller} : {callerRoles[:]}") 
            return False  # Caller was not introduced in at least one path
    
        return True

    def printPathTrace(self, path):
        result = []
        for _, _, transition in path:
            result.append(f"{transition['from']}-{transition['actionLabel']}-{transition['to']}")
        
        return ">".join(result)