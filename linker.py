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
                print bcolors.OKBLUE + "Node " + str(node_num) + \
                " = " + str(node) + bcolors.ENDC   
                node_num += 1   

    def PrintNode_ids(self, node_ids):   
        """
        Prints a list of nodes.       

        @type nodes: List 
        @param nodes: Node tuples to be printed.     
        """   
        nodes = []
        for node_id in node_ids:   
            nodes.append((node_id, 
                self.query_evaluator.get_node_attrs(node_id)))   
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
                print bcolors.OKBLUE + "Edge " + str(edge_num) + " = " + \
                str(edge_tup) + bcolors.ENDC   
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
            self.gs.set_identifier(curr_id, 
                self.query_evaluator.add_node(curr_attrs))   

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

    def PredNodeFilters(self, nodes, keyvals):   
        """
        Checks that the specified predicate attribute is present in the   
        attributes of all of the nodes     

        @type nodes: List 
        @param nodes: List of nodes   
        @type keyvals: keyvals 
        @param keyvals: List of attribute names to check for   
        """  
        filtered_nodes = [] 
        for node in nodes:   
            allpreds = True    
            for keyval in keyvals:      
                if keyval not in node[1].keys():   
                    allpreds = False   
            if allpreds:   
                filtered_nodes.append(node)
        return filtered_nodes

    def getPredAttrs (self, predicates):   
        """
        Get the list of predicate attributes from the predicates list    

        @type predicates: List 
        @param nodes: List of predicate parsed objects     
        """   
        counter = 0
        PredAttrList = []
        for item in predicates:   
            if (counter) % 2 == 0:   
                PredAttrList.append(item[0])   
            counter += 1   
        return PredAttrList

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
                PredAttrs = self.getPredAttrs(predicates[0])
                prednodes = self.PredNodeFilters(nodes, PredAttrs)
                filtered_nodes = self.Filter_Preds(prednodes, predicates[0])
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
        """
        Filter nodes based on parsed predicate objects       

        @type node_ids: List
        @param node_ids: Nodes to filter   
        @type predicates: List
        @param pred_list: Parsed predicate objects to filter on    
        """   
        if len(predicates) < 2:
            return self.pred.filter(nodeids, predicates[0][0], 
                predicates[0][2], predicates[0][1])   
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
            return self.getFilteredNodes(nodeids, pred_list, bool_list)

    def getFilteredNodes(self, nodeids, pred_list, bool_list):   
        """
        Given a list of the predicate objects and a list of boolean arguments,   
        return the list of filtered nodes based on the predicates       

        @type node_ids: List
        @param node_ids: Nodes to filter   
        @type pred_list: List
        @param pred_list: Predicates to filer on
        @type bool_list: List
        @param bool_list: AND or OR strings to combine predicates  
        """   
        filtered_nodes = []  
        for x in range(len(pred_list) - 1):   
            if x == 0:   
                pred0 = pred_list[x]   
                pred1 = pred_list[x + 1]
                filter1 = self.pred.filter(nodeids, 
                    pred0[0], pred0[2], pred0[1]) 
                filter2 = self.pred.filter(nodeids, 
                    pred1[0], pred1[2], pred1[1])
                if bool_list[x] == 'AND':      
                    filtered_nodes = [val for val in filter1 if val in filter2]   
                elif bool_list[x] == 'OR':   
                    for fltr in filter2:   
                        if fltr not in filter1:
                            filter1.append(fltr)
                    filtered_nodes = filter1    
            else:   
                pred = pred_list[x + 1]   
                fltr = self.pred.filter(filtered_nodes, pred[0], 
                    pred[2], pred[1])   
                if bool_list[x] == 'AND':      
                    filtered_nodes = [val for val in filtered_nodes 
                    if val in fltr]   
                elif bool_list[x] == 'OR':   
                    filtered_nodes = list(set(filtered_nodes + fltr))
        return filtered_nodes   

    def TwoItemsFilter(self, item, preds):   
        nodes = self.query_evaluator.match_node(item[2])
        PredAttrs = self.getPredAttrs(preds)
        prednodes = self.PredNodeFilters(nodes, PredAttrs)
        filtered_nodes = self.Filter_Preds(prednodes, preds)   
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
                filtered_nodes = self.TwoItemsFilter(item1, predicates[0])   
            edges = self.query_evaluator.match_node_rel(item1[2], item2[2], 
                filtered_nodes)  
            self.gs.set_identifier(curr_id, edges)   
            self.PrintEdges(edges)   
        else:   
            filtered_nodes = None   
            if (predicates != []):   
                filtered_nodes = self.TwoItemsFilter(item2, predicates[0])      
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
        if (len(predicates) == 2):  
            filtered_nodes1 = self.TwoItemsFilter(item1, predicates[0])  
            filtered_nodes2 = self.TwoItemsFilter(item3, predicates[1])
        elif (len(predicates) == 1):   
            if (item1[1] == predicates[0][0][3]):   
                filtered_nodes1 = self.TwoItemsFilter(item1, predicates[0])   
            else:   
                filtered_nodes2 = self.TwoItemsFilter(item3, predicates[0]) 
        edges = self.query_evaluator.match_node_node_rel(item1[2], item3[2], 
            item2[2], filtered_nodes1, filtered_nodes2)   
        self.gs.set_identifier(item1[1], edges)
        self.PrintEdges(edges)   

    def getIdList(self, attribute_list):   
        """
        Gets the list of identifiers from the attribute list     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".  
        """ 
        counter = 0  
        IdList = []
        for item in attribute_list: 
            if (counter % 2) == 0:   
                IdList.append(item[1])  
            counter += 1 
        return IdList

    def getPredOrder(self, attribute_list, predicates):   
        """
        Calculates the order in which the predicates must be applied   
        to the nodes     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        @type predicates: List 
        @param predicates: List of parsed predicate objects  
        """   
        IdList = self.getIdList(attribute_list)   
        predIdList = []
        PredOrder = []
        for pred in predicates:   
            predIdList.append(pred[0][3])   
        for predId in predIdList:   
            PredOrder.append(IdList.index(predId))   
        return PredOrder


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
        predOrder = []     
        filtered_nodes = [None] * len(node_attr_list)
        if predicates != []:   
            predOrder = self.getPredOrder(attribute_list, predicates)  
            for x in predOrder:   
                nodes1 = self.query_evaluator.match_node(node_attr_list[x])   
                PredAttrs1 = self.getPredAttrs(predicates[0])
                prednodes1 = self.PredNodeFilters(nodes1, PredAttrs1)   
                filtered_nodes1 = self.Filter_Preds(prednodes1, predicates[0])
                filtered_nodes[x] = filtered_nodes1   
                predicates.pop(0)
        nodes = self.query_evaluator.multi_match(node_attr_list, 
            edge_attr_list, filtered_nodes)
        self.gs.set_identifier(attribute_list[0][1], nodes)      
        if nodes == None:   
             print bcolors.FAIL + "No matches found" + bcolors.ENDC  
        else:
            print bcolors.OKGREEN + "NODE MATCHES:" + bcolors.ENDC   
            node_num = 1
            for node in nodes:
                node_tup = (node[0], 
                    self.query_evaluator.get_node_attrs(node[0]))  
                print bcolors.OKBLUE + "Node " + str(node_num) + \
                " = " + str(node_tup) + bcolors.ENDC   
                node_num += 1      

    def GeneralMatch(self, attribute_list, predicates):   
        """
        Calls the corresponding match function to match a set of ndoes     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        @type predicates: List 
        @param predicates: List of parsed predicate objects  
        """   
        if (len(attribute_list) == 1):   
            self.MatchSingleItem(attribute_list, predicates)      
        elif(len(attribute_list) == 2):      
            self.MatchTwoItems(attribute_list, predicates)
        elif(len(attribute_list) == 3):   
            self.MatchThreeItems(attribute_list, predicates)  
        else:   
            self.MatchChain(attribute_list, predicates)   

    def ModifyNode(self, attribute_list, predicates):   
        """
        Modifies the specified nodes by either adding or removing attribtues     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        @type predicates: List 
        @param predicates: List of parsed predicate objects  
        """   
        nodes_modified = attribute_list[0]   
        attrs_changed = attribute_list[1]   
        modify_boolean = attribute_list[2]   
        self.query_evaluator.modify_node(nodes_modified[2], 
            attrs_changed[2], int ((modify_boolean[2])['val']))   

    def ModifyEdge(self, attribute_list, predicates):   
        """
        Modifies the specified edges by either adding or removing attribtues     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        @type predicates: List 
        @param predicates: List of parsed predicate objects  
        """   
        edges_modified = attribute_list[0]   
        attrs_changed = attribute_list[1]   
        modify_boolean = attribute_list[2]   
        self.query_evaluator.modify_rel(edges_modified[2], 
            attrs_changed[2], int ((modify_boolean[2])['val']))   

    def ReturnIdent(self, attribute_list):   
        """
        Returns the specified identifier     

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        """   
        for item in attribute_list:    
            print bcolors.OKBLUE + str(item[1]) + " = " \
            + str(self.gs.get_identifier(item[1])) + bcolors.ENDC   

    def HasPath(self, attribute_list):   
        """
        Checks if a path exists between two ndoes.      

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        """   
        item1 = attribute_list[0]   
        item2 = attribute_list[1]   
        nodes1 = self.query_evaluator.match(item1[2], None, None)   
        nodes2 = self.query_evaluator.match(item2[2], None, None)      
        for node1 in nodes1:   
            for node2 in nodes2:   
                if (self.query_evaluator.check_path(node1[0], node2[0])):   
                    print bcolors.OKBLUE + "A path exists between " \
                    + str(node1) + " and " + str(node2) + bcolors.ENDC   
                else:   
                    print bcolors.FAIL + "No path exists between " \
                    + str(node1) + " and " + str(node2) + bcolors.ENDC   

    def ShortestPath(self, attribute_list):   
        """
        Returns the shortest path between two nodes      

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        """   
        item1 = attribute_list[0]   
        item2 = attribute_list[1]   
        nodes1 = self.query_evaluator.match(item1[2], None, None)   
        nodes2 = self.query_evaluator.match(item2[2], None, None)   
        for node1 in nodes1:   
            for node2 in nodes2:   
                if (self.query_evaluator.check_path(node1[0], node2[0])):
                    path_list = self.query_evaluator.get_shortest_path\
                    (node1[0], node2[0])
                    print bcolors.OKGREEN \
                    + "The nodes in the path between " + str(node1) \
                    + " and " + str(node2) + " are: " + bcolors.ENDC    
                    for node_id in path_list:   
                        print bcolors.OKBLUE \
                        + str((node_id, 
                            self.query_evaluator.get_node_attrs\
                            (node_id))) + bcolors.ENDC     
                else:   
                    print bcolors.FAIL + "No path exists between " + \
                    str(node1)+ " and " + str(node2) + bcolors.ENDC   

    def getNeighbors(self, attribute_list):   
        """
        Get the neighbors of the specified nodes      

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        """   
        item1 = attribute_list[0]   
        nodes = self.query_evaluator.match(item1[2], None, None)   
        if nodes == None:   
            print bcolors.FAIL + "No Node matches found" + bcolors.ENDC   
        else:   
            print bcolors.OKGREEN + "NODE Neighbors:" + bcolors.ENDC   
            node_num = 1       
            for node1 in nodes:           
                neighbor_ids = self.query_evaluator.get_neighbors(node1[0])   
                if (neighbor_ids == []): 
                    print bcolors.FAIL + "Neighbors for Node " + \
                    str(node_num) + " = " + "No neighbors for Node(s)" + \
                    bcolors.ENDC   
                else:   
                    neighbors = []   
                    for neighbor_id in neighbor_ids:
                        neighbors.append((neighbor_id, 
                            self.query_evaluator.get_node_attrs(neighbor_id)))   
                    print bcolors.OKBLUE + "Neighbors for Node " + \
                    str(node_num) + " = " + str(neighbors) + bcolors.ENDC   
            node_num += 1   

    def HasEdge(self, attribute_list):   
        """
        Checks if a direct edge exists between two nodes      

        @type attribute_list: List 
        @param attribute_list: List of parsed objects, where each
        element is of the form "Type: Identifier dictionary_attributes".   
        """   
        item1 = attribute_list[0]   
        item2 = attribute_list[1]   
        nodes1 = self.query_evaluator.match(item1[2], None, None)   
        nodes2 = self.query_evaluator.match(item2[2], None, None)      
        for node1 in nodes1:   
            for node2 in nodes2:   
                if (self.query_evaluator.check_path(node1[0], node2[0])):   
                    print bcolors.OKBLUE + \
                    "A direct edge exists between " + str(node1) + \
                    " and " + str(node2) + bcolors.ENDC   
                else:   
                    print bcolors.FAIL + "No direct edge exists between " + \
                    str(node1) + " and " + str(node2) + bcolors.ENDC 

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
                self.GeneralMatch(attribute_list, predicates)
            elif command_name == "MODIFYNODE":   
                self.ModifyNode(attribute_list, predicates)    
            elif command_name == "MODIFYEDGE":   
                self.ModifyEdge(attribute_list, predicates)
            elif command_name == "DELETENODE":   
                node_deleted = attribute_list[0]   
                self.query_evaluator.delete_node(node_deleted[2])   
            elif command_name == "DELETEEDGE":   
                edge_deleted = attribute_list[0]   
                self.query_evaluator.delete_rel(edge_deleted[2])   
            elif command_name == "RETURN":  
                self.ReturnIdent(attribute_list)   
            elif command_name == "HASPATH":   
                self.HasPath(attribute_list)
            elif command_name == "CLEAR":   
                self.query_evaluator.clear()   
            elif command_name == "SHORTESTPATH":   
                self.ShortestPath(attribute_list)
            elif command_name == "SHOW":
                self.gs.display()
            elif command_name == "VISUALIZE":
                self.query_evaluator.create_visual()   
            elif command_name == "NEIGHBOR":
                self.getNeighbors(attribute_list)
            elif command_name == "HASEDGE":   
                self.HasEdge(attribute_list)