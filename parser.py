import sys

# Format: CREATE obj_name attr1_name:attr1 ...
# rule: can't have ':' in attributes!

# Global token and state definitions. 

NUM_TOKENS = 7
NUM_STATES = 9

TOKEN_CREATE = 0
TOKEN_MATCH = 1
TOKEN_RETURN = 2
TOKEN_NAME = 3
TOKEN_ATTR = 4
TOKEN_ERROR = 5
TOKEN_END = 6

STATE_INIT = 0
STATE_CREATE = 1
STATE_MATCH = 2
STATE_RETURN = 3
STATE_NAME_CREATE = 4
STATE_NAME_MATCH = 5
STATE_ATTR = 6
STATE_ERROR = 7
STATE_END = 8


class Parser:
    '''An extremely simple parser class.'''

    def __init__(self, parsedString):
        self.parseStr = parsedString
        self.words = parsedString.split()
        self.create_attrs = {}   # internal dict of arguments for create command
        self.match_attrs = {}    # internal dict of arguments for match command
        self.current_token = -1  # current token being processed by the parser
        self.current_state = STATE_INIT  # current state 
        self.current_word = 0
        self.obj_names = []
        self.done = False        # whether we are done parsing 

        # NOTE: The get token function should keep returning TOKEN_END if
        # there is no more input. 


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
        state_machine[STATE_INIT][TOKEN_END] = (STATE_END, self.finish)

        # STATE_CREATE, received create command 
        state_machine[STATE_CREATE][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_CREATE][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_CREATE][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_CREATE][TOKEN_NAME] = (STATE_NAME_CREATE, self.add_obj_name)
        state_machine[STATE_CREATE][TOKEN_ATTR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_CREATE][TOKEN_ERROR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_CREATE][TOKEN_END] = (STATE_ERROR, self.no_op)

        # STATE_MATCH
        state_machine[STATE_MATCH][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_MATCH][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_MATCH][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_MATCH][TOKEN_NAME] = (STATE_NAME_MATCH, self.no_op)
        state_machine[STATE_MATCH][TOKEN_ATTR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_MATCH][TOKEN_ERROR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_MATCH][TOKEN_END] = (STATE_ERROR, self.no_op)

        # STATE_RETURN
        state_machine[STATE_RETURN][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_NAME] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_ATTR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_ERROR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_RETURN][TOKEN_END] = (STATE_ERROR, self.no_op)

        # STATE_NAME_CREATE
        state_machine[STATE_NAME_CREATE][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_CREATE][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_CREATE][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_CREATE][TOKEN_NAME] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_CREATE][TOKEN_ATTR] = (STATE_ATTR, self.add_create_attr)
        state_machine[STATE_NAME_CREATE][TOKEN_ERROR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_CREATE][TOKEN_END] = (STATE_ERROR, self.no_op)

        # STATE_NAME_MATCH
        state_machine[STATE_NAME_MATCH][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_MATCH][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_MATCH][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_MATCH][TOKEN_NAME] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_MATCH][TOKEN_ATTR] = (STATE_ATTR, self.no_op)
        state_machine[STATE_NAME_MATCH][TOKEN_ERROR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_NAME_MATCH][TOKEN_END] = (STATE_ERROR, self.no_op)

        # STATE_ATTR
        state_machine[STATE_ATTR][TOKEN_CREATE] = (STATE_CREATE, self.no_op)
        state_machine[STATE_ATTR][TOKEN_MATCH] = (STATE_MATCH, self.no_op)
        state_machine[STATE_ATTR][TOKEN_RETURN] = (STATE_RETURN, self.no_op)
        state_machine[STATE_ATTR][TOKEN_NAME] = (STATE_ERROR, self.no_op)
        state_machine[STATE_ATTR][TOKEN_ATTR] = (STATE_ATTR, self.add_create_attr)
        state_machine[STATE_ATTR][TOKEN_ERROR] = (STATE_ERROR, self.no_op)
        state_machine[STATE_ATTR][TOKEN_END] = (STATE_END, self.finish)

        # STATE_ERROR
        state_machine[STATE_ERROR][TOKEN_CREATE] = (STATE_END, self.finish)
        state_machine[STATE_ERROR][TOKEN_MATCH] = (STATE_END, self.finish)
        state_machine[STATE_ERROR][TOKEN_RETURN] = (STATE_END, self.finish)
        state_machine[STATE_ERROR][TOKEN_NAME] = (STATE_END, self.finish)
        state_machine[STATE_ERROR][TOKEN_ATTR] = (STATE_END, self.finish)
        state_machine[STATE_ERROR][TOKEN_ERROR] = (STATE_END, self.finish)
        state_machine[STATE_ERROR][TOKEN_END] = (STATE_END, self.finish)


        self.state_machine = state_machine

    def get_Words(self):
        return self.words

    def get_String(self):
        return self.parseStr

    def get_token(self, word):
        if (word.lower() == "create"):
            return TOKEN_CREATE
        elif (word.lower() == "match"):
            return TOKEN_MATCH
        elif (word.lower() == "return"):
            return TOKEN_MATCH
        elif (word == ";"):
            return TOKEN_END
        elif (word.count(":") == 1):
            return TOKEN_ATTR
        elif (isinstance(word, basestring)):
            return TOKEN_NAME
        else:
            return TOKEN_ERROR

    # Callback methods used in the finite state machine.

    ''' No operation. '''
    def no_op(self):
        return

    ''' Add object name to internal list. '''
    def add_obj_name(self):
        self.obj_names.append(self.current_token)

    ''' Add argument key-value pair to internal attributes dictionary for create 
        command. '''
    def add_create_attr(self):
        lst = self.current_word.split(":")
        self.create_attrs[lst[0]] = lst[1]

    ''' Indicate the end of parsing. '''
    def finish(self):
        self.done = True

    def run(self):
        
        for word in self.words:
            if (self.done):
                break
                
            self.current_word = word
            self.current_token = self.get_token(word)
            # run the state machine one step forward
            tuppy = self.state_machine[self.current_state][self.current_token]

            # execute callback method corresponding to this transition 
            tuppy[1]()

            # transition to the next state
            self.current_state = tuppy[0] 
        
        print self.create_attrs



if __name__ == "__main__":
    commands = []
    print("Welcome to microDB!")
    print("Enter commands into the interpreter below.")
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
            break
        sys.stdout.write("... ")
    command_str = " ".join(commands)
    parser = Parser(command_str)
    parser.run()
