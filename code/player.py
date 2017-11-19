class Player(object):
    """A player

    Attributes:

    """

    def __init__(self, name, location):
        """Return an initialized Player object"""
        self.name = name
        self.myCards = []
        self.curLocation = location #how to initialize?
        
        print("player initialized")
        
    def getLocation(self):
        return self.curLocation
        
    def move(location):
        self.curLocation = location