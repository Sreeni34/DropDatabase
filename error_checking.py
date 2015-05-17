# # Create error class instance
        # errorCheck = ErrorChecking()
        # # If there are errors, don't create linker 
        # if (errorCheck.check_obj(parser.get_object_list())):
        #     return True

class Error_Checking:
    """
    Class that checks whether the commands entered by the 
    user has errors.
    """


    def __init__(self, obj_list):
        self.cmd_obj = obj_list
        self.print_command_objects()


    def check_commands(self):
        for cmd in self.cmd_obj:
            print cmd.get_command()
            if self.any_errors(cmd):
                print "WE HAVE AN ERROR"
                print cmd.get_command()
                return True
        print "No errors"
        return False


    def any_errors(self, command):
        cmd = command.get_command()
        nameList = command.get_names()
        attrList = command.get_attr_list()
        cmdBool = command.get_bool()

        # Start off with no errors
        err = 0

        if (cmd == "CREATE"):
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_edge_attr(attrList)

            print "good"
            print nameList
            print attrList
            return err


    def print_command_objects(self):
        for cmd in self.cmd_obj:
            cmd.print_Class()


    def changed_bool(self, boolVal):
        return boolVal != -1


    def not_empty_names(self, names):
        return (names != [])


    def has_edge_attr(self, attrList):
        for lst in attrList:
            if lst[0] == "e:":
                return True
        return False

    def has_node_attr(self, attrList):
        for lst in attrList:
            if lst[0] == "n:":
                return True
        return False