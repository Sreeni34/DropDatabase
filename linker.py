from query_evaluator import QueryEvaluator
from bcolors import bcolors
from predicates import Predicates

class Linker:
    """ A basic linker class. """

    """
    REL ATTR = e: a b:c
    ID ATTR = n: a a:b
    BOOL = b: a val:0/1
    ID = n: a () ()

    METHODS TO IMPLEMENT
    CREATE          ID ATTR ..
    CREATEEDGE      ID ATTR REL ATTR ID ATTR
    MATCH           ID ATTR REL ATTR ID ATTR REL ATTR ID ATTR ...
    MODIFYNODE      ID ATTR ID ATTR BOOL
    MODIFYEDGE      REL ATTR REL ATTR BOOL
    DELETENODE      ID ATTR
    DELETEEDGE      REL ATTR
    RETURN          ID ID ...
    HASPATH         ID ATTR ID ATTR
    CLEAR
    SHORTESTPATH    ID ATTR ID ATTR
    NEIGHBOR        ID ATTR
    HASEDGE         ID ATTR ID ATTR
    COMMONNEIGHBORS ID ATTR ID ATTR
    RESET
    FLUSH

    # EXTRA
    AGG             [id attr (<, >, =) id attr () val ...]

    METHODS IMPLEMENTED
    CREATE          ID ATTR ..
    CREATEEDGE      ID ATTR REL ATTR ID ATTR
    MATCH           ID ATTR REL ATTR ID ATTR REL ATTR ID ATTR ...
    MODIFYNODE      ID ATTR ID ATTR BOOL
    MODIFYEDGE      REL ATTR REL ATTR BOOL

    DELETENODE      ID ATTR
    DELETEEDGE      REL ATTR
    RETURN          ID ID ...
    HASPATH         ID ATTR ID ATTR
    CLEAR
    SHORTESTPATH    ID ATTR ID ATTR

    """




    def __init__(self, object_list, gs):
        """
        This class is the linker for microDB. It takes in a list of 
        L{Command_Struct} objects that is generated by the parser, and a 
        L{GraphStructure} object. 


        @type object_list: List of L{Command_Struct} objects
        @param object_list: List of packaged commands that should be 
        generated by the parser. 
        @type: gs: L{GraphStructure} object
        @param gs: The current internal graph representation. 
        """

        self.list_objects = object_list;
        self.gs = gs
        self.query_evaluator = QueryEvaluator(gs)   
        self.pred = Predicates(gs)   

    def PrintNodes(self, nodes):   
        """
        Prints a list of nodes.       

        @type nodes: List 
        @param nodes: Node tuples to be printed.     
        """   
        if nodes == []:   
            print bcolors.FAIL + "No matches found" + bcolors.ENDC
        else:
            print bcolors.OKGREEN + "NODE MATCHES:" + bcolors.ENDC   
            node_num = 1
            for node in nodes:  
                print bcolors.OKBLUE + "Node " + str(node_num) + " = " + str(node) + bcolors.ENDC   
                node_num += 1   

    def PrintNode_ids(self, node_ids):   
        """
        Prints a list of nodes.       

        @type nodes: List 
        @param nodes: Node tuples to be printed.     
        """   
        nodes = []
        for node_id in node_ids:   
            nodes.append((node_id, self.query_evaluator.get_node_attrs(node_id)))   
        self.PrintNodes(nodes)   

    def PrintEdges(self, edges):   
        """
        Prints a list of edges.       

        @type edges: List 
        @param edges: Edge tuples to be printed.     
        """   
        if edges == []:   
            print bcolors.FAIL + "No matches found" + bcolors.ENDC
        else:   
            print bcolors.OKGREEN + "EDGE MATCHES:" + bcolors.ENDC
            edge_num = 1   
            for edge in edges:   
                edge_tup = (self.query_evaluator.get_node_attrs(
                    edge[0]), edge[2], 
                    self.query_evaluator.get_node_attrs(edge[1]))   
                print bcolors.OKBLUE + "Edge " + str(edge_num) + " = " + str(edge_tup) + bcolors.ENDC   
                edge_num += 1         

    def CreateNode(self, attribute_list):   
        """
        Creates a node and sets the identifier to   
        refer to the created node using the passed   
        in parsed attribute list.    

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".  
        """   
        for node in attribute_list:
            curr_id = node[1]   
            curr_attrs = node[2]
            self.gs.set_identifier(curr_id, self.query_evaluator.add_node(curr_attrs))   

    def CreateEdge(self, attribute_list):   
        """
        Creates an edge between the specified nodes and with   
        the specified relationship attributes, all contained   
        in the parsed attribute list    

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".  
        """   
        counter = 0
        [nodes1_identifier, nodes1, edge_identifier, edge_attrs, 
        nodes1_identifier, nodes2] = [0]*6
        for item in attribute_list:
            if (counter % 3) == 0:   
                nodes1 = self.query_evaluator.match_node(item[2])
            elif (counter % 3) == 1:
                edge_identifier = item[1]
                edge_attrs = item[2]   
            elif (counter % 3) == 2:   
                nodes2 = self.query_evaluator.match_node(item[2]) 
                for node1 in nodes1:
                    for node2 in nodes2:  
                        self.query_evaluator.add_relationship(node1,
                             node2, edge_attrs)
            counter += 1   

    def MatchSingleItem(self, attribute_list, predicates):   
        """
        Matches a single item, either a node or a relationship, by   
        calling the appropriate query_evaluator method.   
        Then prints out the results of the match query     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        """   
        item = attribute_list[0] 
        curr_id = item[1]  
        if item[0] == "n:":   
            nodes = self.query_evaluator.match_node(item[2])   
            if (predicates != []):
                filtered_nodes = self.Filter_Preds(nodes, predicates[0])
                self.gs.set_identifier(curr_id, filtered_nodes)
                self.PrintNodes(filtered_nodes)   
            else:   
                self.gs.set_identifier(curr_id, nodes)
                self.PrintNodes(nodes)
        elif item[0] == "e:":      
            edges = self.query_evaluator.match(None, None, item[2])
            self.gs.set_identifier(curr_id, edges)   
            self.PrintEdges(edges)   

    def Filter_Preds(self, nodeids, predicates):   
        if len(predicates) < 2:
            return self.pred.filter(nodeids, predicates[0][0], predicates[0][2], predicates[0][1])   
        else:
            lenpred = len(predicates)
            counter = 0   
            pred_list = []   
            bool_list = []   
            for item in predicates: 
                if (counter) % 2 == 0:   
                    pred_list.append(item)   
                elif (counter) % 2 == 1:   
                    bool_list.append(item)   
                counter += 1   
            filtered_nodes = []  
            for x in range(len(pred_list) - 1):   
                if x == 0:   
                    pred0 = pred_list[x]   
                    pred1 = pred_list[x + 1]
                    filter1 = self.pred.filter(nodeids, pred0[0], pred0[2], pred0[1]) 
                    filter2 = self.pred.filter(nodeids, pred1[0], pred1[2], pred1[1])
                    if bool_list[x] == 'AND':      
                        filtered_nodes = [val for val in filter1 if val in filter2]   
                    elif bool_list[x] == 'OR':   
                        for fltr in filter2:   
                            if fltr not in filter1:
                                filter1.append(fltr)
                        filtered_nodes = filter1    
                else:   
                    pred = pred_list[x + 1]   
                    fltr = self.pred.filter(filtered_nodes, pred[0], pred[2], pred[1])   
                    if bool_list[x] == 'AND':      
                        filtered_nodes = [val for val in filtered_nodes if val in fltr]   
                    elif bool_list[x] == 'OR':   
                        filtered_nodes = list(set(filtered_nodes + fltr))   
            return filtered_nodes   

    def MatchTwoItems(self, attribute_list, predicates):   
        """
        Matches a pair of nodes and edges.     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".  
        """   
        item1 = attribute_list[0]   
        item2 = attribute_list[1]   
        curr_id = item1[1]
        if item1[0] == "n:":         
            filtered_nodes = None
            if (predicates != []):   
                nodes = self.query_evaluator.match_node(item1[2])
                filtered_nodes = self.Filter_Preds(nodes, predicates[0])   
            edges = self.query_evaluator.match_node_rel(item1[2], item2[2], 
                filtered_nodes)    
            self.gs.set_identifier(curr_id, edges)   
            self.PrintEdges(edges)   
        else:   
            filtered_nodes = None   
            if (predicates != []):   
                nodes = self.query_evaluator.match_node(item2[2])
                filtered_nodes = self.Filter_Preds(nodes, predicates[0])      
            edges = self.query_evaluator.match_node_rel(item2[2], item1[2], 
                filtered_nodes)
            self.gs.set_identifier(curr_id, edges)   
            self.PrintEdges(edges)   

    def MatchThreeItems(self, attribute_list, predicates):   
        """
        Matches a node, edge, node sequence in that order     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".  
        """   
        item1 = attribute_list[0]   
        item2 = attribute_list[1]   
        item3 = attribute_list[2]   
        filtered_nodes1 = None
        filtered_nodes2 = None   
        print predicates   
        if (len(predicates) == 2):  
            nodes1 = self.query_evaluator.match_node(item1[2]) 
            nodes2 = self.query_evaluator.match_node(item3[2])   
            if (item1[1] == predicates[0][0][3]):      
                filtered_nodes1 = self.Filter_Preds(nodes1, predicates[0])   
                filtered_nodes2 = self.Filter_Preds(nodes2, predicates[1])   
            else:   
                filtered_nodes1 = self.Filter_Preds(nodes1, predicates[1])   
                filtered_nodes2 = self.Filter_Preds(nodes2, predicates[0])   
        edges = self.query_evaluator.match_node_node_rel(item1[2], item3[2], 
            item2[2], filtered_nodes1, filtered_nodes2)   
        self.gs.set_identifier(item1[1], edges)
        self.PrintEdges(edges)   

    def MatchChain(self, attribute_list, predicates):   
        """
        Matches a chain of node, edge, node, edge, node...     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".  
        """   
        counter = 0   
        node_attr_list = []   
        edge_attr_list = []   
        for item in attribute_list:   
            if (counter) % 2 == 0:   
                node_attr_list.append(item[2])   
            elif (counter) % 2 == 1:   
                edge_attr_list.append(item[2])   
            counter += 1   
        nodes = self.query_evaluator.multi_match(node_attr_list, edge_attr_list)
        self.gs.set_identifier(attribute_list[0][1], nodes)
        if nodes == None:   
             print bcolors.FAIL + "No matches found" + bcolors.ENDC  
        for node in nodes:   
            print bcolors.OKGREEN + "NODE MATCHES:" + bcolors.ENDC   
            node_num = 1
            for node in nodes:
                node_tup = (node[0], self.query_evaluator.get_node_attrs(node[0]))  
                print bcolors.OKBLUE + "Node " + str(node_num) + " = " + str(node_tup) + bcolors.ENDC   
                node_num += 1      

    def execute(self):
        """
        Executes commands that were extracted by the parser. 
        """
        # iterate through objects returned by parser to execute queries
        for obj in self.list_objects:
            command_name = obj.get_command()
            attribute_list = obj.get_attr_list()   
            predicates = obj.get_names()
            if command_name == "CREATE":
                self.CreateNode(attribute_list)   
            elif command_name == "CREATEEDGE":   
                self.CreateEdge(attribute_list)   
            elif command_name == "MATCH":   
                if (len(attribute_list) == 1):   
                    self.MatchSingleItem(attribute_list, predicates)      
                elif(len(attribute_list) == 2):      
                    self.MatchTwoItems(attribute_list, predicates)
                elif(len(attribute_list) == 3):   
                    self.MatchThreeItems(attribute_list, predicates)  
                else:   
                    self.MatchChain(attribute_list, predicates)
            elif command_name == "MODIFYNODE":   
                nodes_modified = attribute_list[0]   
                attrs_changed = attribute_list[1]   
                modify_boolean = attribute_list[2]   
                self.query_evaluator.modify_node(nodes_modified[2], attrs_changed[2], int ((modify_boolean[2])['val']))     
            elif command_name == "MODIFYEDGE":   
                edges_modified = attribute_list[0]   
                attrs_changed = attribute_list[1]   
                modify_boolean = attribute_list[2]
                print "Boolean val"
                print (modify_boolean[2])['val']
                self.query_evaluator.modify_rel(edges_modified[2], attrs_changed[2], int ((modify_boolean[2])['val']))    
            elif command_name == "DELETENODE":   
                node_deleted = attribute_list[0]   
                self.query_evaluator.delete_node(node_deleted[2])   
            elif command_name == "DELETEEDGE":   
                edge_deleted = attribute_list[0]   
                self.query_evaluator.delete_rel(edge_deleted[2])   
            elif command_name == "RETURN":  
                for item in attribute_list:    
                    print bcolors.OKBLUE + str(item[1]) + " = " + str(self.gs.get_identifier(item[1])) + bcolors.ENDC   
            elif command_name == "HASPATH":   
                item1 = attribute_list[0]   
                item2 = attribute_list[1]   
                nodes1 = self.query_evaluator.match(item1[2], None, None)   
                nodes2 = self.query_evaluator.match(item2[2], None, None)      
                for node1 in nodes1:   
                    for node2 in nodes2:   
                        if (self.query_evaluator.check_path(node1[0], node2[0])):   
                            print("A path exists between " + str(node1) + " and " + str(node2))   
                        else:   
                            print("No path exists between " + str(node1) + " and " + str(node2))   
            elif command_name == "CLEAR":   
                self.query_evaluator.clear()   
            elif command_name == "SHORTESTPATH":   
                item1 = attribute_list[0]   
                item2 = attribute_list[1]   
                nodes1 = self.query_evaluator.match(item1[2], None, None)   
                nodes2 = self.query_evaluator.match(item2[2], None, None)   
                for node1 in nodes1:   
                    for node2 in nodes2:   
                        if (self.query_evaluator.check_path(node1[0], node2[0])):
                            path_list = self.query_evaluator.get_shortest_path(node1[0], node2[0])
                            print ("The nodes in the path between " + str(node1) + " and " + str(node2) + " are: ")   
                            for node_id in path_list:   
                                print (node_id, self.query_evaluator.get_node_attrs(node_id))   
                        else:   
                            print("No path exists between " + str(node1)+ " and " + str(node2))   
            elif command_name == "SHOW":
                self.gs.display()
            elif command_name == "VISUALIZE":
                self.query_evaluator.create_visual()   
            elif command_name == "NEIGHBOR":
                item1 = attribute_list[0]   
                nodes1 = self.query_evaluator.match(item1[2], None, None)   
                if nodes == None:   
                    print bcolors.FAIL + "No Node matches found" + bcolors.ENDC   
                else:   
                    print bcolors.OKGREEN + "NODE Neighbors:" + bcolors.ENDC   
                    node_num = 1       
                    for node1 in nodes1:           
                        neighbor_id = self.query_evaluator.get_neighbors(node1[0])   
                        if (neighbor_id == []): 
                            print bcolors.FAIL + "Neighbors for Node " + str(node_num) + " = " + "No neighbors for Node(s)" + bcolors.ENDC   
                        else:   
                            neighbors = []   
                            neighbors.append(neighbor_id, self.query_evaluator.get_node_attrs(neighbor_id))   
                            print bcolors.OKBLUE + "Neighbors for Node " + str(node_num) + " = " + neighbors + bcolors.ENDC   
                    node_num += 1
            elif command_name == "HASEDGE":   
                item1 = attribute_list[0]   
                item2 = attribute_list[1]   
                nodes1 = self.query_evaluator.match(item1[2], None, None)   
                nodes2 = self.query_evaluator.match(item2[2], None, None)      
                for node1 in nodes1:   
                    for node2 in nodes2:   
                        if (self.query_evaluator.check_path(node1[0], node2[0])):   
                            print bcolors.OKBLUE + "A direct edge exists between " + str(node1) + " and " + str(node2) + bcolors.ENDC   
                        else:   
                            print bcolors.FAIL + "No direct edge exists between " + str(node1) + " and " + str(node2) + bcolors.ENDC   
            elif command_name == "COMMONNEIGHBORS":   
                item1 = attribute_list[0]   
                item2 = attribute_list[1]   
                nodes1 = self.query_evaluator.match(item1[2], None, None)   
                nodes2 = self.query_evaluator.match(item2[2], None, None)   
                for node1 in nodes1:   
                    for node2 in nodes2:   
                        neighbor_iter = self.query_evaluator(node1[0], node2[0]) 
                        neighbors = []  
                        for x in neighbor_iter:   
                            neighbors.append((x, self.query_evaluator.get_node_attrs(x)))   
                        print bcolors.OKBLUE + "Common neighbors between " + str(node1) + " and " + str(node2) + " are " + str(neighbors) + bcolors.ENDC 




                # if command_name == "MATCH":   
                #     if len(attribute_list) == 1:   
                #         item = attribute_list[0]
                #         if item[0] == "n:":
                #             nodes = self.query_evaluator.match_node(item[2])   
                #             print nodes
                #         elif item[0] == "e:":   
                #             edges = self.query_evaluator.match_rel(item[2])   
                #             print edges   
                #     elif len(attribute_list) == 2:   
                #         item1 = attribute_list[0]   
                #         item2 = attribute_list[1]   
                #         if item1[0] == "n:":   
                #             edges = self.query_evaluator.match(None, items1[2], items2[2])   
                #             for edge in edges:   
                #                 print (self.query_evaluator.get_node_attrs(edge[0]), 
                #                     edge[2], self.query_evaluator.get_node_attrs(edge[1])   
                #         else:   
                              




            # elif obj.command.upper() == "MATCH":
            #     self.gs.set_identifier(cur_id, self.query_evaluator.match(obj.get_attr(), None, None))
            # elif obj.command.upper() == "RETURN":
            #     print "Return val: " + str(self.gs.get_identifier(cur_id))   
