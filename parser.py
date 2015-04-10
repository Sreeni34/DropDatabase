class Parser:
    """An extremely simple parser class"""

    def __init__(self, parsedString):
        self.parseStr = parsedString
        self.words = parsedString.split()

    def get_Words(self):
        return self.words

    def get_String(self):
        return self.parseStr

    def f(self):
        return 'hello, world'

