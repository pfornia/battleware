from random import shuffle

class Card(object):
    '''Card class

    Attributes:
        cardType: 
    
    '''
    def __init__(self, subjectID, thisType):
        self.cardType = thisType
        self.subjectID = subjectID
        print("created a new card.")

class CardController(object):
    '''The card handler for a game instance

    Attributes:

    '''

    def __init__(self, players, locations, weapons):
        '''Return an initialized Game object'''
        #player cards do not exist until players join
        self.playerCards = []
        for p in range(len(players)):
            self.playerCards.append(Card(p, "P"))
        #todo: initialize weapons cards
        self.weaponsCards = []
        for w in range(len(weapons)):
            self.weaponsCards.append(Card(w, "W"))
        #todo: initialize room cards
        self.roomCards = []
        for l in range(len(locations)):
            if locations[l].isRoom:
                self.roomCards.append(Card(l, "R"))

        
        self.createCaseFile()
        
        self.distributeCards(players)
        
        print("card controller initialized!")
        
        
    def createCaseFile(self):
        #make these random
        shuffle(self.playerCards)
        shuffle(self.weaponsCards)
        shuffle(self.roomCards)
        self.caseEnvelope = []
        self.caseEnvelope.append(self.playerCards[0])
        self.caseEnvelope.append(self.roomCards[0])
        self.caseEnvelope.append(self.weaponsCards[0])

        
    def distributeCards(self, players):
        #distribute the cards randomly: do we need random in createCaseFile and distributeCards?
        #for all players???
        #for all remaining cards???
        #do we need a loop to distribute cards?
        #cards are combined after createCaseFile CLUE SETUP 5
        nextPlayer = 0
        
        for p in range(1,len(self.playerCards)):
            players[nextPlayer].addCard(self.playerCards[p])
            if nextPlayer >= len(players) - 1:
                nextPlayer = 0
            else:
                nextPlayer += 1
        for r in range(1,len(self.roomCards)):
            players[nextPlayer].addCard(self.roomCards[r])
            if nextPlayer >= len(players) - 1:
                nextPlayer = 0
            else:
                nextPlayer += 1
        for w in range(1,len(self.weaponsCards)):
            players[nextPlayer].addCard(self.weaponsCards[w])
            if nextPlayer >= len(players) - 1:
                nextPlayer = 0
            else:
                nextPlayer += 1

                
    def checkAccusation(self, suspectID, roomID, weaponNum):
    
        if (suspectID == self.caseEnvelope[0].subjectID and
        roomID == self.caseEnvelope[1].subjectID and
        weaponNum == self.caseEnvelope[2].subjectID):
            return True
        else:
            return False
            
        
