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
        else if node1_attrs is None and node2_attrs is None:
            self.match_rel(rel_attrs)
        else if node1_attrs is None and rel_attrs is None:
            self.match_node(node2_attrs)
        else if node2_attrs is None and rel_attrs is None:
            self.match_node(node1_attrs)
        else if node1_attrs is None:
            self.match_node_rel(node2_attrs, rel_attrs)
        else if node2_attrs is None:
            self.match_node_rel(node1_attrs, rel_attrs)
        else if rel_attrs is None:
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
        the list of attributes. 

        @type node_attrs: dict
        @param node_attrs: All the attributes of the node, including the
                           label.
        """
        self.g.add_node(self.id, node_attrs)
        self.id += 1 
        return (self.id - 1, node_attrs)

    def add_relationship(self, node1, node2, edge_attrs):
        """ 
        Creates a relationship 

        @type node_attrs: dict
        @param node_attrs: All the attributes of the node, including the
                           label.
        """
        node1_id, node1_props = node1
        node2_id, node2_props = node2
        self.g.add_edge(node1_id, node2_id, edge_attrs)   
        return (node1_id, node2_id, edge_attrs)


    def match(self, node_attrs):
        nodes = []
        for node_id, node_attributes in self.g.nodes(data=True):   
            if all(item in node_attributes.items() for item in 
            node_attrs.items()):   
               nodes.append((node_id, node_attributes))
        return nodes


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


