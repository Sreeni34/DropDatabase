import sys
from parser import *
from linker import Linker
from graph_structure import GraphStructure
from graph_storage import GraphStorage
import networkx as nx
from utilities import Utilities
from BatchExecute import BatchExecute

class StartDatabase:
    """
    Class runs the entire graph database in the terminal and manages
    the entire interaction from user input to printing out data. 
    """

    def __init__(self, flag):
        """ 
        Initializes the graph database by reading persisted data on disk
        and setting up the internal in-memory graph file.
        """        
        print "Welcome to microDB!"
        self.gs = GraphStructure()
        self.gstorage = GraphStorage(self.gs)

        # Loads data on disk
        self.graph_file = 'graph_file'
        self.id_file = 'id_file'
        self.load_persistent_data()

        # If flag is set, need to execute commands in file that user passed.
        if flag:
            print "Loading batch file..."
            BatchExecute(self.gs, sys.argv[1])
            print "Done executing batch file!"


    def load_persistent_data(self):
        """
        Loads persisted data on disk, if it exists, into our GraphStructure
        object.
        """
        print "Loading database from disk..."
        if Utilities.files_exist(self.graph_file, self.id_file):
            self.gstorage.load_graph(self.graph_file, self.id_file)
            print "Finished loading database from disk."
        else:
            print "No files to load from."

    def run(self):
        """
        Keeps the graph database and continously running in the terminal
        and parses the input.
        """
        while True:
            # Prints out the graph structure for testing purposes
            #self.gs.display()

            commands = []
            sys.stdout.write(">>> ")
            while True:
                command = raw_input()
                if (len(command) != 0 and command[-1] == ";"):
                    commands.append(command)
                    break
                commands.append(command)
                sys.stdout.write("... ")
            command_str = " ".join(commands)

            # Start the parser and parse the commands
            if (command_str[-1] == ";"):
                real_command = command_str[:-1] + " ;" # need to add space for parser 
                parser = Parser(real_command)
                parser.run()
            else:
                print "ERRORRRRRRRRRRRRRRRRRRRRR"
            # Store the created objects in linker and call functions
            linker = Linker(parser.get_object_list(), self.gs)
            linker.execute()

    def exit(self):
        """
        Persists the graph data and exits the graph database.
        """
        print
        self.persist_data()
        print "Exiting microDB..."

    def persist_data(self):
        """
        Persists the GraphStructure object onto disk.
        """
        print "Writing database back to disk..." 
        self.gstorage.write_graph(self.graph_file, self.id_file)


# Start our main programs
if __name__ == "__main__":

    batch_flag = False

    # Check if user supplied a file of commands to execute in a batch. 
    # If so, indicate that they should be executed during initialization. 
    if len(sys.argv) == 2:
        batch_flag = True

    # Do all necessary initialization on start-up.
    start = StartDatabase(batch_flag)

    # Then run the interpreter. 
    try:
        start.run()
    except KeyboardInterrupt:
        start.exit()



