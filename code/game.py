from card_controller import CardController
from player import Player
from location import Location, Room, Hallway

# Global arrays indicating character names and initial locations
PLAYER_NAMES = ["Miss Scarlet",
    "Col Mustard",
    "Mrs White",
    "Mr Green",
    "Mrs Peacock",
    "Prof Plum"]
    
#location indices
INITIAL_LOCATIONS = [10,13,20,19,16,11]

#Weapons (need to be a class??)
WEAPONS = ["Rope",
    "Lead Pipe",
    "Knife",
    "Wrench",
    "Candlestick",
    "Revolver"]
    
ROOM_NAMES = ["Study",
    "Hall",
    "Lounge",
    "Library",
    "Billiard Room",
    "Dining Room",
    "Conservatory",
    "Ballroom",
    "Kitchen"]

class Game(object):
    '''An instance of a single game of "Clue-less"

    Attributes:
        player: A list of players
        locations: A set of locations
        whoseTurn: The index of the player whose turn is now.
        cardController: CardController object for this game.
    '''
    
    def __init__(self):
        '''Return an initialized Game object'''
        
        #Initialize empty players list
        self.players = []

        #start with zero indexed player
        self.whoseTurn = 0
        self.hasMoved = False
        
        self.initializeRooms()
        
        self.curSugP = None
        self.curSugR = None
        self.curSugW = None
        
        self.disproverTurn = None

           
        print("game initialized! Waiting for players to join...")
        

    def initializeRooms(self):
        #Initialize complete list of all rooms and hallways
        self.locations = []
        for r in ROOM_NAMES:
            self.locations.append(Room(r))
        
        for i in range(0, 12):
            self.locations.append(Hallway("H" + str(i)))   
         
        '''        
        0   9   1   10  2
        11      12      13
        3   14  4   15  5
        16      17      18
        6   19  7   20  8         
        '''
        
        #Study:
        self.locations[0].addAdjLocation(self.locations[9])
        self.locations[0].addAdjLocation(self.locations[11])
        self.locations[0].addAdjLocation(self.locations[8])
        #Hall:
        self.locations[1].addAdjLocation(self.locations[9])
        self.locations[1].addAdjLocation(self.locations[10])
        self.locations[1].addAdjLocation(self.locations[12])        
        #Lounge:
        self.locations[2].addAdjLocation(self.locations[10])
        self.locations[2].addAdjLocation(self.locations[13])
        self.locations[2].addAdjLocation(self.locations[6])                
        #Library:
        self.locations[3].addAdjLocation(self.locations[11])
        self.locations[3].addAdjLocation(self.locations[14])
        self.locations[3].addAdjLocation(self.locations[16])
        #Billiard:
        self.locations[4].addAdjLocation(self.locations[12])
        self.locations[4].addAdjLocation(self.locations[14])
        self.locations[4].addAdjLocation(self.locations[15])        
        self.locations[4].addAdjLocation(self.locations[17])
        #Dining:
        self.locations[5].addAdjLocation(self.locations[13])
        self.locations[5].addAdjLocation(self.locations[15])
        self.locations[5].addAdjLocation(self.locations[18])        
        #Conservatory:
        self.locations[6].addAdjLocation(self.locations[16])
        self.locations[6].addAdjLocation(self.locations[19])        
        #Ballroom:
        self.locations[7].addAdjLocation(self.locations[17])
        self.locations[7].addAdjLocation(self.locations[19])
        self.locations[7].addAdjLocation(self.locations[20])                
        #Kitchen:
        self.locations[8].addAdjLocation(self.locations[18])
        self.locations[8].addAdjLocation(self.locations[20])       
    
    def addPlayer(self):
        '''Adds player to game, by initializing
        player object into the player list and 
        returning the index of the new player'''
        
        numPlayers = len(self.players)
        
        newPlayer = Player(PLAYER_NAMES[numPlayers],
            self.locations[INITIAL_LOCATIONS[numPlayers]])
            
        self.players.append(newPlayer)
        
        return numPlayers
        
    def notify(self, amount):
        '''Does this return information up??'''
        #???
        
    def initializeGame(self):
        #This is run once after all players are signed in and ready to start... right?
        #Todo: anything else need to be here? Notify interfaces??
        self.cardController = CardController(self.players,
            self.locations,
            WEAPONS)
        #self.cardController.distributeCards() Done in initialization I think.
        
        
    #override used for moving people for a suggestion: no isMoveLegal needed.
    def makeMove(self, playerID, locID, override = False):
        location = self.locations[locID]
        player = self.players[playerID]
        if override:
            result = 0
        else:
            result = self.isMoveLegal(playerID, locID)
        if result == 0:
            #make the move
            player.move(location)
            self.hasMoved = True
            #if moved to a hallway...
            if not location.isRoom:
                #...then turn is over
                self.incrementTurn()
                
        return result
        
    def isMoveLegal(self, playerID, locID):
        #return 
        #1 if not turn
        #2 if not adjacent
        #3 if already in the room
        #4 if hall is blocked
        #5 if already moved
        #0 if move is legal
        
        if self.whoseTurn != playerID:
            return 1

        play = self.players[playerID]
        oldLoc = play.curLocation
        newLoc = self.locations[locID]

        if self.hasMoved:
            return 5
            
        if oldLoc.adjLocations.__contains__(newLoc) == False:
            return 2
            
        if oldLoc == newLoc:
            return 3
            
        if newLoc.isRoom == False and len(newLoc.occupants) > 0:
            return 4
            

            
        return 0
        
    def rotateDisprover(self):
        self.disproverTurn = self.rotate(self.disproverTurn)
        
    def makeSuggestion(self, suggesterID, suspectID, roomID, weaponNum):
        self.curSugP = suspectID
        self.curSugR = roomID
        self.curSugW = weaponNum
        
        self.disproverTurn = self.rotate(suggesterID)
        
        #todo: this.
        # print("I suggest the murder was done in " + roomID + " by " + suspectID + " with " + weaponNum)
        # Disprove suggestion
        # move suggesterPlayer to suspectRoom
        self.makeMove(suspectID, roomID, True)
        # move suspectPlayer to suspectRoom
        # move suspectWeapon to suspectRoom
        # if suspectPlayer holds suspectPlayercard or suspectRoomcard or 
        # suspectWeaponcard suspectPlayer reveals suspectPlayercard or 
        # suspectRoomcard or suspectWeaponcard to suggesterPlayer
        # else if nextPlayer holds suspectPlayercard or suspectRoomcard 
        # or suspectWeaponcard nextPlayer reveals suspectPlayercard or 
        # suspectRoomcard or suspectWeaponcard to suggesterPlayer
        # else if nextPlayer holds suspectPlayercard or suspectRoomcard 
        # or suspectWeaponcard nextPlayer reveals suspectPlayercard or 
        # suspectRoomcard or suspectWeaponcard to suggesterPlayer

        #suggesterPlayer makes an accusation or ends turn

    def makeAccusation(self, suspectID, roomID, weaponNum):
        #todo: this.
        self.curSugP = suspectID
        self.curSugR = roomID
        self.curSugW = weaponNum
        # print("I accuse " + players[playerID] + " of committing the murder in the " + roomID + " with the " + weaponNum)
        # suggesterPlayer peaks at caseFile
        # if accusation is incorrect then suggesterPlayer loses the game
        if self.cardController.checkAccusation(suspectID, roomID, weaponNum):
            return True
        # else suggesterPlayer wins the game
        else:
            return False
        # caseFile is revealed to all players

        return
        
    def incrementTurn(self):
        #If on last player, loop back to first player.
        self.whoseTurn = self.rotate(self.whoseTurn)
            
        self.hasMoved = False
            
    def getPlayerLocID(self, playerID):
        print("location: " + str(self.locations.index(self.players[playerID].curLocation)))
        return self.locations.index(self.players[playerID].curLocation)
        
    def getPlayerName(self, playerID):
        return PLAYER_NAMES[playerID]
        
    def getPlayerCards(self, playerID, cardType):
        if cardType == "P":
            return self.players[playerID].myCardsP
        elif cardType == "R":
            return self.players[playerID].myCardsR
        elif cardType == "W":
            return self.players[playerID].myCardsW
            
    def getSugCards(self):
        disprover = self.players[self.disproverTurn]
        output = []
        if self.curSugP in disprover.myCardsP:
            output.append("P")
        if self.curSugR in disprover.myCardsR:
            output.append("R")
        if self.curSugW in disprover.myCardsW:
            output.append("R")
        return output
            
    def rotate(self, x):
        if x >= len(self.players) - 1:
            return 0
        else:
            return x + 1
