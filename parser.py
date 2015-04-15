import sys

# Format: CREATE obj_name attr1_name:attr1 ...
# rule: can't have ':' in attributes!

# Global token and state definitions. 

NUM_TOKENS = 6
NUM_STATES = 7

TOKEN_CREATE = 0
TOKEN_MATCH = 1
TOKEN_RETURN = 2
TOKEN_NAME = 3
TOKEN_ATTR = 4
TOKEN_ERROR = 5

STATE_INIT = 0
STATE_CREATE = 1
STATE_MATCH = 2
STATE_RETURN = 3
STATE_NAME = 4
STATE_ATTR = 5
STATE_ERROR = 6
STATE_END = 7


class Parser:
    '''An extremely simple parser class.'''

    def __init__(self, parsedString):
        self.parseStr = parsedString
        self.words = parsedString.split()

        # The finite state machine used to parse input. Tokens are used to 
        # transition from one state to another. Every entry in the table is 
        # a tuple containing the next state and a function pointer. 
        state_machine = [[0 for j in range(NUM_TOKENS)] for i in range(NUM_STATES)]

        # STATE_INIT
        state_machine[STATE_INIT][TOKEN_CREATE] = (STATE_CREATE, self.no_op)
        state_machine[STATE_INIT][TOKEN_MATCH] = (STATE_MATCH, self.no_op)
        state_machine[STATE_INIT][TOKEN_RETURN] = (STATE_RETURN, self.no_op)
        state_machine[STATE_INIT][TOKEN_NAME] = (STATE_ERROR, self.no_op)
        state_machine[STATE_INIT][TOKEN_ATTR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_INIT][TOKEN_ERROR] = (STATE_ERROR, self.no_op)

        # STATE_CREATE
        state_machine[STATE_CREATE][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_CREATE][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_CREATE][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_CREATE][TOKEN_NAME] = (STATE_NAME, self.no_op)
        state_machine[STATE_CREATE][TOKEN_ATTR] = (STATE_ATTR, self.no_op)
        state_machine[STATE_CREATE][TOKEN_ERROR] = (STATE_ERROR, self.no_op)

        # STATE_MATCH
        state_machine[STATE_MATCH][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_MATCH][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_MATCH][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_MATCH][TOKEN_NAME] = (STATE_NAME, self.no_op)
        state_machine[STATE_MATCH][TOKEN_ATTR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_MATCH][TOKEN_ERROR] = (STATE_ERROR, self.no_op)

        # STATE_RETURN
        state_machine[STATE_RETURN][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_NAME] = (STATE_NAME, self.no_op)
        state_machine[STATE_RETURN][TOKEN_ATTR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_ERROR] = (STATE_ERROR, self.no_op)

        # STATE_NAME
        state_machine[STATE_NAME][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME][TOKEN_NAME] = (STATE_NAME, self.no_op)
        state_machine[STATE_NAME][TOKEN_ATTR] = (STATE_ATTR, self.no_op)
        state_machine[STATE_NAME][TOKEN_ERROR] = (STATE_ERROR, self.no_op)

        # STATE_ATTR
        state_machine[STATE_ATTR][TOKEN_CREATE] = (STATE_CREATE, self.no_op)
        state_machine[STATE_ATTR][TOKEN_MATCH] = (STATE_MATCH, self.no_op)
        state_machine[STATE_ATTR][TOKEN_RETURN] = (STATE_RETURN, self.no_op)
        state_machine[STATE_ATTR][TOKEN_NAME] = (STATE_ERROR, self.no_op)
        state_machine[STATE_ATTR][TOKEN_ATTR] = (STATE_ATTR, self.no_op)
        state_machine[STATE_ATTR][TOKEN_ERROR] = (STATE_ERROR, self.no_op)

        # STATE_ERROR
        state_machine[STATE_ERROR][TOKEN_CREATE] = (STATE_END, self.no_op)
        state_machine[STATE_ERROR][TOKEN_MATCH] = (STATE_END, self.no_op)
        state_machine[STATE_ERROR][TOKEN_RETURN] = (STATE_END, self.no_op)
        state_machine[STATE_ERROR][TOKEN_NAME] = (STATE_END, self.no_op)
        state_machine[STATE_ERROR][TOKEN_ATTR] = (STATE_END, self.no_op)
        state_machine[STATE_ERROR][TOKEN_ERROR] = (STATE_END, self.no_op)


        self.state_machine = state_machine

    def get_Words(self):
        return self.words

    def get_String(self):
        return self.parseStr

    def f(self):
        return 'hello, world'

    # Callback methods used in the finite state machine.

    ''' No operation. '''
    def no_op(self):
        print ('no_op')
        return





if __name__ == "__main__":
    commands = []
    print("Welcome to microDB!")
    print("Enter commands into the interpreter below.")
    sys.stdout.write(">>> ")
    while True:
        try:
            command = raw_input()
            if (len(command) != 0 and command[-1] == ";"):
                commands.append(command[:-1])
                break
            commands.append(command)
        except KeyboardInterrupt:
            print("Exiting microDB...")
            break
        sys.stdout.write("... ")
    command_str = " ".join(commands)
    parser = Parser(command_str)
    parser.state_machine[0][0][1]()

