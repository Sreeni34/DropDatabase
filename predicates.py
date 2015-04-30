class Predicates:   
    """
    Predicates contains the methods to perform filtering on node   
    attributes in the graph, such as counting number of nodes that have   
    an attribute less than a particular value.   
    """   

    def __init__(self, gs):   
        """
        Constructor takes a GraphStructure object as an argument and 
        stores its in-memory graph representation.
        """
        self.gs = gs
        self.g = gs.get_graph()   

    def less_than(self, key, value):

