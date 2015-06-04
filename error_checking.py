class Error_Checking:
    """
    Class that checks whether the commands entered by the 
    user has errors.
    """


    def __init__(self, obj_list):
        """
        Constructor takes in an object list to check for errors.
        """
        self.cmd_obj = obj_list
        self.print_command_objects()


    def check_commands(self):
        """
        Go through each command check if there are any errors. If there
        is an error return True, otherwise return False.
        """
        for cmd in self.cmd_obj:
            #print cmd.get_command()
            if self.any_errors(cmd):
                print "ERROR in command " + cmd.get_command()
                return True
        print "No errors"
        return False


    def any_errors(self, command):
        """
        Given a specific command as an argument, check if it first matches
        any of the already present commands and within each command, check
        if there is an error in the attributes, lists, or boolean values. If
        there is an error, return True, else return False.
        """
        cmd = command.get_command()
        nameList = command.get_names()
        attrList = command.get_attr_list()
        cmdBool = command.get_bool()

        # Start off with no errors
        err = False

        if (cmd == "CREATE"):
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_edge_attr(attrList) or self.has_bool_attr(attrList)

        elif cmd == "CREATEEDGE":
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_bool_attr(attrList) or (not self.last_node(attrList))

        elif cmd == "MATCH":
            err = self.changed_bool(cmdBool) or self.has_bool_attr(attrList)

        elif cmd == "MODIFYNODE":
            err = (not self.changed_bool(cmdBool)) or self.not_empty_names(nameList) \
                    or self.has_edge_attr(attrList) or self.not_length(attrList, 3) \
                    or (not self.last_bool(attrList)) or (not self.all_node_last(attrList))

        elif cmd == "MODIFYEDGE":
            err = (not self.changed_bool(cmdBool)) or self.not_empty_names(nameList) \
                    or self.has_node_attr(attrList) or self.not_length(attrList, 3) \
                    or (not self.last_bool(attrList)) or (not self.all_edge_last(attrList))

        elif cmd == "DELETENODE":
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_bool_attr(attrList) or self.has_edge_attr(attrList) \
                    or self.not_length(attrList, 1)

        elif cmd == "DELETEEDGE":
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_bool_attr(attrList) or self.has_node_attr(attrList) \
                    or self.not_length(attrList, 1)

        elif cmd == "RETURN":
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_bool_attr(attrList) or self.has_edge_attr(attrList) \
                    or (not self.only_id)

        elif cmd == "HASPATH":
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_bool_attr(attrList) or self.has_edge_attr(attrList) \
                    or self.not_length(attrList, 2) or (not self.two_nodes(attrList))

        elif cmd == "CLEAR":
            err = self.not_empty(attrList)

        elif cmd == "SHORTESTPATH":
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_bool_attr(attrList) or self.has_edge_attr(attrList) \
                    or self.not_length(attrList, 2) or (not self.two_nodes(attrList))

        elif cmd == "NEIGHBOR":
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_bool_attr(attrList) or self.has_edge_attr(attrList) \
                    or self.not_length(attrList, 1)

        elif cmd == "HASEDGE":
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_bool_attr(attrList) or self.has_edge_attr(attrList) \
                    or self.not_length(attrList, 2) or (not self.two_nodes(attrList))

        elif cmd == "COMMONNEIGHBORS":
            err = self.changed_bool(cmdBool) or self.not_empty_names(nameList) \
                    or self.has_bool_attr(attrList) or self.has_edge_attr(attrList) \
                    or self.not_length(attrList, 2) or (not self.two_nodes(attrList))

        elif cmd == "SHOW":
            err = self.not_empty(attrList)

        return err


    def print_command_objects(self):
        """
        Print information regarding each command object.
        """
        for cmd in self.cmd_obj:
            cmd.print_Class()


    def changed_bool(self, boolVal):
        """
        If the boolean has changed from -1, then return True.
        Otherwise, return False.
        """
        return boolVal != -1


    def not_empty_names(self, names):
        """
        Check whether there are any empty names.
        If yes, return True. Otherwise, return False.
        """
        return (names != [])


    def not_empty(self, attrList):
        """
        Check whether the attribute list is not empty.
        If yes, return True. Otherwise, return False.
        """
        return (not attrList == [])


    def has_edge_attr(self, attrList):
        """
        Check if an edge attribute exists in the list of attributes.
        If yes, return True. Otherwise, return False.
        """
        for lst in attrList:
            if lst[0] == "e:":
                return True
        return False


    def has_node_attr(self, attrList):
        """
        Check if a node attribute exists in the list of attributes.
        If yes, return True. Otherwise, return False.
        """
        for lst in attrList:
            if lst[0] == "n:":
                return True
        return False


    def has_bool_attr(self, attrList):
        """
        Check if a boolean attribute exists in the list of attributes.
        If yes, return True. Otherwise, return False.
        """
        for lst in attrList:
            if lst[0] == "b:":
                return True
        return False


    def not_length(self, attrList, num):
        """
        Check if the supplied length is the same length as that of the
        attribute list passed in the argument list. 
        If yes, return True. Otherwise, return False.
        """
        return len(attrList) != num


    def even(self, attrList):
        """
        Check if the supplied length is even. 
        If yes, return True. Otherwise, return False.
        """
        return (len(attrList) % 2) == 0


    def odd(self, attrList):
        """
        Check if the supplied length is odd. 
        If yes, return True. Otherwise, return False.
        """
        return (not self.even(attrList))


    def not_alt_node_edge(self, attrList):
        """
        Check if the attribute list has alternating node and edges. 
        If not, return True. Otherwise, return False.
        """
        # counter for odd and even
        i = 1
        for lst in attrList:
            if (i % 2) == 1:
                if lst[0] == "e:":
                    return True
                i += 1
            else:
                if lst[0] == "n:":
                    return True
                i += 1
        return False


    def all_node_last(self, attrList):
        """
        Check if all the attributes except the last attribute is a node. 
        If yes, return True. Otherwise, return False.
        """
        i = len(attrList)
        for x in range(0, i - 1):
            if attrList[x][0] != "n:":
                return False
        return True


    def all_edge_last(self, attrList):
        """
        Check if all the attributes except the last attribute is a edge. 
        If yes, return True. Otherwise, return False.
        """
        i = len(attrList)
        for x in range(0, i - 1):
            if attrList[x][0] != "e:":
                return False
        return True


    def all_bool_last(self, attrList):
        """
        Check if all the attributes except the last attribute is a bool. 
        If yes, return True. Otherwise, return False.
        """
        i = len(attrList)
        for x in range(0, i - 1):
            if attrList[x][0] != "b:":
                return False
        return True


    def last_node(self, attrList):
        """
        Check if last attribute is a node attribute.  
        If yes, return True. Otherwise, return False.
        """
        i = len(attrList)
        return attrList[i - 1][0] == "n:"


    def last_edge(self, attrList):
        """
        Check if last attribute is a edge attribute.  
        If yes, return True. Otherwise, return False.
        """
        i = len(attrList)
        return attrList[i - 1][0] == "e:"


    def last_bool(self, attrList):
        """
        Check if last attribute is a bool attribute.  
        If yes, return True. Otherwise, return False.
        """
        i = len(attrList)
        return attrList[i - 1][0] == "b:"


    def two_nodes(self, attrList):
        """
        Check if first two attributes are node attributes.  
        If yes, return True. Otherwise, return False.
        """
        return attrList[0][0] == "n:" and attrList[1][0] == "n:"


    def two_edges(self, attrList):
        """
        Check if first two attributes are edge attributes.  
        If yes, return True. Otherwise, return False.
        """
        return attrList[0][0] == "e:" and attrList[1][0] == "e:"


    def only_id(self, attrList):
        """
        Check if there are only identifiers in our list of attrbutes.  
        If yes, return True. Otherwise, return False.
        """
        for lst in attrList:
            if len(lst[2]) != 0:
                return False
        return True