# May not need this file eventually.
#  but useful for testing.

from game import Game

thisGame = Game()

#for l in thisGame.locations:
    #print(l.isRoom)
        
me1 = thisGame.addPlayer()

print(me1.name)

me2 = thisGame.addPlayer()

print(me2.name)


