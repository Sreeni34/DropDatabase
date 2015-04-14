import networkx as nx

class Query_Evaluator:
    """
    Query_Evaluator performs evalution of graph query language.
    """

    def __init__(self):
        self.g = nx.Graph()
        self.id = 0


    def match (self, node1_attrs, node2_attrs, rel_attrs):   
        if node1_attrs is None and node2_attrs is None and rel_attrs is None:   
            assert("Must specify either nodes or relationship")
        elif node1_attrs is None and node2_attrs is None:
            self.match_rel(rel_attrs)
        elif node1_attrs is None and rel_attrs is None:
            self.match_node(node2_attrs)
        elif node2_attrs is None and rel_attrs is None:
            self.match_node(node1_attrs)
        elif node1_attrs is None:
            self.match_node_rel(node2_attrs, rel_attrs)
        elif node2_attrs is None:
            self.match_node_rel(node1_attrs, rel_attrs)
        elif rel_attrs is None:
            self.match_find_rel(node1_attrs, node2_attrs)
        else:
            self.match_node_node_rel(node1_attrs, node2_attrs, rel_attrs)

    
    def match_node(self, node_attrs):
        nodes = []
        for node_id, node_attributes in self.g.nodes(data=True):   
            if all(item in node_attributes.items() for item in 
            node_attrs.items()):   
               nodes.append((node_id, node_attributes))
        return nodes


    def add_node(self, node_attrs):
        """ 
        Creates a node with the following attributes and returns 
        a tuple representing the node id and a list of attributes. 

        @type node_attrs: dict
        @param node_attrs: All the attributes of the node, including the
                           label.
        @rtype: tuple
        @return: a number representing the created node's unique id and 
                a list of attributes.
        """
        self.id += 1 
        self.g.add_node(self.id, node_attrs)
        return (self.id, node_attrs)

    def add_relationship(self, node1, node2, edge_attrs):
        """ 
        Creates a relationship between node1 and node2 defined by the
        edges attributes and returns a tuple containing both the nodes
        and the created edges attributes.

        @type node1: tuple
        @param node1: Starting node for edge
        @type node2: tuple
        @param node2: Ending node for edge
        @type edge_attrs: dict
        @param edge_attrs: All the attributes of the edge.
        @rtype: tuple
        @return: tuple in the format (starting node id, ending node id, edge 
                attributes).
        """
        node1_id, node1_props = node1
        node2_id, node2_props = node2
        self.g.add_edge(node1_id, node2_id, edge_attrs)   
        return (node1_id, node2_id, edge_attrs)



if __name__ == '__main__':
    q = Query_Evaluator()
    node = q.add_node({'Label' : 'Person', 'Name' : 'You'})
    # node2 = q.add_node({'Label' : 'Person', 'Name' : 'Sreeni'})
    # node3 = q.add_node({'Label' : 'Alien', 'Gender' : 'Unknown'})
    node4 = q.add_node({'Label' : 'neo:Database:NoSql:Graph', 'Name' : 'SARS Database'})
    LIKE_rel = q.add_relationship(node, node4, {'Rel_Type' : 'LIKES'})   
    print node
    print node4
    print LIKE_rel
    print q.g.nodes(data=True)
    print q.g.edges(data=True)
    # print q.match({'Label' : 'Person'})   


