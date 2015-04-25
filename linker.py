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
            cur_id = obj.get_name()
            if obj.command.upper() == "CREATE":
                self.gs.set_identifier(cur_id, self.query_evaluator.add_node(obj.get_attr()))
            elif obj.command.upper() == "MATCH":
                self.gs.set_identifier(cur_id, self.query_evaluator.match(obj.get_attr(), None, None))
            elif obj.command.upper() == "RETURN":
                print "Return val: " + str(self.gs.get_identifier(cur_id))



