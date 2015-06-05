class Project:   
    """
    L{Project} contains the methods to perform simple projects on node and 
    edge attributes in the graph. 
    """   

    def project(self, theList, attrs):
        """
        Function that takes a list of nodes or edges and a list of 
        attributes to project on. It returns the projected list of nodes or 
        edges. 

        @type theList: List (duh)
        @param theList: List of nodes or edges. Each node is a tuple
        consisting of a node id and a dictionary of attributes while each
        edge is a tuple consisting of two node ids and a dictionary
        of attributes. 
        @type attrs: List of strings
        @param attrs: List of attributes to project on. 
        @rtype: List 
        @return: Projected list of nodes or edges. 
        """
        
        if len(theList) == 0:
            print "ERROR : List of nodes/edges must be non-empty for project."
        if len(theList[0]) == 2:
            return self.project_nodes(theList, attrs)
        elif len(theList[0]) == 3:
            return self.project_edges(theList, attrs)
        else:
            print "ERROR : Invalid input list for project."

    def project_nodes(self, theList, attrs):
        """
        Function that takes a list of nodes and a list of 
        attributes to project on. It returns the projected list of nodes.

        @type theList: List (duh)
        @param theList: List of nodes. Each node is a tuple consisting of a 
        node id and a dictionary of attributes.
        @type attrs: List of strings
        @param attrs: List of attributes to project on. 
        @rtype: List 
        @return: Projected list of nodes. 
        """
        ret = []
        try:
            ret = [{attr: n[1][attr] for attr in attrs} for n in theList]
        except KeyError:
            print "ERROR : Invalid attribute for project."
        return ret 

    def project_edges(self, theList, attrs):
        """
        Function that takes a list of edges and a list of 
        attributes to project on. It returns the projected list of edges.

        @type theList: List (duh)
        @param theList: List of edges. Each node is a tuple consisting of two
        node ids and a dictionary of attributes.
        @type attrs: List of strings
        @param attrs: List of attributes to project on. 
        @rtype: List 
        @return: Projected list of edges. 
        """
        ret = []
        try:
            ret = [{attr: e[2][attr] for attr in attrs} for e in theList]
        except KeyError:
            print "ERROR : Invalid attribute for project."
        return ret 
        '''
        ret = [{} for i in range(len(theList))];
        for i, n in enumerate(theList):
            for attr in attrs:
                try:
                    ret[i][attr] = n[1][attr]
                except KeyError:
                    print "ERROR : Invalid attribute for project."
        return ret 
        '''


