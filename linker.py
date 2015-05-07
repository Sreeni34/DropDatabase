from query_evaluator import QueryEvaluator

class Linker:
    """ A basic linker class. """

    def __init__(self, object_list, gs):
        """
        This class is the linker for microDB. It takes in a list of 
        Command_Struct objects that is generated by the parser, and a 
        GraphStructure object. 


        @type object_list: List of Command_Stuct objects
        @param object_list: List of packaged commands that should be 
        generated by the parser. 
        @type: gs: GraphStructure object
        @param gs: The current internal graph representation. 
        """

        self.list_objects = object_list;
        self.gs = gs
        self.query_evaluator = QueryEvaluator(gs)

    def execute(self):
        """
        Executes commands that were extracted by the parser. 
        """
        # iterate through objects returned by parser to execute queries
        for obj in self.list_objects:
            command_name = obj.get_command()
            attribute_list = obj.get_attr_list()
            if command_name == "CREATE":
                for node in attribute_list:
                    curr_id = node[1]   
                    curr_attrs = node[2]
                    self.gs.set_identifier(curr_id, self.query_evaluator.add_node(curr_attrs))   
            elif command_name == "CREATEEDGE":   
                counter = 0
                [nodes1_identifier, nodes1, edge_identifier, edge_attrs, 
                nodes1_identifier, nodes2] = [0]*6
                for item in attribute_list:
                    if ((counter % 3) == 0):   
                        nodes1 = self.query_evaluator.match_node(item[2])
                    elif ((counter % 2) == 1):
                        edge_identifier = item[1]
                        edge_attrs = item[2]   
                    elif((counter % 3) == 2):   
                        nodes2 = self.query_evaluator.match_node(item[2])   
                        for node1 in nodes1:
                            for node2 in nodes2:  
                                self.gs.set_identifier(edge_identifier, 
                                    self.query_evaluator.add_relationship(node1,
                                     node2, edge_attrs))
                    counter += 1   
            elif command_name == "MATCH":   
                if (len(attribute_list) == 1):   
                    item = attribute_list[0]   
                    if (item[0] == "n:"):   
                        nodes = self.query_evaluator.match(item[2], None, None)   
                        print nodes   
                    elif (item[0] == "e:"):   
                        edges = self.query_evaluator.match(None, None, item[2])   
                        for edge in edges:   
                            edge_tup = (self.query_evaluator.get_node_attrs(edge[0]), edge[2], self.query_evaluator.get_node_attrs(edge[1]))   
                            print(edge_tup)   
                elif(len(attribute_list) == 2):   
                    item1 = attribute_list[0]   
                    item2 = attribute_list[1]   
                    if (item1[0] == "n:"):   
                        edges = self.query_evaluator.match(None, item1[2], item2[2])   
                        for edge in edges:   
                            edge_tup = (self.query_evaluator.get_node_attrs(edge[0]), edge[2], self.query_evaluator.get_node_attrs(edge[1]))   
                    else:   
                        edges = self.query_evaluator.match(None, item2[2], item1[2])   
                        for edge in edges:   
                            edge_tup = (self.query_evaluator.get_node_attrs(edge[0]), edge[2], self.query_evaluator.get_node_attrs(edge[1]))   
                elif(len(attribute_list) == 3):   
                    item1 = attribute_list[0]   
                    item2 = attribute_list[1]   
                    item3 = attribute_list[2]   
                    edges = self.query_evaluator.match(item1[2], item3[2], item2[2])   
                        for edge in edges:   
                            edge_tup = (self.query_evaluator.get_node_attrs(edge[0]), edge[2], self.query_evaluator.get_node_attrs(edge[1]))   
                else:   
                    counter = 0   
                    node_attr_list = []   
                    edge_attr_list = []   
                    for item in attribute_list:   
                        if ((counter) % 2 == 0):   
                            node_attr_list.append(item[2])   
                        elif((counter) % 2 == 1):   
                            edge_attr_list.append(item[2])   
                    nodes = self.query_evaluator.multi_match(node_attr_list, edge_attr_list)   
                    if (nodes == None):   
                        print("No nodes exist")   
                    else:   
                        for node in nodes:   
                            print(node[0], self.query_evaluator.get_node_attrs(node[0]))      
            elif command_name == "MODIFYNODE":   
                nodes_modified = attribute_list[0]   
                attrs_changed = attribute_list[1]   
                modify_boolean = attribute_list[2]   
                self.query_evaluator(nodes_modified[2], attrs_changed[2], modify_boolean[2])   
                print("Updated Nodes: ")   
                print(self.query_evaluator.match_node(nodes_modified[2]))   
            elif command_name == "MODIFYEDGE":   
                edges_modified = attribute_list[0]   
                attrs_changed = attribute_list[1]   
                modify_boolean = attribute_list[2]   
                self.query_evaluator(eges_modified[2], attrs_changed[2], modify_boolean[2])   
                print("Updated Relationships: ")   
                print(self.query_evaluator.match_rel(edges_modified[2]))   
            elif command_name == "DELETENODE":   
                node_deleted = attribute_list[0]   
                self.query_evaluator.delete_node(node_deleted[2])   
            elif command_name == "DELETEEDGE":   
                edge_deleted = attribute_list[0]   
                self.query_evaluator.delete_rel(edge_deleted[2])   
            elif command_name == "RETURN":  
                for item in attribute_list:    
                    print (item[1] + " = " + str(self.gs.get_identifier(item[1])))   
            elif command_name == "HASPATH":   
                item1 = attribute_list[0]   
                item2 = attribute_list[1]   
                nodes1 = self.query_evaluator.match(item1[2], None, None)   
                nodes2 = self.query_evaluator.match(item2[2], None, None)      
                for node1 in nodes1:   
                    for node2 in nodes2:   
                        if (self.query_evaluator.check_path(node1[0], node2[0])):   
                            print("A path exists between " + node1 + " and " + node2)   
                        else:   
                            print("No path exists between " + node1 + " and " + node2)   
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
                            print ("The nodes in the path between " + node1 + " and " + node2 + " are: ")   
                            for node_id in path_list:   
                                print (node_id, self.query_evaluator.get_node_attrs(node_id))   
                        else:   
                            print("No path exists between " + node1 + " and " + node2)   
            



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

