#To test adding players and 
import sys
sys.path.append("..")

from game import Game
from card_controller import CardController
from card_controller import Card
from location import Location
from player import Player
#from client.server import ClientChannel
import compileall
import threading
import time
from subprocess import check_output, call, Popen

serverFileName = "server.py"
clientFileName = "game_menu_ui.py"
testPlayers=[]

testPlayers.append("Michael")
testPlayers.append("Alice")
testPlayers.append("Peter")
testPlayers.append("Hercules")
testPlayersCount = len(testPlayers)

def startServer():
    print(threading.currentThread().getName(), 'Executing Server')
    #compiled = compile('',serverFileName, 'exec')
    #exec(compiled)
    
    call(["python3.4",serverFileName])
    time.sleep(2)
    #exec(open(myPyFile).read())
    #exec(open("./client/server.py").read())
    #call('python3.4 /server.py')
    print(threading.currentThread().getName(), 'Closing Server')
    
          
def startBoardGame():
    print(threading.currentThread().getName(), 'Executing a client session')
    call(["python3.4",clientFileName])
    time.sleep(2)
    print(threading.currentThread().getName(), 'Closed a client session')

TestServer = threading.Thread(name='', target=startServer)
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
i.join()    
#for thread in threading.enumerate():
    #thread.join()
    #print(thread.name)    
time.sleep(5)

#TestServer.join()
        
print("\nTest End")
