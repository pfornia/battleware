class Location(object):
    """A location

    Attributes:

    """

    def __init__(self, name, adjLocations):
        """Return an initialized Player object"""
        self.name = name
        #initialize empty set of occupants
        self.occupants = []
        self.adjLocations = adjLocations
        
        print("location initialized")
        
    def getOccupants(self):
        return self.occupants
            
    def getAdjLocations(self):
        return self.adjLocations
    
    def addOccupant(self, player):
        self.occupants.append(player)
    
    def addOccupant(self, player):
        self.occupants.append(player)
