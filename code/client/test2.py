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
testPlayers=("player1", "player2","player3","player4")

testGame = Game()

for x in testPlayers:
    x
    
testPlayer1 = testGame.addPlayer()
testPlayer2 = testGame.addPlayer()
testPlayer3 = testGame.addPlayer()
testPlayer4 = testGame.addPlayer()

newGame = testGame.initializeGame()



print("\nTest End")
