import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
from game import Game

from socket import socket, SOCK_DGRAM, AF_INET 
import socketserver

TOTAL_PLAYERS = 2
    
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
        self.curSugL = None
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
        for p in range(len(self.players)):
            turn = self.game.whoseTurn
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
        if self.optionSet == "room":               
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
                self.sendOptions(PLAYER_NAMES[0:TOTAL_PLAYERS], playerID)
        elif self.optionSet == "suggestionP":
            print("hello")
            self.curSugP = option
            self.optionSet = "suggestionL"
            self.sendOptions(ROOM_NAMES, playerID)
        elif self.optionSet == "suggestionL":
            self.curSugL = option
            self.optionSet = "suggestionW"
            self.sendOptions(WEAPONS, playerID)
        elif self.optionSet == "suggestionW":
            self.curSugW = option
            self.optionSet = "disprove"
            self.sendMessageAll("Interviewing witnesses...")
            self.game.makeSuggestion(playerID, self.curSugP, self.curSugL, self.curSugW)
            #self.sendOptions(???, ??playerID??)
            
            print("suggestion: ", self.curSugP, self.curSugL, self.curSugW)
            
        elif self.optionSet == "accusationP":
            print("hello")
            self.curSugP = option
            self.optionSet = "accusationL"
            self.sendOptions(ROOM_NAMES, playerID)
        elif self.optionSet == "accusationL":
            self.curSugL = option
            self.optionSet = "accusationW"
            self.sendOptions(WEAPONS, playerID)
        elif self.optionSet == "accusationW":
            self.curSugW = option
            self.optionSet = "ok"
            win = self.game.makeAccusation(self.curSugP, self.curSugL, self.curSugW)
            if win:
                self.clearAllOptions()
                self.sendMessageAll(PLAYER_NAMES[playerID] + " WINS!!")
            #self.sendOptions(???, ??playerID??)    
            
        
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
    splitIP[1:] = (['1338)'])
    newAddress = ",".join(splitFields)
    myLink = (str(onlyIP[1]),1338)
except:
    print("No network connection found, trying localhost.")
    myLink = ('localhost',1339)

print("STARTING SERVER ON " + str(myLink))
gameServe=GameMenuServer(localaddr=myLink)

while True:
    gameServe.Pump()
    sleep(0.01)  
