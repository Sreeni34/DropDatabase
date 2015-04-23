from query_evaluator import QueryEvaluator
from graph_structure import GraphStructure

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
        # Sets up a QueryEvaluator object to perform the loading operations
        self.q_eval = QueryEvaluator(gs)


    def load_text_file(self, text_file):
        """
        Loads the data from the text file into the in memory graph 
        structure stored in the QueryEvaluator object.
        """
        f = open(text_file, 'r')
        for line in f:
            # Skips commented lines in text file
            if line[0][0] == '#':
                continue
            # Adds node and edges between the nodes in our graph database
            line = line.strip().split('\t')
            node1, node2 = int(line[0]), int(line[1])
            n1 = self.q_eval.add_node({'id' : node1})
            n2 = self.q_eval.add_node({'id' : node2})
            e1 = self.q_eval.add_relationship(n1, n2, {})

        f.close()

if __name__ == '__main__':
    file_name = 'Wiki-Vote.txt'
    gs = GraphStructure()
    data = LoadData(gs)
    data.load_text_file(file_name)
    

