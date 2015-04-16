import networkx as nx

class Query_Evaluator:
    """
    Query_Evaluator performs evalution of graph query language.
    """

    def __init__(self):
        self.g = nx.DiGraph()
        self.id = 0

    def match(self, node1_attrs, node2_attrs, rel_attrs):   
        """ 
        Matches the specified node attributes and and relationship by calling   
        the appropriate match function. Returns a list of tuples of node(s)   
        and/or relationships that were matched

        @type node1_attrs: Dictionary
        @param node1_attrs: Node 1 attributes to match
        @type node2_attrs: Dictionary
        @param node2_attrs: Node 2 attributes to match
        @type rel_attrs: Dictionary
        @param rel_attrs: Relationship attributes to match
        @rtype: list of tuples
        @return: list of tuples containing node attributes and/or relationship   
        attributes depending on the match function called.         
        """

        result = []  
        if node1_attrs is None and node2_attrs is None and rel_attrs is None:   
            assert("Must specify either nodes or relationship")
        elif node1_attrs is None and node2_attrs is None:
            result = self.match_rel(rel_attrs)
        elif node1_attrs is None and rel_attrs is None:
            result = self.match_node(node2_attrs)
        elif node2_attrs is None and rel_attrs is None:
            result = self.match_node(node1_attrs)
        elif node1_attrs is None:
            result = self.match_node_rel(node2_attrs, rel_attrs)
        elif node2_attrs is None:
            result = self.match_node_rel(node1_attrs, rel_attrs)
        elif rel_attrs is None:
            result = self.match_find_rel(node1_attrs, node2_attrs)
        else:
            result = self.match_node_node_rel(node1_attrs, node2_attrs, rel_attrs)  
        return result

    def match_find_rel(self, node1_attrs, node2_attrs):   
        """ 
        Finds the relationships that connect the nodes with the specified   
        node attributes   

        @type node1_attrs: Dictionary
        @param node1_attrs: Node 1 attributes to match
        @type node2_attrs: Dictionary
        @param node2_attrs: Node 2 attributes to match
        @rtype: list of tuples
        @return: Edge tuples in the format (node1_id, node2_id, edge_attributes)       
        """   
        return self.match_node_node_rel(node1_attrs, node2_attrs, {})   


    def match_node_rel(self, node_attrs, rel_attrs):   
        """ 
        Finds the nodes that have relationships with nodes that have the   
        specified node attributes

        @type node_attrs: Dictionary
        @param node_attrs: Node attributes to match
        @type rel_attrs: Dictionary
        @param rel_attrs: Relationship attributes to match
        @rtype: list of tuples
        @return: Edge tuples in the format (node1_id, node2_id, edge_attributes)        
        """   
        return self.match_node_node_rel(node_attrs, {}, rel_attrs)

    def match_node_node_rel(self, node1_attrs, node2_attrs, rel_attrs):   
        """ 
        Finds the nodes that have relationships with both nodes that have the   
        specified node 1 and node 2 attributes, respectively      

        @type node1_attrs: Dictionary
        @param node1_attrs: Node 1 attributes to match   
        @type node2_attrs: Dictionary
        @param node2_attrs: Node 2 attributes to match
        @type rel_attrs: Dictionary
        @param rel_attrs: Relationship attributes to match
        @rtype: list of tuples
        @return: Edge tuples in the format (node1_id, node2_id, edge_attributes)        
        """   

        nodes1 = self.match_node(node1_attrs)   
        edges = self.match_rel(rel_attrs)   
        node_rels = []
        for node in nodes1:
            # Finds all neighbors of node satisfying node 2 attributes
            neighbors = self.filter_nodes(self.g.neighbors(node[0]), node2_attrs)
            for node2_id in neighbors:
                # Iterates through out edges of first node
                out_edges = self.g.out_edges(node[0], data=True)
                for edge in edges:   
                    if edge in out_edges and node2_id in edge:   
                        node_rels.append(edge)   

        return node_rels

    def filter_nodes(self, node_id_lst, node_attrs):
        """
        Helper function that takes a list of node ids and returns
        a filtered list of nodes that contain the attributes.

        @type node_id_lst: List
        @param node_id_lst: List of node id
        @type node_attrs: Dictionary
        @param node_attrs: Attributes used to filter node
        @rtype: List
        @return: List of nodes that contain the attributes
        """
        ret = []
        for n in node_id_lst:
            if all(item in self.g.node[n].items() for item in node_attrs.items()):
                ret.append(n)
        return ret

    def match_rel(self, rel_attrs):   
        """ 
        Finds the relationships that have the specified relationship attributes   

        @type rel_attrs: Dictionary
        @param rel_attrs: Relationship attributes to match
        @rtype: list of tuples
        @return: Edge tuples in the format (node1_id, node2_id, edge_attributes)           
        """   
        edges = []   
        for node1_id, node2_id, edge_attributes in self.g.edges(data=True):   
            if all(item in edge_attributes.items() for item in rel_attrs.items()):
                edges.append((node1_id, node2_id, edge_attributes))
        return edges       
    
    def match_node(self, node_attrs):   
        """ 
        Find the nodes that have the specified node attributes      

        @type node_attrs: Dictionary
        @param node_attrs: Node attributes to match
        @rtype: list of tuples
        @return: Node tuples of the format (node_id, node_attributes)              
        """
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

    def delete_node(self, node_attrs):   
        """ 
        Deletes the nodes containing the specified node attributes and all of   
        their associated edges

        @type node_attrs: dict
        @param node_attrs: All the attributes of the node.
        @rtype: None
        @return: None
        """   
        nodes = self.match_node(node_attrs)   
        for node in nodes:   
            self.g.remove_node(node[0])      

    def delete_rel(self, rel_attrs):   
        """ 
        Finds the relationships that have the specified relationship attributes
        and deleted them   

        @type rel_attrs: Dictionary
        @param rel_attrs: Relationship attributes to match and delete
        @rtype: None
        @return: None           
        """

        edges = self.match_rel(rel_attrs)
        for edge in edges:
            self.g.remove_edge(edge[0], edge[1])   

    def modify_node(self, node_attrs, attr_change, update_type):   
        nodes = self.match_node(node_attrs)   
        for node in nodes:   
            current_node_attrs = self.g.get_node_attributes(node[0])   
            if (!update_type):   
                key_values = attr_change.keys()
                for key_val in key_values:   
                    current_node_attrs.pop(key_val)   
                self.g.set_node_attributes(node[0], current_node_attrs)   
            else:   
                attr_keys = attr_change.keys()
                for key_val in attr_keys:   
                    current_node_attrs[key_val] = attr_keys[key_val]   
                self.g.set_node_attributes(node[0], current_node_attrs)   

    def modify_relationship(self, rel_attrs, rel_change, update_type):   
        edges = self.match_rel(rel_attrs)   
        for edge in edges:   
            current_edge_attrs = self.g[edge[0]][edge[1]]   
            if (!update_type):   
                key_values = rel_change.keys()
                for key_val in key_values:   
                    current_edge_attrs.pop(key_val)   
                self.g[edge[0]][edge[1]] = current_edge_attrs   
            else:   
                attr_keys = rel_change.keys()
                for key_val in attr_keys:   
                    current_edge_attrs[key_val] = attr_keys[key_val]   
                self.g[edge[0]][edge[1]] = current_edge_attrs





if __name__ == '__main__':

    q = Query_Evaluator()
    # node = q.add_node({'Label' : 'Person', 'Name' : 'You'})
    # # node2 = q.add_node({'Label' : 'Person', 'Name' : 'Sreeni'})
    # # node3 = q.add_node({'Label' : 'Alien', 'Gender' : 'Unknown'})
    # node4 = q.add_node({'Label' : 'neo:Database:NoSql:Graph', 'Name' : 'SARS Database'})
    # LIKE_rel = q.add_relationship(node, node4, {'Rel_Type' : 'LIKES'})   
    # print node
    # print node4
    # print LIKE_rel
    # print q.g.nodes(data=True)
    # print q.g.edges(data=True)
    # print q.match({'Label' : 'Person'}, None, None)
    # print q.match(None, None, {'Rel_Type' : 'LIKES'})   


