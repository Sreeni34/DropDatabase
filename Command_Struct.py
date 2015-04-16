class Command_Struct:
    """ 
    This class stores the name of the command and its arguments.
    It is used to help the parser.
    """

    def __init__(self, command):
        self.command = command
        self.name = ""
        self.attr = {}

    def set_name(self, name):
        self.name = name

    def insert_attr(self, attr1, attr2):
        self.attr[attr1] = attr2

    def get_command(self):
        return command

    def get_name(self):
        return self.name

    def get_attr(self):
        return self.attr;

    def print_Class(self):
        print "Command: " + self.command
        print "Name: " + self.name
        print "Attributes "
        print self.attr