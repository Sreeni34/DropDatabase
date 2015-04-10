from struct import pack, unpack


''' This class just defines some useful color variables for changing the
    color of stuff printed to the terminal.'''
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":
	print(bcolors.OKGREEN + "TRYING BINARY" + bcolors.ENDC)