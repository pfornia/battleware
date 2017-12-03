#To test adding players and 

import PodSixNet.Channel
import PodSixNet.Server
#from client.server import *
#import client.game_menu_ui
from game import Game
from card_controller import CardController
from card_controller import Card
from location import Location
from player import Player
#from client.server import ClientChannel
import compileall
import threading
import time
from subprocess import check_output, call

serverFileName = "client/server.py"
clientFileName = "client/game_menu_ui.py"
testPlayers=[]

testPlayers.append("Michael")
testPlayers.append("Alice")
testPlayers.append("Peter")
testPlayers.append("Hercules")
testPlayersCount = len(testPlayers)
myPyFile = "client/server.py"

def startServer():
    print(threading.currentThread().getName(), 'Started')
    compiled = compile('',serverFileName, 'exec')
    exec(compiled)
    time.sleep(10)
    #exec(open(myPyFile).read())
    #exec(open("./client/server.py").read())
    #call('python3.4 /server.py')
    print(threading.currentThread().getName(), 'Ended')
    
          
def startBoardGame():
    print(threading.currentThread().getName(), 'joined the game')
    compiled = compile('',clientFileName, 'exec')
    exec(compiled)
    time.sleep(2)
    print(threading.currentThread().getName(), 'left the game')

TestServer = threading.Thread(name='Server', target=startServer)
TestServer.setDaemon(True)
TestServer.start()
time.sleep(1)

for i in testPlayers:
    i = threading.Thread(name=i, target=startBoardGame)
    i.setDaemon(True)
    i.start()

#for i in testPlayers:
#    i.join()
#    print(i)
    
#for thread in threading.enumerate():
    #thread.join()
    #print(thread.name)    

TestServer.join()
        
print("\nTest End")
