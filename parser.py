import sys
# if below is commented NEED TO CALL rlwrap with script
# import readline 
from Command_Struct import Command_Struct

# TODO: support for both strings and numbers 
# TODO: MATCH query support for multiple nodes, edges 

# Format: CREATE obj_name attr1_name:attr1 ...
# rule: can't have ':' in attributes!

# Global token and state definitions. 

NUM_TOKENS = 10
NUM_STATES = 8 # number of states with actual transitions (excludes error state)

TOKEN_CREATE = 0
TOKEN_MATCH = 1
TOKEN_RETURN = 2
TOKEN_NAME = 3
TOKEN_ATTR = 4
TOKEN_EDGE = 5
TOKEN_NODE = 6
TOKEN_REL = 7
TOKEN_ERROR = 8
TOKEN_END = 9

STATE_INIT = 0
STATE_CREATE = 1
STATE_MATCH = 2
STATE_RETURN = 3
STATE_NAME = 4
STATE_ATTR = 5
STATE_EDGE = 6
STATE_END = 7
STATE_ERROR = 8


class Parser:
    '''An extremely simple parser class.'''

    def __init__(self, parsedString):
        self.parseStr = parsedString
        self.words = parsedString.split()
        self.current_token = -1  # current token being processed by the parser
        self.curr_list_token = -1 # specific for createEdge command
        self.current_state = STATE_INIT  # current state 
        self.current_word = ''
        self.obj_list = []       #Store a list of command objects
        self.curr_obj = None
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
        state_machine[STATE_INIT][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_EDGE] = (STATE_EDGE, self.add_createEdge_object)
        state_machine[STATE_INIT][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_REL] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_ERROR] = (STATE_ERROR, self.error)
        state_machine[STATE_INIT][TOKEN_END] = (STATE_END, self.finish)

        # STATE_CREATE, received create command 
        state_machine[STATE_CREATE][TOKEN_CREATE] = (STATE_ERROR, self.error)
        state_machine[STATE_CREATE][TOKEN_MATCH] = (STATE_ERROR, self.error)
        state_machine[STATE_CREATE][TOKEN_RETURN] = (STATE_ERROR, self.error)
        state_machine[STATE_CREATE][TOKEN_NAME] = (STATE_NAME, self.add_create_object)
        state_machine[STATE_CREATE][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_CREATE][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_CREATE][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_CREATE][TOKEN_REL] = (STATE_ERROR, self.error)
        state_machine[STATE_CREATE][TOKEN_ERROR] = (STATE_ERROR, self.error)
        state_machine[STATE_CREATE][TOKEN_END] = (STATE_ERROR, self.error)

        # STATE_MATCH
        state_machine[STATE_MATCH][TOKEN_CREATE] = (STATE_ERROR, self.error)
        state_machine[STATE_MATCH][TOKEN_MATCH] = (STATE_ERROR, self.error)
        state_machine[STATE_MATCH][TOKEN_RETURN] = (STATE_ERROR, self.error)
        state_machine[STATE_MATCH][TOKEN_NAME] = (STATE_NAME, self.add_match_object)
        state_machine[STATE_MATCH][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_MATCH][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_MATCH][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_MATCH][TOKEN_REL] = (STATE_ERROR, self.error)
        state_machine[STATE_MATCH][TOKEN_ERROR] = (STATE_ERROR, self.error)
        state_machine[STATE_MATCH][TOKEN_END] = (STATE_ERROR, self.error)

        # STATE_RETURN
        state_machine[STATE_RETURN][TOKEN_CREATE] = (STATE_ERROR, self.error)
        state_machine[STATE_RETURN][TOKEN_MATCH] = (STATE_ERROR, self.error)
        state_machine[STATE_RETURN][TOKEN_RETURN] = (STATE_ERROR, self.error)
        state_machine[STATE_RETURN][TOKEN_NAME] = (STATE_END, self.add_return_object)
        state_machine[STATE_RETURN][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_RETURN][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_RETURN][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_RETURN][TOKEN_REL] = (STATE_ERROR, self.error)
        state_machine[STATE_RETURN][TOKEN_ERROR] = (STATE_ERROR, self.error)
        state_machine[STATE_RETURN][TOKEN_END] = (STATE_ERROR, self.error)

        # STATE_NAME
        state_machine[STATE_NAME][TOKEN_CREATE] = (STATE_ERROR, self.error)
        state_machine[STATE_NAME][TOKEN_MATCH] = (STATE_ERROR, self.error)
        state_machine[STATE_NAME][TOKEN_RETURN] = (STATE_ERROR, self.error)
        state_machine[STATE_NAME][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_NAME][TOKEN_ATTR] = (STATE_ATTR, self.add_attr)
        state_machine[STATE_NAME][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_NAME][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_NAME][TOKEN_REL] = (STATE_ERROR, self.error)
        state_machine[STATE_NAME][TOKEN_ERROR] = (STATE_ERROR, self.error)
        state_machine[STATE_NAME][TOKEN_END] = (STATE_ERROR, self.error)

        # STATE_ATTR
        state_machine[STATE_ATTR][TOKEN_CREATE] = (STATE_CREATE, self.no_op)
        state_machine[STATE_ATTR][TOKEN_MATCH] = (STATE_MATCH, self.no_op)
        state_machine[STATE_ATTR][TOKEN_RETURN] = (STATE_RETURN, self.no_op)
        state_machine[STATE_ATTR][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_ATTR][TOKEN_ATTR] = (STATE_ATTR, self.add_attr)
        state_machine[STATE_ATTR][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_ATTR][TOKEN_NODE] = (STATE_ATTR, self.add_list_attr)
        state_machine[STATE_ATTR][TOKEN_REL] = (STATE_ATTR, self.add_list_attr)
        state_machine[STATE_ATTR][TOKEN_ERROR] = (STATE_ERROR, self.error)
        state_machine[STATE_ATTR][TOKEN_END] = (STATE_END, self.finish)

        # STATE_EDGE
        state_machine[STATE_EDGE][TOKEN_CREATE] = (STATE_ERROR, self.no_op)
        state_machine[STATE_EDGE][TOKEN_MATCH] = (STATE_ERROR, self.no_op)
        state_machine[STATE_EDGE][TOKEN_RETURN] = (STATE_ERROR, self.no_op)
        state_machine[STATE_EDGE][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_NODE] = (STATE_ATTR, self.add_list_attr)
        state_machine[STATE_EDGE][TOKEN_REL] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_ERROR] = (STATE_ERROR, self.error)
        state_machine[STATE_EDGE][TOKEN_END] = (STATE_END, self.finish)

        # STATE_END
        state_machine[STATE_END][TOKEN_CREATE] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_MATCH] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_RETURN] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_NAME] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_ATTR] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_EDGE] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_NODE] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_REL] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_ERROR] = (STATE_ERROR, self.error)
        state_machine[STATE_END][TOKEN_END] = (STATE_END, self.finish)

        self.state_machine = state_machine


    def get_token(self, word):
        """
        This method takes in a word entered by the user and 
        returns token specifying the next execuation step. 

        @type word: string
        @param word: The word to convert to token
        @rtype: Integer
        @return: An integer which represents a specific token command
        """

        if (word.lower() == "create"):
            return TOKEN_CREATE
        elif (word.lower() == "match"):
            return TOKEN_MATCH
        elif (word.lower() == "return"):
            return TOKEN_RETURN
        elif (word.lower() == "createedge"):
            return TOKEN_EDGE
        elif (word.lower() == "n:"):
            return TOKEN_NODE
        elif (word.lower() == "e:"):
            return TOKEN_REL
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
        print "TODO: OPERATION"
        return 


