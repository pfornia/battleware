# May not need this file eventually.
#  but useful for testing.

#assume exactly 2 players.

from game import Game

thisGame = Game()

#for l in thisGame.locations:
    #print(l.isRoom)
        
me1 = thisGame.addPlayer()

print(me1)

me2 = thisGame.addPlayer()

print(me2)

me3 = thisGame.addPlayer()

print(me3)

print(thisGame.getPlayerLocID(me1))
print(thisGame.locations[10].occupants)
#print(me3.getLocation().name)
print(thisGame.makeMove(me1, 2))

print(thisGame.getPlayerLocID(me1))
print(thisGame.locations[10].occupants)

#print(me3.getLocation().name)
