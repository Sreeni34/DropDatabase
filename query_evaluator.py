import networkx as nx

class Query_Evaluator:
    """
    Query_Evaluator performs evalution of graph query language.
    """

    def __init__(self):
        self.g = nx.Graph()
        self.id = 0


    def match(self, node_attrs):
        try:
            return self.g.node[node_val]
        except Exception, e:
            raise e

        return self.g.node[node_val]

    def add(self, node_attrs):
        """ 
        Creates a node with the following attributes and returns 
        the list of attributes. 

        @type node_attrs: dict
        @param node_attrs: All the attributes of the node, including the
                           label.
        """
        self.g.add_node(self.id, node_attrs)
        self.id += 1 




if __name__ == '__main__':
    q = Query_Evaluator()
    q.add(1)
    q.add(2)
    print q.g.nodes()
    print q.match(1)
    print "Adding node"


