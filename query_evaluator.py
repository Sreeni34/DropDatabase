from graph_structure import GraphStructure
import networkx as nx
from visualize_graph import VisualizeGraph

class QueryEvaluator:
    """
    L{QueryEvaluator} performs evalution of graph query language by 
    modifying the in-memory graph representation of a L{GraphStructure}
    object.
    """

    def __init__(self, gs):
        """
        Constructor takes a L{GraphStructure} object as an argument and 
        stores its in-memory graph representation.
        """
        self.gs = gs
        self.g = gs.get_graph()


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
        self.gs.inc_id()
        self.g.add_node(self.gs.get_id(), node_attrs)
        return (self.gs.get_id(), node_attrs)   

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
            
            self.gs.delete_identifier(node)      

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
        """ 
        Modifies the specified node by either adding or deleting the   
        attribute specified   

        @type node_attrs: Dictionary
        @param node_attrs: Node attributes to match and update   
        @type attr_change: Dictionary
        @param attr_change: Attributes to either add or delete   
        @type update_type: Boolean
        @param update_type: Specifies whether to add or delete an attribute.   
        True/1 means an attribute is being added and false/0 means an attribute   
        is being deleted.    
        @rtype: None
        @return: None           
        """   
        nodes = self.match_node(node_attrs)   
        for node1 in nodes:
            current_node_attrs = self.g.node[node1[0]] 
            if not update_type:   
                key_values = attr_change.keys()
                for key_val in key_values:   
                    current_node_attrs.pop(key_val)   
                self.g.node[node1[0]] = current_node_attrs   
            else:   
                attr_keys = attr_change.keys()
                for key_val in attr_keys:   
                    current_node_attrs[key_val] = attr_change[key_val]   
                self.g.node[node1[0]] = current_node_attrs   

    def modify_rel(self, rel_attrs, rel_change, update_type):   
        """ 
        Modifies the specified relationship by either adding or deleting the   
        attribute specified   

        @type rel_attrs: Dictionary
        @param rel_attrs: Relationship attributes to match and update   
        @type rel_change: Dictionary
        @param rel_change: Attributes to either add or delete   
        @type update_type: Boolean
        @param update_type: Specifies whether to add or delete an attribute.   
        True means an attribute is being added and false means an attribute   
        is being deleted   
        @rtype: None
        @return: None           
        """   
        edges = self.match_rel(rel_attrs)   
        for edge in edges:   
            current_edge_attrs = self.g[edge[0]][edge[1]]   
            if not update_type:   
                key_values = rel_change.keys()
                for key_val in key_values:   
                    current_edge_attrs.pop(key_val)   
                self.g[edge[0]][edge[1]] = current_edge_attrs   
            else:   
                attr_keys = rel_change.keys()
                for key_val in attr_keys:   
                    current_edge_attrs[key_val] = rel_change[key_val]   
                self.g[edge[0]][edge[1]] = current_edge_attrs   

    def set_rel_attrs(self, node1_id, node2_id, rel_attrs):   
        """ 
        Sets the edge with the specified node1_id and node2_id with the   
        specified relationship attribtues    

        @type node1_id: Integer
        @param node1_id: The first node of the edge   
        @type node2_id: Integer
        @param node2_id: The second node of the edge   
        @type rel_attrs: Dictionary         
        @param rel_attrs: Relationship attrubtes to set the edge attributes to    
        @rtype: None
        @return: None           
        """   
        self.g[node1_id][node2_id] = rel_attrs  

    def get_rel_attrs(self, node1_id, node2_id):   
        """ 
        Get the relationship attributes from the edge (node1_id, node2_id)    

        @type node1_id: Integer
        @param node1_id: The first node of the edge   
        @type node2_id: Integer
        @param node2_id: The second node of the edge   
        @rtype: Dictionary
        @return: Relationship attributes of the edge (node1_id, node2_id)           
        """   
        return self.g[node1_id][node2_id]

    def get_node_attrs(self, node_id):   
        """ 
        Get the node_id node attribtues 

        @type node_id: Integer
        @param node_id: The node id    
        @rtype: Dictionary
        @return: Node attributes of the node with id node_id           
        """   
        return self.g.node[node_id]


    def set_node_attrs(self, node_id, node_attributes):   
        """ 
        Set the attribtues of node_id with the specified node attribtues 

        @type node_id: Integer
        @param node_id: The node id  
        @type node_attributes: Dictionary         
        @param node_attributes: Node attributes to be set  
        @rtype: None
        @return: None           
        """   
        self.g.node[node_id] = node_attributes

    def consolidate(self, edge_list):   
        """ 
        Consolidates the connected nodes in the edge_list by checking if   
        there are common nodes in the edge tuples 

        @type edge_list: Dictionary
        @param edge_list: Dictionary containing lists of edge 
        tuples to consolidate  
        @rtype: Dictionary
        @return: Consolidated dictionary of lists of edge tuples.            
        """      
        i = 0
        consolidated_list = {}
        consolidated_nodes = []
        for x in range(len(edge_list) - 1):
            nodes1 = edge_list[x]
            nodes2 = edge_list[x + 1]
            for node1 in nodes1:
                for node2 in nodes2:   
                    if (node1[1] == node2[0]):   
                        consolidated_nodes.append((node1[0], node2[1]))   
            if (not consolidated_nodes):   
                return None   
            consolidated_list[i] = consolidated_nodes
            i += 1
        return consolidated_list
    
    def multi_match(self, node_attr_list, rel_attr_list):   
        """ 
        Determines if there is a chain of nodes described by the node_attr_list   
        and rel_attr_list in the graph. Then returns the first and last node   
        of this chain.    

        @type node_attr_list: List of node attributes   
        @param node_attr_list: List of node attributes to match the nodes in 
        the desired chain.   
        @type rel_attr_list: List of relationship attributes   
        @param rel_attr_list: List of relationship attributes to match 
        the edes in the chain    
        @rtype: Dictionary
        @return: The first and last node of the chain found or None if no   
        chain exists with the specified node attributes and   
        the relationship attributes             
        """   
        i = 0   
        edge_list = {}   
        for x in range(len(node_attr_list) - 1):   
            edges = self.match(node_attr_list[x], node_attr_list[x + 1], rel_attr_list[x])   
            # Break out if no match exists between the nodes and relationship
            if edges == []:
                edge_list = {}
                break
            edge_list[i] = edges   
            i += 1

        # Return none if no match was found
        if edge_list == {}:
            return None

        while (len(edge_list) != 1):   
            edge_list = self.consolidate(edge_list)   
            if (edge_list == {}):   
                return None
                
        return (edge_list[0])   

    def check_path(self, source_id, target_id):   
        """ 
        Determines if a path exists between two nodes. 

        @type source_id: Integer   
        @param source_id: Id of the source node     
        @type target_id: Integer   
        @param target_id: Id of the target node   
        @rtype: Boolean
        @return: Returns true if a path exists between the source and target   
        node in the graph. Otherwise, returns false.                
        """   
        return nx.has_path(self.g, source_id, target_id)   

    def get_shortest_path(self, source_id, target_id):   
        """ 
        Get the shortest path between two nodes 

        @type source_id: Integer   
        @param source_id: Id of the source node     
        @type target_id: Integer   
        @param target_id: Id of the target node   
        @rtype: Array
        @return: Array of nodes in the path between the source and target node                   
        """   
        return nx.shortest_path(self.g, source_id, target_id)   

    def get_neighbors(self, node_id):   
        """ 
        Get all of the neighbors of a node

        @type node_id: Integer   
        @param node_id: Id of the node to find neighbors of     
        @rtype: Array
        @return: Array of neighbors' node_ids                      
        """   
        return self.g.neighbors(node_id)   

    def get_common_neighbors(self, node1_id, node2_id):   
        """ 
        Get the common neighbors of two nodes

        @type node1_id: Integer   
        @param node1_id: Id of the first node   
        @type node2_id: Integer   
        @param node2_id: Id of the second node     
        @rtype: iterator
        @return: iterator of the common neighbors of u and v in the graph                      
        """   
        return nx.common_neighbors(self.g, node1_id, node2_id)   

    def clear(self):   
        """ 
        Clear the graph of all nodes and edges
                      
        """   
        self.gs.clear_all()

    def is_connected(self, node1_id, node2_id):   
        """ 
        Check if two nodes are connected in the graph.   
        
        @type node1_id: Integer   
        @param node1_id: Id of the first node   
        @type node2_id: Integer   
        @param node2_id: Id of the second node     
        @rtype: Boolean
        @return: True if an edge exists between the nodes, false otherwise                 
        """   
        return self.g.has_edge(node1_id, node2_id)           

    def create_visual(self):
        """
        Creates a diagram that represents the nodes and
        edges of our graph database.
        """
        # Set up visual
        newVis = VisualizeGraph(self.gs)
        newVis.draw_graph()
            
        



