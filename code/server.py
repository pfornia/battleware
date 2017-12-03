import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
from game import Game

TOTAL_PLAYERS = 2

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print(data)

    def Network_doThing(self, data):
        #self.running=True
        #self.num=data["player"]
        #self.gameid=data["gameid"]
        self._server.doThing()
        
    def Network_move(self, data):
        player = self._server.players[data["client"]]
        self._server.game.makeMove(player, data["l"])
        #send updated positions
        self._server.sendPositions()
        
     
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
                            "name":self.players[p].name,
                            "numPlayers": TOTAL_PLAYERS})      
                self.numPlayers+=1   
                self.sendPositions()
       
    #tell all clients all board positions
    def sendPositions(self):
        message = {"action": "updatePositions"}
        #add players' positions to the message
        for p in range(len(self.players)):
            message[str(p)] = self.game.locations.index(self.players[p].curLocation)
            
        #send entire message to each player
        for pc in self.playerChannels:
            pc.Send(message)
    
print("STARTING SERVER ON LOCALHOST")

gameServe=GameMenuServer(localaddr=('localhost', 1337))
while True:
    gameServe.Pump()
    sleep(0.01)