import networkx as nx 

class GraphStorage:
    """
    This class handles writing the graph database to memory and reading
    the graph database from memory. 
    """
    def __init__(self, gs):
        # Takes a graph structure object. 
        self.gs = gs
        
    def load_file(self, file1):
        # load graph from file and set it to be the global graph
        self.gs.set_graph(nx.read_graphml(file1))
        print(self.gs.get_graph().nodes(data=True))

    def write_file(self, file1):
        # get graph from graph structure and write it to file 
        nx.write_graphml(self.gs.get_graph(), file1)
