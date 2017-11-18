class Player(object):
    """A player

    Attributes:

    """

    def __init__(self, name):
        """Return an initialized Player object"""
        self.name = name
        self.myCards = []
        self.curLocation = "???" #how to initialize?
        
        print("player initialized")
        
    def getLocation(self):
        return self.curLocation
        
    def move(location):
        self.curLocation = location