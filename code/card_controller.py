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

        
        #self.createCaseFile() ??
        
        #self.distributeCards(players) ??
        
        print("card controller initialized!")
        
        
    #def createCaseFile(self):
          
    #def distributeCards(self, players):
        