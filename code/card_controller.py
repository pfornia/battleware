class Card(object):
    """Card class

    Attributes:
        cardType: 
    
    """
    def __init__(self, thisPlayer, thisType):
        self.cardType = thisType
        self.name = thisPlayer
        print("created a new card.")

class CardController(object):
    """The card handler for a game instance

    Attributes:

    """

    def __init__(self):
        """Return an initialized Game object"""
        #player cards do not exist until players join
        self.playerCards = []
        #todo: initialize weapons cards
        self.weaponsCards = []
        #todo: initialize room cards
        self.roomCards = []
        
        #self.caseEnvelope = ??
        
        print("card controller initialized!")
        
    def addPlayerCard(self, thisPlayer):
        self.playerCards.append(Card(thisPlayer, "P"))
        
    #def createCaseFile(self):
        #do nothing??   
        