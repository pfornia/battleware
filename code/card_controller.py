class Card(object):
    """Card class

    Attributes:
        cardType: 
    
    """
    def __init__(self, subject, thisType):
        self.cardType = thisType
        self.subject = subject
        print("created a new card.")

class CardController(object):
    """The card handler for a game instance

    Attributes:

    """

    def __init__(self, players, locations, weapons):
        """Return an initialized Game object"""
        #player cards do not exist until players join
        self.playerCards = []
        for p in players:
            self.playerCards.append(Card(p, "P"))
        #todo: initialize weapons cards
        self.weaponsCards = []
        for w in weapons:
            self.weaponsCards.append(Card(w, "W"))
        #todo: initialize room cards
        self.roomCards = []
        for l in locations:
            if l.isRoom:
                self.roomCards.append(Card(l, "R"))

        
        self.createCaseFile()
        
        self.distributeCards(players)
        
        print("card controller initialized!")
        
        
    def createCaseFile(self):
        #make these random
        self.caseEnvelope = []
        self.caseEnvelope.append(playerCards[0])
        self.caseEnvelope.append(weaponsCards[0])
        self.caseEnvelope.append(roomCards[0])
        
    def distributeCards(self, players):
        #distribute the cards randomly:
        #for all players???
        #for all remaining cards???
        players[0].addCard(playerCards[1])
        players[0].addCard(weaponsCards[1])
        players[0].addCard(roomCards[1])
        
    def checkAccusation(self, cardSet):
        #todo: if all three cards in set are in caseEnvelope (in any order), return true
        return False
        
