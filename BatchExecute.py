from query_evaluator import QueryEvaluator
from graph_structure import GraphStructure
from parser import Parser
from linker import Linker

class BatchExecute:   
    """
    This class is responsible for executing a batch of commands that are 
    in a txt file. 
    """   

    def __init__(self, gs, filename):   
        """
        Constructor takes a GraphStructure object, a parser object, and  
        a file name as arguments. It will execute all of the commands that are 
        in the file. 
        """
        self.gs = gs

        f = open(filename, 'r')

        # Every line in the file is a command 
        for line in f:
            # Skips blank lines and commented lines in text file
            if (len(line.split()) == 0) or (line[0] == '#'):
                continue

            # Assert that line ends with semicolon 
            if line.split()[-1][-1] != ';':
                print "Invalid file format! Every line must end with a semicolon."
                break

            # Add a space before semicolon for parser. This ensures that 
            # commands can end with a semicolon right after the last word 
            # in the command.  
            arr = line.split()
            arr[-1] = arr[-1][:-1] + ' ;'
            command = " ".join(arr) 

            # Run the parser. 
            parser = Parser(command)
            parser.run()

            # Extract the created objects from the parser and execute the linker. 
            linker = Linker(parser.get_object_list(), self.gs)
            linker.execute()

        f.close()




