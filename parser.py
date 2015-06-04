import sys
# if below is commented NEED TO CALL rlwrap with script
# import readline 
from Command_Struct import Command_Struct

# TODO: support for both strings and numbers 
# TODO: MATCH query support for multiple nodes, edges 

# Format: CREATE obj_name attr1_name:attr1 ...
# rule: can't have ':' in attributes!



# Full List of Commands

"""
REL ATTR = e: a b:c
ID ATTR = n: a a:b
BOOL = b: a val:0/1
ID = n: a () ()


CREATE          ID ATTR
CREATEEDGE      ID ATTR REL ATTR ID ATTR ...
CREATEALLEDGE   ID ATTR ID ATTR ... ID ATTR REL ATTR
MATCH           ID ATTR REL ATTR ID ATTR REL ATTR ID ATTR ...
MODIFYNODE      ID ATTR ID ATTR BOOL
MODIFYEDGE      REL ATTR REL ATTR BOOL
DELETENODE      ID ATTR
DELETEEDGE      REL ATTR
RETURN          ID ID ...
HASPATH         ID ATTR ID ATTR
CLEAR
SHORTESTPATH    ID ATTR ID ATTR
NEIGHBOR        ID ATTR
HASEDGE         ID ATTR ID ATTR
COMMONNEIGHBORS ID ATTR ID ATTR
SHOW

# EXTRA
AGG             [id attr (<, >, =) id attr () val ...]
"""





# The following finite state machine is used by the parser to
# enforce the general structure of commands without worrying
# specifically about the type of command. Without the state 
# machine, error checking would be a lot more extensive for
# the parser. There is an error class that is responsible 
# for enforcing correct syntax given a specific commands.




# Global token and state definitions. 

# Tokens to address which state to move to
TOKEN_COMMAND = 0   # Ex. CREATE, MATCH, MODIFYEDGE, etc
TOKEN_NODE = 1      # Ex. n:
TOKEN_NAME = 2      # Ex. a, b, c, etc., any name
TOKEN_ATTR = 3      # Ex. a:b, c:d, ef:gh, etc.
TOKEN_EDGE = 4      # Ex. e:
TOKEN_BOOL = 5      # Ex. b:
TOKEN_PRED = 6      # Ex. >, <, =
TOKEN_END = 7       # Ex. ; - semicolon indicates termination
TOKEN_ERROR = 8     # Ex. CREATE MATCH


# Possible machine states
STATE_INIT = 0
STATE_COMMAND = 1
STATE_NODE = 2
STATE_NAME = 3
STATE_ATTR = 4
STATE_EDGE = 5
STATE_BOOL = 6
STATE_PRED = 7
STATE_END = 8
STATE_ERROR = 9


NUM_TOKENS = TOKEN_ERROR - TOKEN_COMMAND + 1
# number of states with actual transitions (excludes error state)
NUM_STATES = STATE_ERROR - STATE_INIT 




