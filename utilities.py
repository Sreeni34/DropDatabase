import os.path

class Utilities:
    """
    Class provides a list of static methods that are useful throughout
    the graph database implementation.
    """

    @staticmethod 
    def files_exist(*files):
        """
        Static method accepts an arbitrary number of filename and
        returns true if all the files exist, false otherwise.

        @type files: String
        @param files: Filename to check if it exists
        """
        for f in files:
            if not os.path.isfile(f):
                return False
        return True
