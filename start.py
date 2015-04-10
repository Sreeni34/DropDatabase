import parser

# Function that asks user for input until the user
# decides to quit the program.
def askInput():
	while (True):
		query = raw_input("Query(Enter Q to quit)>>> ")
		if (query == "Q"):
			break
		else:
			parse = parser.Parser(query)
			print parse.get_Words()
			print parse.get_String()

# Start our main program
if __name__ == '__main__':
	print "Starting Program\n"
	askInput()
	print "\nProgram Done!\n"