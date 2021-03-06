class Command_Struct:
    """ 
    L{Command_Struct} stores information regarding a specific command
    and arguments entered by the user. 
    """

    def __init__(self, command):
        """
        Constructor that takes in name of command to create and
        initializes the command, name, boolean value(for special
        cases only) and list of attributes.
        """
        self.command = command
        self.name = []
        self.attr = [] 
        self.bool = -1

##
##  Methods for self.name
##

    def insert_name(self, name):
        """
        Inserts the current object name into list.

        @type name: String
        @param name: String representing name of L{Command_Struct} object
        """

        self.name.append(name)


    def get_names(self):
        """
        Returns a list containing the names specified in the
        commmand. 

        @rtype: List of String
        @return: List of names specified in command 
        """

        return self.name


    def get_names_size(self):
        """
        Returns the number of names specified in the command.

        @rtype: Integer
        @return: Integer representing the size of names in list.
        """

        return len(self.name)

    def fix_names(self):
        prevElem = self.name[0]
        newLst = []
        i = -1   # Counter for newLst last element
        prevIden = ""
        for elem in self.name:
            # First check if and is supplied
            if elem == "AND" or elem == "OR":
                # Append it to the previous list
                newLst[i].append(elem)
            elif prevIden != elem[3]:
                i += 1
                # Add new list item to lst
                newLst.insert(i, [elem])
                # Set a new identifier
                prevIden = elem[3]
            else:
                # Previous element contains same identifier
                # Add the element to the end of the last list
                newLst[i].append(elem)
        self.name = newLst

##
##  Methods for self.attr
##

    def insert_attr_type(self, attr_type):
        """
        Inserts the type which identifies whether the list of attributes
        belong to a node or an edge.

        @type attr_type: String
        @param attr_type: String representing the type of attributes
        """

        self.attr.append([attr_type, "", {}])


    def insert_attr_name(self, name):
        """
        Inserts the name which identifies the list of attributes.

        @type name: String
        @param name: String representing the name to identify attributes
        """

        last_idx = len(self.attr) - 1
        self.attr[last_idx][1] = name


    def insert_attr(self, attr1, attr2):
        """
        Inserts the attributes into the last element
        of the list.

        @type attr1: String
        @param attr1: String representing first half of an attribute
        @type attr2: String
        @param attr2: String representing second half of an attribute
        """

        last_idx = len(self.attr) - 1
        self.attr[last_idx][2][attr1] = attr2


    def get_attr_type(self):
        """
        This method returns the type of the last attribute
        entered into the list of list of types, names and dictionaries.

        @rtype: String
        @return: Type of last attribute
        """

        last_idx = len(self.attr) - 1
        return self.attr[last_idx][0]


    def get_attr_name(self):
        """
        This method returns the name of the last attribute
        entered into the list of list of types, names and dictionaries.

        @rtype: String
        @return: Name of last attribute
        """

        last_idx = len(self.attr) - 1
        return self.attr[last_idx][1]


    def get_attr_name_attrs(self):
        """
        This method returns the dictionary containing the list
        of attributes belonging to a certain name.

        @rtype: Dictionary
        @return: Dictionary of attributes related to the last identifier.
        """

        last_idx = len(self.attr) - 1
        return self.attr[last_idx][2]

    def get_attr_list(self):
        """
        This method returns the list which contains our type,
        identifier, and attributes. 

        @rtype: List
        @return: List of type, id, and attributes
        """
        return self.attr


##
##  Methods for self.bool
##

    def set_bool(self, bool_val):
        """
        This method updates the boolean value to the value
        specified by the user.

        @type bool_val: Boolean
        @param bool_val: Boolean value further used in query evaluator. 
        """

        self.bool = bool_val


    def get_bool(self):
        """
        This method returns the boolean value pertaining to 
        the specific command.

        @rtype: Boolean
        @return: Boolean value (-1 if none set)
        """

        return self.bool

##
##  Methods for self.command
##
    
    def get_command(self):
        """
        Returns the command of this object.

        @rtype: String
        @return: String representing command of object
        """

        return self.command


##
##  Methods to reset data values
##

    def clear_name(self):
        """
        Clears the name list.
        """
        self.name = []


    def clear_attr(self):
        """
        Clears the attribute list.
        """
        self.attr = []


##
##  Methods to print values
##

    def print_Class(self):
        """
        Prints information about the specific commands and
        its attributes.
        """
        print "Command: " + self.command
        print "Names: ", 
        print self.name
        print "Attributes: ",
        print self.attr
        print "Bool: ",
        print self.bool
        print
        

