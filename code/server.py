import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
from game import Game

TOTAL_PLAYERS = 2
    
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
                for p in range(len(self.playerChannels)):
                    self.playerChannels[p].Send({"action": "startgame",
                            "player":p, 
                            "numPlayers": TOTAL_PLAYERS})  
                    self.sendMessage("All player's have arrived. Let's begin!", p)
                    self.sendOptions(["give up", "fight!"], p)
                self.numPlayers+=1   
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
        
    def sendTurns(self):
        for p in range(len(self.players)):
            turn = self.game.whoseTurn
            if turn == p:
                self.sendMessage("Your Turn!", p)
            else:
                message = "Waiting for " + self.game.getPlayerName(turn) + "..."
                self.sendMessage(message, p)

    #Send generic options to a player's HUD
    def sendOptions(self, options, playerID):
        transmission = {"action": "options", "numOptions": len(options)}
        for o in range(len(options)):
            transmission[str(o)] = options[o]
        self.playerChannels[playerID].Send(transmission)        
    
    def selectOption(self, option, playerID):
        print("made it into the selectOption function...")
        print(self.optionSet)
        if self.optionSet == "room":
            print("...with correct option set...")
            if option == 2:
                print("...and correct option.")
                self.game.incrementTurn()
            
    
print("STARTING SERVER ON LOCALHOST")

gameServe=GameMenuServer(localaddr=('localhost', 1337))
while True:
    gameServe.Pump()
    sleep(0.01)