class Parser:
    '''An extremely simple parser class.'''

    def __init__(self, parsedString):
        self.parseStr = parsedString
        self.words = parsedString.split()

        self.curr_token = -1  # current token being processed by the parser
        self.curr_list_token = -1 # specific for createEdge command

        self.curr_state = STATE_INIT  # current state 
        self.curr_word = ""
        self.curr_iden = ""

        self.curr_command = ""      # Used for error checking
        self.errors = 0             # Initialize to no errors

        self.obj_list = []       # Store a list of command objects

        self.curr_obj = None
        self.done = False        # whether we are done parsing 

        # NOTE: The get token function should keep returning TOKEN_END if
        # there is no more input. 


        # The finite state machine used to parse input. Tokens are used to 
        # transition from one state to another. Every entry in the table is 
        # a tuple containing the next state and a function pointer. 
        state_machine = [[0 for j in range(NUM_TOKENS)] for i in range(NUM_STATES)]


        # STATE_INIT
        state_machine[STATE_INIT][TOKEN_COMMAND] = (STATE_COMMAND, self.create_cmd_obj)
        state_machine[STATE_INIT][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_BOOL] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_PRED] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_END] = (STATE_ERROR, self.finish)
        state_machine[STATE_INIT][TOKEN_ERROR] = (STATE_ERROR, self.error)


        # STATE_COMMAND
        state_machine[STATE_COMMAND][TOKEN_COMMAND] = (STATE_ERROR, self.error)
        state_machine[STATE_COMMAND][TOKEN_NODE] = (STATE_NODE, self.create_node)
        state_machine[STATE_COMMAND][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_COMMAND][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_COMMAND][TOKEN_EDGE] = (STATE_EDGE, self.create_edge)
        state_machine[STATE_COMMAND][TOKEN_BOOL] = (STATE_BOOL, self.create_bool)
        state_machine[STATE_COMMAND][TOKEN_PRED] = (STATE_ERROR, self.error)
        state_machine[STATE_COMMAND][TOKEN_END] = (STATE_END, self.finish)
        state_machine[STATE_COMMAND][TOKEN_ERROR] = (STATE_ERROR, self.error)


        # STATE_NODE
        state_machine[STATE_NODE][TOKEN_COMMAND] = (STATE_ERROR, self.error)
        state_machine[STATE_NODE][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_NODE][TOKEN_NAME] = (STATE_NAME, self.add_name)
        state_machine[STATE_NODE][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_NODE][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_NODE][TOKEN_BOOL] = (STATE_ERROR, self.error)
        state_machine[STATE_NODE][TOKEN_PRED] = (STATE_ERROR, self.error)
        state_machine[STATE_NODE][TOKEN_END] = (STATE_END, self.finish)
        state_machine[STATE_NODE][TOKEN_ERROR] = (STATE_ERROR, self.error)


        # STATE_NAME
        state_machine[STATE_NAME][TOKEN_COMMAND] = (STATE_COMMAND, self.project_cmd_obj)
        state_machine[STATE_NAME][TOKEN_NODE] = (STATE_NODE, self.create_node)
        state_machine[STATE_NAME][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_NAME][TOKEN_ATTR] = (STATE_ATTR, self.add_attr)
        state_machine[STATE_NAME][TOKEN_EDGE] = (STATE_EDGE, self.create_edge)
        state_machine[STATE_NAME][TOKEN_BOOL] = (STATE_BOOL, self.create_bool)
        state_machine[STATE_NAME][TOKEN_PRED] = (STATE_PRED, self.add_pred)
        state_machine[STATE_NAME][TOKEN_END] = (STATE_END, self.finish)
        state_machine[STATE_NAME][TOKEN_ERROR] = (STATE_ERROR, self.error)


        # STATE_ATTR
        state_machine[STATE_ATTR][TOKEN_COMMAND] = (STATE_COMMAND, self.create_cmd_obj)
        state_machine[STATE_ATTR][TOKEN_NODE] = (STATE_NODE, self.create_node)
        state_machine[STATE_ATTR][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_ATTR][TOKEN_ATTR] = (STATE_ATTR, self.add_attr)
        state_machine[STATE_ATTR][TOKEN_EDGE] = (STATE_EDGE, self.create_edge)
        state_machine[STATE_ATTR][TOKEN_BOOL] = (STATE_BOOL, self.create_bool)
        state_machine[STATE_ATTR][TOKEN_PRED] = (STATE_PRED, self.add_pred)
        state_machine[STATE_ATTR][TOKEN_END] = (STATE_END, self.finish)
        state_machine[STATE_ATTR][TOKEN_ERROR] = (STATE_ERROR, self.error)


        # STATE_EDGE
        state_machine[STATE_EDGE][TOKEN_COMMAND] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_NAME] = (STATE_NAME, self.add_name)
        state_machine[STATE_EDGE][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_BOOL] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_PRED] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_END] = (STATE_END, self.finish)
        state_machine[STATE_EDGE][TOKEN_ERROR] = (STATE_ERROR, self.error)


        # STATE_BOOL
        state_machine[STATE_BOOL][TOKEN_COMMAND] = (STATE_ERROR, self.error)
        state_machine[STATE_BOOL][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_BOOL][TOKEN_NAME] = (STATE_NAME, self.add_name)
        state_machine[STATE_BOOL][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_BOOL][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_BOOL][TOKEN_BOOL] = (STATE_ERROR, self.error)
        state_machine[STATE_BOOL][TOKEN_PRED] = (STATE_ERROR, self.error)
        state_machine[STATE_BOOL][TOKEN_END] = (STATE_END, self.finish)
        state_machine[STATE_BOOL][TOKEN_ERROR] = (STATE_ERROR, self.error)


        # STATE_PRED
        state_machine[STATE_PRED][TOKEN_COMMAND] = (STATE_COMMAND, self.create_cmd_obj)
        state_machine[STATE_PRED][TOKEN_NODE] = (STATE_NODE, self.create_node)
        state_machine[STATE_PRED][TOKEN_NAME] = (STATE_PRED, self.add_pred)
        state_machine[STATE_PRED][TOKEN_ATTR] = (STATE_ATTR, self.add_attr)
        state_machine[STATE_PRED][TOKEN_EDGE] = (STATE_EDGE, self.create_edge)
        state_machine[STATE_PRED][TOKEN_BOOL] = (STATE_BOOL, self.create_bool)
        state_machine[STATE_PRED][TOKEN_PRED] = (STATE_PRED, self.add_pred)
        state_machine[STATE_PRED][TOKEN_END] = (STATE_END, self.finish)
        state_machine[STATE_PRED][TOKEN_ERROR] = (STATE_ERROR, self.error)


        # STATE_END
        state_machine[STATE_END][TOKEN_COMMAND] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_BOOL] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_PRED] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_END] = (STATE_ERROR, self.finish)
        state_machine[STATE_END][TOKEN_ERROR] = (STATE_ERROR, self.error)

        self.state_machine = state_machine

    def get_token(self, word):
        """
        This method takes in a word entered by the user and 
        returns token specifying the next execuation step. 

        NOTE: The following list of commands represents TOKEN_COMMAND:

        CREATE
        CREATEEDGE
        MATCH 
        MODIFYNODE
        MODIFYEDGE
        DELETENODE
        DELETEEDGE
        HASPATH
        SHORTESTPATH
        NEIGHBOR
        HASEDGE
        COMMONNEIGHBORS
        RETURN
        CLEAR
        SHOW
        VISUALIZE



        @type word: string
        @param word: The word to convert to token
        @rtype: Integer
        @return: An integer which represents a specific token command
        """

        commands_list = ["create", "createedge", "match", "modifynode", 
            "modifyedge", "deletenode", "deleteedge", "haspath", 
            "shortestpath", "neighbor", "hasedge", "commonneighbors", 
            "return", "clear", "show", "visualize", "project"]

        if (word.lower() in commands_list):
            return TOKEN_COMMAND
        elif (word.lower() == "n:"):
            return TOKEN_NODE
        elif (word.lower() == "e:"):
            return TOKEN_EDGE
        elif (word.lower() == "b:"):
            return TOKEN_BOOL
        elif (word == ";"):
            return TOKEN_END
        elif (word.count(":") == 1):
            return TOKEN_ATTR
        elif (word.count(">") == 1 or word.count("<") == 1 or
                 word.count("=") == 1):
            return TOKEN_PRED
        elif (isinstance(word, basestring)):
            return TOKEN_NAME
        else:
            return TOKEN_ERROR

    # Callback methods used in the finite state machine.

    ''' No operation. '''
    def no_op(self):
        print "TODO: OPERATION"
        return 