if __name__ == '__main__':
    gs = GraphStructure()
    # q = QueryEvaluator()
    # node = q.add_node({'Label' : 'Person', 'Name' : 'You'})
    # node2 = q.add_node({'Label' : 'Person', 'Name' : 'Sreeni'})
    # node3 = q.add_node({'Label' : 'Alien', 'Gender' : 'Unknown'})
    # node4 = q.add_node({'Label' : 'neo:Database:NoSql:Graph', 'Name' : 'SARS Database'})
    # LIKE_rel = q.add_relationship(node, node4, {'rel' : 'LIKES', 'rel' : 'boss'})   
    # print node
    # print node4
    # print LIKE_rel
    # print q.g.nodes(data=True)
    # print q.g.edges(data=True)
    # print q.match({'Label' : 'Person'}, None, None)
    # print q.match(None, None, {'Rel_Type' : 'LIKES'})   
    # q.set_rel_attrs(node[0], node4[0], {'Rel_Type' : 'LOVES'}) 
    # print q.get_rel_attrs(node[0], node4[0])  
    #print q.g.node[node[0]]   
    q = QueryEvaluator(gs)
    node = q.add_node({'Label' : 'Person', 'Name' : 'You'})
    node2 = q.add_node({'Label' : 'Person', 'Name' : 'Sreeni'})   
    node3 = q.add_node({'Label' : 'Alien', 'Gender' : 'Unknown'})
    node4 = q.add_node({'Label' : 'neo:Database:NoSql:Graph', 'Name' : 'SARS Database'})
    LIKE_rel = q.add_relationship(node, node4, {'rel' : 'LIKES'})
    owner_rel = q.add_relationship(node4, node3, {'rel' : 'OWNER'})   
    #LIKE_rel2 = q.add_relationship(node2, node4, {'rel' : 'LIKES'})   
    node_attr_list = [{'Label' : 'Person'}, {'Label' : 'neo:Database:NoSql:Graph'}, {'Label' : 'Alien'}]   
    rel_attr_list = [{'rel' : 'LIKES'}, {'rel' : 'OWNER'}]
    node_matches = q.multi_match(node_attr_list, rel_attr_list)
    #print nx.has_path(gs.get_graph(), node2[0], node3[0])
    #print nx.shortest_path(gs.get_graph(), node[0], node3[0])   
    #print nx.all_neighbors(gs.get_graph(), node[0])
    q.clear()
    print gs.get_graph().nodes()
    #print node_matches


