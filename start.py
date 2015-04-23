import sys
from parser import Parser
from linker import Linker
from graph_structure import GraphStructure

# Start our main programs
if __name__ == "__main__":
    print("Welcome to microDB!")
    print("Enter commands into the interpreter below.")
    not_done = True
    gs = GraphStructure()
    
    while True:
        commands = []
        try:
            sys.stdout.write(">>> ")
            while True:
                try:
                    command = raw_input()
                    if (len(command) != 0 and command[-1] == ";"):
                        commands.append(command)
                        break
                    commands.append(command)
                except KeyboardInterrupt:
                    print("\nExiting microDB...")
                    not_done = False
                    break
                sys.stdout.write("... ")
            if not not_done:
                break
            command_str = " ".join(commands)

            # Start the parser and parse the commands
            parser = Parser(command_str)
            parser.run()

            # Store the created objects in linker and call functions
            linker = Linker(parser.get_object_list(), gs)
            # linker.print_object_list()
            # linker.link_object()
            linker.execute()

        except KeyboardInterrupt:
            print("\nExiting microDB...")
            break