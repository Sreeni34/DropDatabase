import sys
from parser import *
from linker import Linker
from graph_structure import GraphStructure
from graph_storage import GraphStorage
import networkx as nx
from utilities import Utilities
from BatchExecute import BatchExecute
from error_checking import Error_Checking
import readline

class StartDatabase:
    """
    Class runs the entire graph database in the terminal and manages
    the entire interaction from user input to printing out data. 
    """

    def __init__(self, flag, verbose):
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

        # Stores verbose flag
        self.verbose = verbose

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

    def has_Errors(self, parser):
        """
        This method checks the command entered by the user
        for any errors and if there are any, don't create
        a linker.

        @type parser: Object
        @param parser: Parser instance used to check for errors
        @rtype: Boolean
        @return: Boolean indicating whether errors exist
        """

        # First check if state machine produced any error
        # If errors exist, then don't create linker
        if (parser.get_Errors()):
            print "State machine Error"
            return True

        # Create error class instance
        errorCheck = Error_Checking(parser.get_object_list())
        # If there are errors, don't create linker 
        if errorCheck.check_commands():
            print "Command state Error"
            return True       

        return False

    def run(self):
        """
        Keeps the graph database and continously running in the terminal
        and parses the input.
        """
        while True:

            if verbose:
                # Prints out the graph structure for verbose output
                self.gs.display()

            commands = []
            #sys.stdout.write(">>> ")
            command = raw_input(">>> ")
            while True:
                #command = raw_input(">>> ")
                if (len(command) != 0 and command[-1] == ";"):
                    commands.append(command)
                    break
                commands.append(command)
                command = raw_input("... ")
            command_str = " ".join(commands)

            # Start the parser and parse the commands
            if (command_str[-1] == ";"):
                real_command = command_str[:-1] + " ;" # need to add space for parser 
                parser = Parser(real_command)
                parser.run()
            else:
                print "ERROR INVALID QUERY"
            

            # Check if user entered any errors in query.
            # If there are no errors, then create linker
            if (not(self.has_Errors(parser))):
                linker = Linker(parser.get_object_list(), self.gs)
                linker.execute()
            # Else, print the error
            else:
                print "Invalid Query"


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
    verbose = False

    # Initialize options supplied by user for extra options
    if "-b" in sys.argv:
        # Executes batch file into our database
        batch_flag = True
    if "-v" in sys.argv:
        # Displays show for every command
        verbose = True

    # Do all necessary initialization on start-up.
    start = StartDatabase(batch_flag, verbose)

    # Then run the interpreter. 
    try:
        start.run()
    except KeyboardInterrupt:
        start.exit()