############################################################
#   Functions that create Command_Struct objects
#   and modify their data.
############################################################


    def add_create_object(self):
        """ 
        Create a Command_Struct object that represents a create
        command entered by the user. Insert current name into
        new command struct object and append the object to list
        of command objects. 
        """
        self.curr_obj = Command_Struct("CREATE")
        self.curr_obj.set_name(self.current_word)
        self.obj_list.append(self.curr_obj)


    def add_match_object(self):
        """ 
        Create a Command_Struct object that represents a match
        command entered by the user. Insert current name into
        new command struct object and append the object to list
        of command objects. 
        """
        self.curr_obj = Command_Struct("MATCH")
        self.curr_obj.set_name(self.current_word)
        self.obj_list.append(self.curr_obj)


    def add_return_object(self):
        """ 
        Create a Command_Struct object that represents a return
        command entered by the user. Insert current name into
        new command struct object and append the object to list
        of command objects. 
        """
        self.curr_obj = Command_Struct("RETURN")
        self.curr_obj.set_name(self.current_word)
        self.obj_list.append(self.curr_obj)


    def add_createEdge_object(self):
        """ 
        Create a Command_Struct object that represents a createEdge
        command entered by the user. Append the object to list
        of command objects. Also have a token state to help us keep
        track of the arguments supplied to command.
        """
        self.curr_obj = Command_Struct("CREATEEDGE")
        self.curr_obj.set_name("NO NAME")
        self.obj_list.append(self.curr_obj)

        # Reset token object to mention that we are in this command
        self.curr_list_token = 0;


    def add_attr(self):
        """
        Add argument key-value pair to internal attributes dictionary 
        for specific command object. Take care of the special case
        where the command is CREATEEDGE.
        """
        if (self.curr_obj.get_command() == "CREATEEDGE"):
            self.add_list_attr()
        else:
            lst = self.current_word.split(":")
            self.curr_obj.insert_attr(lst[0], lst[1])


    def add_list_attr(self):
        """
        Helper method for the add_attr method. This takes care of
        the special case when CreateEdge is supplied as an argument.
        The method inserts the attribute into the appropriate location
        in our list of attributes dictionary. 
        """

        # Error because we are not in the createEdge command
        if (self.curr_list_token == -1):
            self.error()

        # In createEdge command but have not initialized state
        # The first state would be the n: state
        elif (self.curr_list_token == 0):
            self.curr_list_token = TOKEN_NODE

        # Current state is either n: or e: but we are simply
        # adding an attribute to our dictionary
        elif (self.current_token == TOKEN_ATTR):
            # Add to dictionary
            lst = self.current_word.split(":")
            self.curr_obj.insert_attr(lst[0], lst[1])

            # Update list of dictionary object
            self.update_list_dict()

        # Transition from attr in n: to e:
        elif (self.curr_list_token == TOKEN_NODE and self.current_token == TOKEN_REL):
            # Update current list token and clear list
            self.update_token_and_clear(TOKEN_REL, 1)

        # Transition from attr in e: to n:
        elif (self.curr_list_token == TOKEN_REL and self.current_token == TOKEN_NODE):
            # Update current list token and clear list
            self.update_token_and_clear(TOKEN_NODE, 2)

        # No-valid state
        else:
            self.error_Message("add_list_attr");


    def update_list_dict(self):
        """
        This is a helper function to the add_list_attr method
        which updates the list of dictionaries in the Command_Struct
        object. 
        """
        # Update first index in list of dict object
        if (self.curr_list_token == TOKEN_NODE and
            (self.curr_obj.get_attr_list_size() == 0 or
            self.curr_obj.get_attr_list_size() == 1)):

            self.curr_obj.insert_attr_list(0)
        # Update second index in list of dict object
        elif (self.curr_list_token == TOKEN_REL):
            self.curr_obj.insert_attr_list(1)
        # Update third index in list of dict object
        elif (self.curr_list_token == TOKEN_NODE):
            self.curr_obj.insert_attr_list(2)
        # Invalid Token Read
        else:
            self.error_Message("update_list_dict");


    def update_token_and_clear(self, token, size):
        """
        This method resets the token to represent the new 
        state (n: or e:) we are in and clears the previous
        list of attributes.
        """
        # Check if the sizes are satisfied
        if (self.curr_obj.get_attr_list_size() == size):
            # Update pointer, and clear attributes
            self.curr_list_token = token
            self.curr_obj.clear_attr()
        # Sizes do not match, problem with add_list_attr
        else:
            self.error_Message("update_token_and_clear");


############################################################
#   Functions that deal with running and ending the program.
############################################################
    
    def error(self):
        """
        Prints out an error and exits the program.
        """
        print "TODO : ERROR MESSAGE HERE"
        self.done = True


    def error_Message(self, message):
        """
        Prints out an error message specifying the method
        where the error had occurred. Program will stop
        immediately. 

        @type message: string
        @param message: Error message to print our to user
        """

        print "ERROR: " + message
        self.done = True


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
            # print "this is the word: " + word
            if (self.done):
                # print "Error occurred in parser."
                break
            
            self.current_word = word
            self.current_token = self.get_token(word)

            # print "this is current token " + str(self.current_token)

            # run the state machine one step forward
            tuppy = self.state_machine[self.current_state][self.current_token]

            # execute callback method corresponding to this transition 
            tuppy[1]()

            # transition to the next state
            self.current_state = tuppy[0] 
