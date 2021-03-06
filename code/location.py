class Location(object):
    '''A location

    Attributes:

    '''

    def __init__(self, name):
        '''Return an initialized Location object'''
        self.name = name
        #initialize empty set of occupants
        self.occupants = []
        self.adjLocations = []
        
        print("location initialized")
        
    def addAdjLocation(self, location):
        ''' add adjacency (in both directions)'''
        self.adjLocations.append(location)
        location.adjLocations.append(self)
    
    def addOccupant(self, player):
        self.occupants.append(player)
    
    def rmvOccupant(self, player):
        #remove occupant.
        self.occupants.__delitem__(self.occupants.index(player))
        return

class Room(Location):
    '''A Room (type of Location)'''

    def __init__(self, name):
        '''Return an initialized Room object'''
        self.name = name
        #initialize empty set of occupants
        self.occupants = []
        self.adjLocations = []
        self.isRoom = True

        #print("room initialized")
        
    
    
class Hallway(Location):
    '''A Hallway (type of Location)'''

    def __init__(self, name):
        '''Return an initialized hallway object'''
        self.name = name
        #initialize empty set of occupants
        self.occupants = []
        self.adjLocations = []
        self.isRoom = False
        
        #print("hallway initialized")
        
