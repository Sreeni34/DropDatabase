import networkx as nx 
from utilities import Utilities

class GraphStorage:
    """
    This class handles writing and reading the GraphStructure object 
    to disk.
    """
    def __init__(self, gs):
        """ 
        Takes a GraphStructure object to store on disk.

        @type gs: GraphStructure
        @param gs: GraphStructure object to store on disk.
        """
        self.gs = gs
        
    def load_graph(self, graph_file, id_file):
        """
        Loads the GraphStructure object from two files. The first file
        persists the in-memory graph data while the second file persists
        the unique ids. The two files must exist or else nothing will happen.

        @type graph_file: String
        @param graph_file: File to store the in-memory graph structure
        @type id_file: String
        @param id_file: File to store unique id number
        """

        if not Utilities.files_exist(graph_file, id_file):
            print 'One or more files does not exist' 
            return

        # Stores graph data from file and loads it to internal graph
        self.gs.set_graph(nx.read_graphml(graph_file))

        # Read current id from file to GraphStructure
        f = open(id_file, 'r')
        val = f.readline().strip()
        if val == "":
            val = 0
        self.gs.set_id(int(val))
        f.close()


    def write_graph(self, file1, file2):
        """
        Writes the GraphStructure object to two files. The first file
        will contain the in-memory graph data while the second file will
        contain the unique id number. 
        """
        nx.write_graphml(self.gs.get_graph(), file1)

        # Write current Id to another file
        f = open(file2, 'w')
        f.write(str(self.gs.get_id()))
        f.close()



