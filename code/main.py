# May not need this file eventually.
#  but useful for testing.

#assume exactly 2 players.

from game import Game

thisGame = Game()

#for l in thisGame.locations:
    #print(l.isRoom)
        
me1 = thisGame.addPlayer()

print(me1.name)

me2 = thisGame.addPlayer()

print(me2.name)

me3 = thisGame.addPlayer()

print(me3.name)


print(me3.getLocation().name)
thisGame.makeMove(me3, thisGame.locations[0])
print(me3.getLocation().name)
