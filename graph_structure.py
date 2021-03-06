import networkx as nx
from pprint import pprint

class GraphStructure:
    """
    Class represents the in memory directed graph structure of the graph database.
    It contains important information such as the internal graph library
    used by networkx and the starting point for the next unique id.
    """

    def __init__(self, start_id=0):
        """
        Initializes the internal graph representation and the unique 
        id according to the argument.

        @type start_id: Integer, default value is 0
        @param start_id: Staring unique id for in-memory graph structure
        """
        self.graph = nx.DiGraph()
        self.id = start_id
        # Internal dictionary to store variables and values
        self.identifier = {}

    def get_graph(self):
        """
        Returns the internal graph object used to store nodes and nodes.
        Allows the caller to modify the state of the graph structure.

        @rtype: Graph object
        @return: the internal graph object used for storing data
        """
        return self.graph

    def set_graph(self, graph):
        """
        Sets the internal graph object to the one provided by the arguments.

        @type graph: Graph
        @param graph: Graph used to set to the internal L{GraphStructure} object
        """
        self.graph = graph

    def get_id(self):
        """
        Returns unique id for graph nodes. If id is used, user must 
        increment it.

        @rtype: Integer
        @return: Id for the next graph node.
        """
        return self.id

    def set_id(self, num):
        """
        Sets the unique id to the argument num.

        @type num: Integer
        @param num: Next free id to store nodes
        """
        self.id = num

    def inc_id(self):
        """
        Increments unique id for graph nodes.
        """
        self.id += 1

    def print_nodes(self):
        """
        Prints all the nodes in the form (node id, node attributes).
        """
        print 'Nodes'
        pprint(self.graph.nodes(data=True))

    def print_edges(self):
        """
        Prints all the edges in the form (starting node id, ending node id,
        edge attributes)
        """
        print 'Edges'
        pprint(self.graph.edges(data=True))

    def print_id(self):
        """
        Prints the unique node id for the L{GraphStructure}.
        """
        print 'Unique node id: ' + str(self.id)

    def print_identifier_dict(self):
        """
        Prints the identifier dictionary.
        """
        print "Identifier"
        pprint(self.identifier)

    def set_identifier(self, id, val):
        """
        Stores the key : value pair id and val in the dictionary.

        @type id: String
        @param id: Key to insert in dictionary
        @type val: Anything
        @param val: Value for the given key 
        """
        self.identifier[id] = val

    def get_identifier(self, id):
        """
        Returns the value for the given key in the dictionary. If
        no key exists, we return None.

        @type id: String
        @param id: Key to look up in dictionary
        @rtype: Anything or None
        @return: Value for the key or None, if key is not present
        """
        if id in self.identifier:
            return self.identifier[id]
        return None   

    def delete_identifier(self, node):
        """
        Delete key for the given value in the dictionary. If
        no key exists, nothing happens.

        @type node: String
        @param node: Value to remove in the dictionary
        """
        for key_val in self.identifier.keys():
            if self.identifier[key_val] == node:   
                self.identifier.pop(key_val)    

    def clear_all(self):   
        self.id = 0
        # Internal dictionary to store variables and values
        self.identifier = {}
        self.graph = nx.DiGraph()

    def display(self):
        """
        Display the nodes and edges of the in-memory graph and also
        prints out the next unique node id.
        """
        self.print_id()
        self.print_nodes()
        self.print_edges()
        self.print_identifier_dict()

    
            








