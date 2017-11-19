# May not need this file eventually.
#  but useful for testing.

from game import Game

thisGame = Game()

for l in thisGame.locations:
    print(l.name + " neigbors:")
    for al in l.adjLocations:
        print(al.name)
        
me1 = thisGame.addPlayer()

print(me1.curLocation.name)