############################################################
#   Functions that create Command_Struct objects
#   and modify their data.
############################################################

    def create_cmd_obj(self):
        """ 
        Create a Command_Struct object that represents a
        command entered by the user. Insert current word into
        new command struct object and append the object to list
        of command objects. 
        """

        command = self.curr_word.upper()
        self.curr_obj = Command_Struct(command)
        self.obj_list.append(self.curr_obj)

        self.curr_command = command

    def project_cmd_obj(self):
        """
        Check if the command is a project. If the command is
        a project, then we are allowed to enter a command after
        the list of project values in the project command. If the
        command is not project, then we toss and error
        """

        if (self.curr_command.lower() != "project"):
            self.error();
        else:
            # Since this structure is valid, create a new command
            self.create_cmd_obj();



    def create_node(self):
        """
        Create a new list into our list in the current object.
        The type of the object will be classified as n:.
        """

        self.curr_obj.insert_attr_type("n:")


    def create_edge(self):
        """
        Create a new list into our list in the current object.
        The type of the object will be classified as e:.
        """

        self.curr_obj.insert_attr_type("e:")


    def create_bool(self):
        """
        Create a new list into our list in the current object.
        The type of the object will be classified as b:.
        """

        self.curr_obj.insert_attr_type("b:")


    def add_name(self):
        """
        Insert the specified name into our current object.
        """
        self.curr_iden = self.curr_word
        self.curr_obj.insert_attr_name(self.curr_word)


    def add_attr(self):
        """
        Insert the attribute to our current object.
        """

        lst = self.curr_word.split(":")
        self.curr_obj.insert_attr(lst[0], lst[1])

        # If we are currently on bool, store that value
        if (self.curr_obj.get_attr_type() == "b:"):
            if (lst[0].lower() != "val" or (lst[1] != "0" and lst[1] != "1")):
                self.error()
            else:
                self.curr_obj.set_bool(int(lst[1]))

    def add_pred(self):
        """
        Insert the predicate into the names list of our
        current object. If the current word does not contain any
        predicate information, an error is tossed.
        """
        if (self.curr_word.lower() == "and" or self.curr_word.lower() == "or"):
            self.curr_obj.insert_name(self.curr_word.upper())
        elif (">" in self.curr_word):
            lst = self.curr_word.split(">")
            self.curr_obj.insert_name([lst[0], ">", lst[1], self.curr_iden])
        elif ("<" in self.curr_word):
            lst = self.curr_word.split("<")
            self.curr_obj.insert_name([lst[0], "<", lst[1], self.curr_iden])
        elif ("=" in self.curr_word):
            lst = self.curr_word.split("=")
            self.curr_obj.insert_name([lst[0], "=", lst[1], self.curr_iden])
        else:
            self.error()


