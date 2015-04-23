import networkx as nx

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

    def get_graph(self):
        """
        Returns the internal graph object used to store nodes and nodes.
        Allows the caller to modify the state of the graph structure.

        @rtype: Graph object
        @return: the internal graph object used for storing data
        """
        return self.graph

    def get_id(self):
        """
        Returns unique id for graph nodes. If id is used, user must 
        increment it.

        @rtype: Integer
        @return: Id for the next graph node.
        """
        return self.id

    def inc_id(self):
        """
        Increments unique id for graph nodes.
        """
        self.id += 1

    def print_nodes(self):
        """
        Prints all the nodes in the form (node id, node attributes).
        """
        print self.graph.nodes(data=True)

    def print_edges(self):
        """
        Prints all the edges in the form (starting node id, ending node id,
            edge attributes)
        """
        print self.graph.edges(data=True)





