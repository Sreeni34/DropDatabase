import networkx as nx
import matplotlib.pyplot as plt
from graph_structure import *

class VisualizeGraph:
    """
    Class allows a L{GraphStructure} object to be displayed in a user-friendly
    format.
    """
    def __init__(self, gs):
        """
        Stores the L{GraphStructure} object to visually display.

        @type gs: L{GraphStructure} object
        @param gs: L{GraphStructure} object to visually display.
        """
        self.gs = gs
        self.g = self.gs.get_graph()

        # Sets up visual node properties
        self.node_size = 1600
        self.node_color = 'blue'
        self.node_alpha = 0.3
        self.node_text_size = 8

        # Sets up visual edge properties
        self.edge_color = 'blue'
        self.edge_alpha = 0.3
        self.edge_tickness = 1
        self.edge_text_pos = 0.5
        self.edge_text_size = 8

        # Sets the text font for the graph to display 
        self.text_font = 'sans-serif'

        # Uses a shell layout for the graph visualization
        self.graph_pos = nx.shell_layout(self.g)

    def draw_graph(self):
        """
        Draws the entire contents of the graph. The nodes have described
        text for its attributes and the edges also have described text
        for its attributes. The thicker side of the edge indirects a 
        directed edge with an arrow pointing to the end location. 
        """

        self.gs.display()

        # Draws all the nodes
        nx.draw_networkx_nodes(self.g,self.graph_pos,
            node_size=self.node_size, 
            alpha=self.node_alpha,
            node_color=self.node_color)
        # Draw all the edges
        nx.draw_networkx_edges(self.g,self.graph_pos,
            width=self.edge_tickness,
            node_size=self.node_size, 
            alpha=self.edge_alpha,
            edge_color=self.edge_color)

        # Stores all the nodes attributes in a dictionary format
        node_attrs = {}
        for (key, val) in self.g.nodes(data=True):
            node_attrs[key] = val
        # Draws the node attributes
        nx.draw_networkx_labels(self.g, self.graph_pos, 
            labels=node_attrs,
            font_size=self.node_text_size, 
            font_family=self.text_font)

        # Stores all the edges attributes in dictionary format
        edge_dict = {}
        for (n1, n2, attr) in self.g.edges(data=True):
            edge_dict[(n1, n2)] = attr
        # Draws the edge attributes
        nx.draw_networkx_edge_labels(self.g, self.graph_pos, 
            labels=edge_dict, 
            font_size=self.edge_text_size,
            label_pos=self.edge_text_pos)

        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    # Creates a small visual from test data
    gs = GraphStructure();
    g = gs.get_graph()
    g.add_node(1, {'asdf' : 12})
    g.add_node(2, {'qwer' : 2})
    g.add_node(7, {'qwer' : 2})
    g.add_node(5, {'qwer' : 2})
    g.add_node(3, {})
    g.add_edge(1, 2, {'fail' : 'yea'})
    g.add_edge(2,3, {})

    vg = VisualizeGraph(gs)
    vg.draw_graph()