############################################################
#   Functions that deal with running and ending the program.
############################################################



    def error(self):
        """
        Prints out an error and exits the program.
        """
        self.errors = 1
        self.error_Message(self.curr_command)
        self.done = True


    def error_Message(self, message):
        """
        Prints out an error message specifying the method
        where the error had occurred. Program will stop
        immediately. 

        @type message: String
        @param message: Error message to print our to user
        """

        if message == "":
            print "ERROR: No command entered"
        else:
            print "ERROR in command " + message
        self.done = True

    def get_Errors(self):
        """
        Checks whether any errors have been called when
        going through the state machine. If there are errors,
        return true.

        @rtype: Boolean
        @return: Indicates if there is an error with state machine
        """

        if (self.errors == 1):
            return True
        return False


    def finish(self):
        """ 
        Indicate the end of parsing. 
        """
        self.done = True

    def get_object_list(self):
        """
        Return the list of objects representing commands specified
        by user.

        @rtype: List of Command_Struct objects
        @return: Object list representing commands and arguments
        """
        return self.obj_list


    def run(self):
        """
        Runs the parser and creates an object list containing 
        information about commands and their arguments.
        """
        
        for word in self.words:
            if (self.done or (self.words[len(self.words) - 1] == word)):
                # Do a last update on the names for match commands
                for i in range(0, len(self.obj_list)):
                    if self.obj_list[i].get_command() == "MATCH":
                        if (self.obj_list[i].get_names_size() != 0):
                            self.obj_list[i].fix_names()
                break
            
            self.curr_word = word
            self.curr_token = self.get_token(word)

            # print "this is current token " + str(self.current_token)

            # run the state machine one step forward
            tuppy = self.state_machine[self.curr_state][self.curr_token]

            # execute callback method corresponding to this transition 
            tuppy[1]()

            # transition to the next state
            self.curr_state = tuppy[0] 
