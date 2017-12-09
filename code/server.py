import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
from game import Game

from socket import socket, SOCK_DGRAM, AF_INET 
import socketserver

TOTAL_PLAYERS = 1
    
PLAYER_NAMES = ["Miss Scarlet",
    "Col Mustard",
    "Mrs White",
    "Mr Green",
    "Mrs Peacock",
    "Prof Plum"]
    
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
    

    
class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print(data)
        
    def Network_move(self, data):
        #What is status of attempted move?
        legal = self._server.game.makeMove(data["client"], data["l"])
        if legal == 0:
            self._server.sendPositions()
            #if they have moved, but turn is not yet over
            if self._server.game.hasMoved:
                self._server.optionSet = "room"
                self._server.sendOptions([
                        "Make Suggestion",
                        "Make Accusation",
                        "End turn"],
                    data["client"])
            else: 
                self._server.clearAllOptions()
                self._server.sendTurns()
     
        elif legal == 1:
            self._server.sendMessage("Not your turn.", data["client"])
        elif legal == 2:
            self._server.sendMessage("That room is too far away.", data["client"])
        elif legal == 3:
            self._server.sendMessage("Can't stay here.", data["client"])
        elif legal == 4:
            self._server.sendMessage("Hallway blocked.", data["client"]) 
        elif legal == 5:
            self._server.sendMessage("You've already moved.", data["client"])            
            
            
    def Network_selectOption(self, data):
        self._server.selectOption(data["o"], data["client"])
            
    #This will run when a client closes their window.
    #def Close(self):
    #    self._server.close(self.gameid)
    
