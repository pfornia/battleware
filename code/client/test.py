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

serverFileName = "../server.py"
clientFileName = "game_menu_ui.py"
testPlayers=[]

testPlayers.append("Michael")
testPlayers.append("Alice")
testPlayers.append("Peter")
testPlayers.append("Hercules")
testPlayersCount = len(testPlayers)

def startServer():
        print(threading.currentThread().getName(), ' Started a Server thread.')
        call(["python3.4",serverFileName])
        time.sleep(2)
        print(threading.currentThread().getName(), ' Ended a Server thread.')
        #Code for Server thread monitors thread count and exit
        t_end = time.monotonic() + 10
        while time.monotonic() < t_end:
            #Wait for other threads to startServer
            time.sleep(1)
        while threading.active_count() > 1:
            time.sleep(1)
            if threading.active_count() < 3:
                TestServer._stop = True
                break
            break

def startBoardGame():
    print(threading.currentThread().getName(), ' Started a client thread.')
    call(["python3.4",clientFileName])
    time.sleep(2)
    print(threading.currentThread().getName(), ' Ended a client thread.')

TestServer = threading.Thread(name='Server', target=startServer)
TestServer.setDaemon(False)
TestServer.start()
TestServer._stop = threading.Event()
TestServer.lock = threading.Lock()
#TestServer.shut = threading._shutdown()
mainThread = threading.main_thread
mainThread._stop = threading.Event()
time.sleep(1)

for i in testPlayers:
    i = threading.Thread(name=i, target=startBoardGame)
    i.setDaemon(True)
    time.sleep(2)
    i.start()

while threading.active_count() > 1:
    time.sleep(1)
    if threading.active_count() == 2:
       # TestServer._stop.set()
        #TestServer.shutdown = True
        print("All clients should exited by now.")
        #TestServer._tstate_lock = None
        #TestServer._wait_for_tstate_lock()
        TestServer.lock = None
        #TestServer.join()
        print("Threads left: ", threading.active_count())
        input("Press Enter to end the test...")
        TestServer._stop = True
        break
    
print("\nTest End. Press Ctl + c to exit.")



