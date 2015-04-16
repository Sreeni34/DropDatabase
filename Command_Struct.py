class Command_Struct:
    """ 
    Command_Struct stores information regarding a specific command
    and arguments entered by the user. 
    """

    def __init__(self, command):
        self.command = command
        self.name = ""
        self.attr = {}

    def set_name(self, name):
        """
        Set the current object name. 
        """
        self.name = name

    def insert_attr(self, attr1, attr2):
        """
        Insert the attribute to dictionary containing
        list of attributes.
        """
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
        print "Attributes ",
        print self.attr