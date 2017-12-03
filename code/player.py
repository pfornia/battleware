class Player(object):
    '''A player

    Attributes:

    '''

    def __init__(self, name, location):
        '''Return an initialized Player object'''
        self.name = name
        self.myCards = []
        self.curLocation = location #how to initialize?
        
        print("player initialized")
        
    def getLocation(self):
        return self.curLocation
        
    def move(self, location):
        #rmv from first location
        #location.rmvOccupant.remove(self)
        
        #update location
        self.curLocation = location
        
        #add self to location's occupant list
        location.addOccupant(self)
        
    def addCard(self, card):
        self.myCards.append(card)
        
    def getCards(self):
        return self.myCards