class GameMenuServer(PodSixNet.Server.Server):
    
    
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.game = Game()
        self.numPlayers=0
        self.playerChannels = [] #list of channels
        self.players = [] #list of player object pointers
        self.optionSet = "" #string identifier used to indicate set of options.
       
        self.curSugP = None
        self.curSugR = None
        self.curSugW = None

    channelClass = ClientChannel

    
    def Connected(self, channel, addr):
        print('new connection:', channel)
        
        if self.numPlayers >= TOTAL_PLAYERS:
            channel.Send({"action": "rejected", "message": "Too many players!"})        
        else:
            self.playerChannels.append(channel)
            self.players.append(self.game.addPlayer())
            self.numPlayers+=1
            
            if self.numPlayers == TOTAL_PLAYERS:
                #Start the game
                self.game.initializeGame()
                for p in range(len(self.playerChannels)):
                    self.sendCards(p)
                    self.playerChannels[p].Send({"action": "startgame",
                            "player":p, 
                            "numPlayers": TOTAL_PLAYERS})  
                    self.sendMessage("All player's have arrived. Let's begin!", p)
                self.sendPositions()
                self.sendTurns()
       
    #tell all clients all board positions
    def sendPositions(self):
        transmission = {"action": "updatePositions"}
        #add players' positions to the transmission
        for p in range(len(self.players)):
            transmission[str(p)] = self.game.getPlayerLocID(p)
            
        transmission['turn'] = self.game.whoseTurn
            
        #send entire transmission to each player
        for pc in self.playerChannels:
            pc.Send(transmission)
    
    #Send generic message to a player's HUD
    def sendMessage(self, message, playerID):
        transmission = {"action": "message", "message": message}
        self.playerChannels[playerID].Send(transmission)
        
    def sendMessageAll(self, message):
        for p in range(len(self.playerChannels)):
            self.sendMessage(message, p)
      
    def sendTurns(self):
        turn = self.game.whoseTurn
        for p in range(len(self.players)):
            if turn == p:
                self.sendMessage("Your Turn!", p)
            else:
                message = "Waiting for " + self.game.getPlayerName(turn) + "..."
                self.sendMessage(message, p)
                
    def sendCards(self, playerID):
        cardsP = self.game.getPlayerCards(playerID, "P")
        print(cardsP)
        transmission = {"action": "setCards", 
            "cardType": "P", 
            "numCards": len(cardsP)}
        for c in range(len(cardsP)):
            transmission[str(c)] = cardsP[c]
        self.playerChannels[playerID].Send(transmission)
        
        cardsR = self.game.getPlayerCards(playerID, "R")
        transmission = {"action": "setCards", 
            "cardType": "R", 
            "numCards": len(cardsR)}
        for c in range(len(cardsR)):
            transmission[str(c)] = cardsR[c]        
        self.playerChannels[playerID].Send(transmission)
        
        cardsW = self.game.getPlayerCards(playerID, "W")
        transmission = {"action": "setCards", 
            "cardType": "W", 
            "numCards": len(cardsW)}
        for c in range(len(cardsW)):
            transmission[str(c)] = cardsW[c]        
        self.playerChannels[playerID].Send(transmission)
        
        
        
        
        
    #Send generic options to a player's HUD
    def sendOptions(self, options, playerID, clearOthers = True):
        transmission = {"action": "options", "numOptions": len(options)}
        for o in range(len(options)):
            transmission[str(o)] = options[o]
        self.playerChannels[playerID].Send(transmission)
        
        #clear all other user's options
        if clearOthers:
            for p in range(self.numPlayers):
                if p != playerID:
                    transmission = {"action": "options", "numOptions": 0}
                    self.playerChannels[p].Send(transmission)
    
    def clearAllOptions(self):
        for p in range(self.numPlayers):
            transmission = {"action": "options", "numOptions": 0}
            self.playerChannels[p].Send(transmission)
    
    
    def selectOption(self, option, playerID):
        if self.optionSet == "ok":
            self.game.incrementTurn()
            self.clearAllOptions()
            self.sendTurns() 
        elif self.optionSet == "room":               
            if option == 2:
                self.game.incrementTurn()
                self.clearAllOptions()
                self.sendTurns()
                return
            else:
                #cardsL = ROOM_NAMES
                #cardsW = WEAPONS
                if option == 0:
                    self.optionSet = "suggestionP"
                else:
                    self.optionSet = "accusationP"
                self.sendMessage("Who's the muderer?!", playerID)
                self.sendOptions(PLAYER_NAMES[0:TOTAL_PLAYERS], playerID)
        elif self.optionSet == "suggestionP":
            self.curSugP = option
            self.optionSet = "suggestionW"
            self.sendMessage("What was the weapon?", playerID)
            #room must be current room
            self.curSugR = self.game.getPlayerLocID(playerID)
            self.sendOptions(WEAPONS, playerID)
        elif self.optionSet == "suggestionW":
            self.curSugW = option
            self.sendMessageAll(PLAYER_NAMES[playerID] + " suggests: '" +
                                PLAYER_NAMES[self.curSugP] + " in the " +
                                ROOM_NAMES[self.curSugR] + " with the " +
                                WEAPONS[self.curSugW] + "!' Interviewing Witnesses...")
            self.game.makeSuggestion(playerID, self.curSugP, self.curSugR, self.curSugW)
            self.sendPositions()
            self.clearAllOptions()
            self.disprove(playerID)
         
        elif self.optionSet == "accusationP":
            self.curSugP = option
            self.optionSet = "accusationL"
            self.sendMessage("Where did they do it?", playerID)
            self.sendOptions(ROOM_NAMES, playerID)
        elif self.optionSet == "accusationL":
            self.curSugR = option
            self.optionSet = "accusationW"
            self.sendMessage("What was the weapon?", playerID)
            self.sendOptions(WEAPONS, playerID)
        elif self.optionSet == "accusationW":
            self.curSugW = option
            self.optionSet = "ok"
            win = self.game.makeAccusation(self.curSugP, self.curSugR, self.curSugW)
            if win:
                self.clearAllOptions()
                self.sendMessageAll(PLAYER_NAMES[playerID] + " WINS!!")
            else:
                self.clearAllOptions()
                self.sendMessageAll(PLAYER_NAMES[playerID] + " falsely accused... They lose!")
                
        elif self.optionSet == "disprove":
            accuser = self.game.whoseTurn
            disprover = playerID
            if self.disproveCardTypes[option] == "P":
                cardText = PLAYER_NAMES[self.curSugP]
            elif self.disproveCardTypes[option] == "R":
                cardText = ROOM_NAMES[self.curSugR]                
            elif self.disproveCardTypes[option] == "W":
                cardText = WEAPONS[self.curSugW]                

            self.sendMessage(PLAYER_NAMES[disprover] + " shows you a card: " + cardText, accuser)
            self.sendMessage("You show " + PLAYER_NAMES[accuser] + " a card: " + cardText, disprover)
            self.clearAllOptions()
            self.optionSet = "ok"
            self.sendOptions(["OK"], accuser)
            
    
    def disprove(self, accuser):
        disprover = self.game.disproverTurn
        #if disprove turn makes it back to the accuser
        if disprover == accuser:
            self.sendMessageAll("Suggesting was not disproven!!")
            self.clearAllOptions()
            self.game.incrementTurn()
            self.sendTurns()
        else: 
            self.optionSet = "disprove"
            #get from game somehow??
            self.disproveCardTypes = self.game.getSugCards()
            options = []
            for i in range(len(self.disproveCardTypes)):
                if self.disproveCardTypes[i] == "P":
                    options.append("Show card: " + PLAYER_NAMES[self.curSugP])
                elif self.disproveCardTypes[i] == "R":
                    options.append("Show card: " + ROOM_NAMES[self.curSugR])
                elif self.disproveCardTypes[i] == "W":
                    options.append("Show card: " + WEAPONS[self.curSugW])
            
            if len(options) == 0:
                self.game.rotateDisprover()
                self.disprove(accuser)
            else:
                self.sendOptions(options, disprover)

        
try:    
    #To use local active IP address
    s = socket(AF_INET, SOCK_DGRAM) 
    s.connect(('8.8.8.8', 0))
    localIP = s.getsockname()
    #print(localIP)   
    s.close()
    splitIP = str(localIP).split('.')
    onlyIP = str(localIP).split('\'')
    splitIP[3:] = (['0/24'])
    IPRange = ".".join(splitIP)
    #Not needed but saving it
    splitFields = str(localIP).split(',')
    splitIP[1:] = (['55123)'])
    newAddress = ",".join(splitFields)
    myLink = (str(onlyIP[1]),55123)
except:
    print("No network connection found, trying localhost.")
    myLink = ('localhost',55123)
    
print("STARTING SERVER ON " + str(myLink))
gameServe=GameMenuServer(localaddr=myLink)

while True:
    gameServe.Pump()
    sleep(0.01)  
