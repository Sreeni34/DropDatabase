class Command_Struct:
    """ 
    Command_Struct stores information regarding a specific command
    and arguments entered by the user. 
    """

    def __init__(self, command):
        """
        Constructor that takes in name of command to create and
        initializes the command, name and list of attributes. In 
        the case of the command "createEdge", a list of dictionaries
        would also be used.
        """
        self.command = command
        self.name = ""
        self.attr = {}

        # Variable to hold list of dictionary of attributes
        # Specific to createEdge command
        self.attr_list = []


    def set_name(self, name):
        """
        Set the current object name. 

        @type name: String
        @param name: String representing name of Command Struct object
        """
        self.name = name


    def insert_attr(self, attr1, attr2):
        """
        Insert the attribute to dictionary containing
        list of attributes.

        @type attr1: String
        @param attr1: The key to add to dictionary
        @type attr2: String 
        @param attr2: The value to add to dictionary
        """
        self.attr[attr1] = attr2


    def insert_attr_list(self, ind):
        """
        Method adds the current attribute dictionary to list of 
        dictionaries at specified index location.

        @type ind: Integer
        @param ind: Index location to insert the dictionary into list
        """
        if (ind >= len(self.attr_list)):
            self.attr_list.append(self.attr)
        else:
            self.attr_list[ind] = self.attr


    def clear_attr(self):
        """
        Clears the attribute list.
        """
        self.attr = {}


    def get_command(self):
        """
        Returns the command of this object.

        @rtype: String
        @return: String representing command of object
        """
        return self.command


    def get_name(self):
        """
        Returns the name of the object if the object has one.
        "NO NAME" is supplied if none exits.

        @rtype: String 
        @return: String representing the name of object
        """
        return self.name


    def get_attr(self):
        """
        Returns the list of attributes for the command. Method 
        works for commands CREATE, MATCH, and RETURN.

        @rtype: dictionary
        @return: List of attributes in dictionary format
        """
        return self.attr


    def get_attr_list(self):
        """
        Returns the list of dictionaries that represents attributes.
        Method works for command CREATEEDGE.

        @rtype: List of dictionaries
        @return: List of dictionaries representing attributes for 
        createEdge command.
        """
        return self.attr_list


    def get_attr_size(self):
        """
        Returns the size of the attribute dictionary.

        @rtype: Integer
        @return: Integer representing size of dictionary.
        """
        return len(self.attr)


    def get_attr_list_size(self):
        """
        Returns the number of dictionaries in list.

        @rtype: Integer
        @return: Number of dictionaries in list.
        """
        return len(self.attr_list)


    def print_Class(self):
        print "Command: " + self.command
        print "Name: " + self.name
        print "Attributes: ",
        print self.attr
        
        if (self.command == "CREATEEDGE"):
            print "List of Attributes: ",
            print self.attr_list

