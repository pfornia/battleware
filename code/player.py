class Player(object):
    '''A player

    Attributes:

    '''

    def __init__(self, name, location):
        '''Return an initialized Player object'''
        self.name = name
        self.myCardsP = []
        self.myCardsR = []
        self.myCardsW = []
        self.curLocation = location #how to initialize?
        location.addOccupant(self)
        
        print("player initialized")
        
    def getLocation(self):
        return self.curLocation
        
    def move(self, location):
        #rmv from first location
        self.curLocation.rmvOccupant(self)
        
        #update location
        self.curLocation = location
        
        #add self to location's occupant list
        location.addOccupant(self)
        
        
        
    def addCard(self, card):
        if card.cardType == "P":
            self.myCardsP.append(card.subjectID)
        elif card.cardType == "R":
            self.myCardsR.append(card.subjectID)
        elif card.cardType == "W":
            self.myCardsW.append(card.subjectID)
            
    def getCards(self):
        return self.myCards
