from query_evaluator import QueryEvaluator
from graph_structure import GraphStructure
from graph_storage import GraphStorage
from utilities import Utilities



class LoadData:
    """
    Class is responsible for taking a text file in a certain format
    and loading add the nodes and edges into the in memory Graph Database.
    """

    def __init__(self, gs):
        """
        Takes a GraphStructure object to load the data into.

        @type gs: GraphStructure object
        @param gs: GraphStructure object that is used to store nodes and 
        edges in.
        """
        self.gs = gs
        self.gstorage = GraphStorage(self.gs)

        # Loads data on disk
        self.graph_file = 'graph_file'
        self.id_file = 'id_file'
        self.load_data()

        # Sets up a QueryEvaluator object to perform the loading operations
        self.q_eval = QueryEvaluator(gs)

    def load_data(self):
        """
        Loads persisted data on disk, if it exists, into our GraphStructure
        object.
        """
        if Utilities.files_exist(self.graph_file, self.id_file):
            self.gstorage.load_graph(self.graph_file, self.id_file)


    def load_text_file(self, text_file):
        """
        Loads the data from the text file into the in memory graph 
        structure stored in the QueryEvaluator object and saves the
        data onto disk.
        """
        # Stores a set of nodes and edges
        node = set()
        edge = set()

        f = open(text_file, 'r')
        for line in f:
            # Skips commented lines in text file
            if line[0][0] == '#':
                continue
            # Stores nodes and edges in our set data structure
            line = line.strip().split('\t')
            node1, node2 = line[0], line[1]
            node.add(node1)
            node.add(node2)
            edge.add((node1, node2))

        f.close()

        # Stores return value when a node is added
        node_dict = {}

        # Adds node and edges between the nodes in our graph database
        for n in node:
            n1 = self.q_eval.add_node({'id' : n})
            node_dict[n] = n1

        for node1,node2 in edge:
            self.q_eval.add_relationship(node_dict[node1], node_dict[node2], {})

        # Saves the file to disk
        self.gstorage.write_graph(self.graph_file, self.id_file)

if __name__ == '__main__':
    file_name = 'Wiki-Vote.txt'
    gs = GraphStructure()
    data = LoadData(gs)
    data.load_text_file(file_name)
    

