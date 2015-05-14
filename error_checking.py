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
            if self.any_errors(cmd):
                print "WE HAVE AN ERROR"
                print cmd.get_command
                return True
        return False


    def any_errors(self, command):
        cmd = command.get_command()
        nameList = command.get_names()
        attrList = command.get_attr_list()
        cmdBool = command.get_bool()

        # Start off with no errors
        err = 0

        if (cmd == "CREATE"):
            err = unchanged_bool(cmdBool)

            print "good"
            print nameList
            print attrList
            return True

    def print_command_objects(self):
        for cmd in self.cmd_obj:
            cmd.print_Class()


    def unchanged_bool(self, boolVal):
        if (boolVal == -1):
            return True
        return False