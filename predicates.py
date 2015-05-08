class Predicates:   
    """
    Predicates contains the methods to perform filtering on node   
    attributes in the graph, such as counting number of nodes that have   
    an attribute less than a particular value.   
    """   

    def __init__(self, gs):   
        """
        Constructor takes a GraphStructure object as an argument and 
        stores its in-memory graph representation.
        """
        self.gs = gs
        self.g = gs.get_graph()   

    def str2float(self, value):
        """
        Helper function that tries to convert a string representing a number
        to a floating point number. If the string does not represent a 
        number, returns the string "ERROR". 

        @type value: String that represents a number.
        @param value: String to convert to a float. 
        @rtype: Float
        @return: The converted string as a float, or 
                 "ERROR" if an error occurred. 
        """
        try:
            float_val = float(value)
            return float_val 
        except ValueError:
            return "ERROR"

    def filter(self, node_list, attr, value, op):
        """
        Function that takes a list of node ids, an
        attribute to filter on, a value to filter on, and an
        operation string. Returns a filtered list of node ids that 
        satisfy the predicate consisting of the attribute, 
        value and operation. 

        @type node_list: List
        @param node_list: List of nodes. Each node is a tuples consisting 
        of an id and a dictionary of attributes.
        @type attr: String
        @param attr: Attribute used to filter node
        @type value: String that represents a number.
        @param value: Value to compare the node attributes against. 
        @type op: String that is either "<", "=", or ">".
        @param op: Operation to perform when comparing each node attribute 
                   against value. 
        @rtype: List
        @return: Filtered list of nodes that satisfy the predicate. 
        """
        val = self.str2float(value)
        if val == "ERROR":
            print "ERROR : Comparison Value must be an number..."
            return []
        if op == "<":
            return self.filter_less(node_list, attr, val)
        elif op == ">":
            return self.filter_greater(node_list, attr, val)
        elif op == "=":
            return self.filter_equal(node_list, attr, val)
        else:
            print "ERROR : Invalid predicate operation..."
            return []

    def filter_less(self, node_list, attr, val):
        """
        Function that takes a list of node ids, an
        attribute to filter on, and a value to filter on. 
        Returns a filtered list of node ids whose attributes 
        are less than the passed value. 

        @type node_list: List
        @param node_list: List of nodes. Each node is a tuples consisting 
        of an id and a dictionary of attributes.
        @type attr: String
        @param attr: Attribute used to filter node
        @type val: Float
        @param val: Value to compare the node attributes against. 
        @rtype: List
        @return: Filtered list of nodes that satisfy the predicate. 
        """
        ret = []
        for n in node_list:
            attr_val = self.str2float(n[1][attr])
            if attr_val == "ERROR":
                print "ERROR : Got attribute value that is not a number..."
                continue
            if attr_val < val:
                ret.append(n)
        return ret 

    def filter_greater(self, node_list, attr, val):
        """
        Function that takes a list of node ids, an
        attribute to filter on, and a value to filter on. 
        Returns a filtered list of node ids whose attributes 
        are greater than the passed value. 

        @type node_list: List
        @param node_list: List of nodes. Each node is a tuples consisting 
        of an id and a dictionary of attributes.
        @type attr: String
        @param attr: Attribute used to filter node
        @type val: Float
        @param val: Value to compare the node attributes against. 
        @rtype: List
        @return: Filtered list of nodes that satisfy the predicate. 
        """
        ret = []
        for n in node_list:
            attr_val = self.str2float(n[1][attr])
            if attr_val == "ERROR":
                print "ERROR : Got attribute value that is not a number..."
                continue
            if attr_val > val:
                ret.append(n)
        return ret 

    def filter_equal(self, node_list, attr, val):
        """
        Function that takes a list of node ids, an
        attribute to filter on, and a value to filter on. 
        Returns a filtered list of node ids whose attributes 
        are equal to the passed value. 

        @type node_list: List
        @param node_list: List of nodes. Each node is a tuples consisting 
        of an id and a dictionary of attributes.
        @type attr: String
        @param attr: Attribute used to filter node
        @type val: Float
        @param val: Value to compare the node attributes against. 
        @rtype: List
        @return: Filtered list of nodes that satisfy the predicate. 
        """
        ret = []
        for n in node_list:
            attr_val = self.str2float(n[1][attr])
            if attr_val == "ERROR":
                print "ERROR : Got attribute value that is not a number..."
                continue
            if attr_val == val:
                ret.append(n)
        return ret 


