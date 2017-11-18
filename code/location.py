class Location(object):
    """A location

    Attributes:

    """

    def __init__(self, name):
        """Return an initialized Location object"""
        self.name = name
        #initialize empty set of occupants
        self.occupants = []
        self.adjLocations = adjLocations
        
        print("location initialized")
        
    def getOccupants(self):
        return self.occupants
            
    def getAdjLocations(self):
        return self.adjLocations
        
    def addAdjLocation(self, location):
        """ add adjacency (in both directions)"""
        self.adjLocations.append(location)
        location.adjLocations.append(self)
    
    def addOccupant(self, player):
        self.occupants.append(player)
    
    def addOccupant(self, player):
        self.occupants.append(player)
        

class Room(Location):
    """A Room (type of Location)"""

    def __init__(self, name):
        """Return an initialized Room object"""
        self.name = name
        #initialize empty set of occupants
        self.occupants = []
        self.adjLocations = []

        print("room initialized")
        
    
    
class Hallway(Location):
    """A Hallway (type of Location)"""

    def __init__(self, name):
        """Return an initialized hallway object"""
        self.name = name
        #initialize empty set of occupants
        self.occupants = []
        self.adjLocations = []

        print("hallway initialized")
        