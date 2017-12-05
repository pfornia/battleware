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
        
        self.initializeRooms()
           
        print("game initialized! Waiting for players to join...")
        

    def initializeRooms(self):
        #Initialize complete list of all rooms and hallways
        self.locations = []
        self.locations.append(Room("Study"))
        self.locations.append(Room("Hall"))
        self.locations.append(Room("Lounge"))
        self.locations.append(Room("Library"))
        self.locations.append(Room("Billiard Room"))
        self.locations.append(Room("Dining Room"))
        self.locations.append(Room("Conservatory"))
        self.locations.append(Room("Ballroom"))
        self.locations.append(Room("Kitchen"))
        
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
        self.cardController.distributeCards()
        
        
    def makeMove(self, playerID, locID):
        location = self.locations[locID]
        player = self.players[playerID]
        result = self.isMoveLegal(playerID, locID)
        if result == 0:
            #make the move
            player.move(location)
            self.incrementTurn()
            return result
        return result
        
    def isMoveLegal(self, playerID, locID):
        #return 
        #1 if not turn
        #2 if not adjacent
        #3 if already in the room
        #4 if hall is blocked
        #0 if move is legal
        
        if self.whoseTurn != playerID:
            return 1

        play = self.players[playerID]
        oldLoc = play.curLocation
        newLoc = self.locations[locID]
        
        if oldLoc.adjLocations.__contains__(newLoc) == False:
            return 2
            
        if oldLoc == newLoc:
            return 3
            
        if newLoc.isRoom == False and len(newLoc.occupants) > 0:
            return 4
            
        return 0
        
    def makeSuggestion(self, suggesterID, suspectID, roomID, weaponNum):
        #todo: this.
        return
        
    def makeAccusation(self, suggesterID, suspectID, roomID, weaponNum):
        #todo: this.
        return
        
    def incrementTurn(self):
        #If on last player, loop back to first player.
        if self.whoseTurn >= len(self.players) - 1:
            self.whoseTurn = 0
        else:
            self.whoseTurn += 1
            
    def getPlayerLocID(self, playerID):
        return self.locations.index(self.players[playerID].curLocation)
        
    def getPlayerName(self, playerID):
        return PLAYER_NAMES[playerID]