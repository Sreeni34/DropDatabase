from query_evaluator import Query_Evaluator
class Linker:
    """ A basic linker class. """

    def __init__(self, object_list):
        self.list_objects = object_list;
        self.query_evaluator = Query_Evaluator()


    def print_object_list(self):
        for obj in self.list_objects:
            obj.print_Class()


    def link_object(self):
        curr_obj = self.list_objects[0]
        create_obj = self.query_evaluator.add_node(curr_obj.get_attr())
        print create_obj
