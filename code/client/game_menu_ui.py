from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import os, sys
import pygame
from pygame.locals import *

#def main():

PLAYER_NAMES = ["Miss Scarlet",
    "Col Mustard",
    "Mrs White",
    "Mr Green",
    "Mrs Peacock",
    "Prof Plum"]

class GameMenu(ConnectionListener):
    '''
    GameMenu is the UI for the clue game (client side)
    
    Many code snippets taken from 
    
    
        pygame.org tutorials
        (especially https://www.pygame.org/docs/tut/ChimpLineByLine.html),
        https://www.raywenderlich.com/38732/multiplayer-game-programming-for-teens-with-python
        and
        https://www.raywenderlich.com/46843/multiplayer-game-programming-for-teens-with-python-part-2
    
    '''
    
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.size = width, height = 1000, 600
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Clue-Less!")
        
        self.titleMessage = "Waiting for more players..."
        self.serverMessage = ""
        
        #initialize pygame clock
        self.clock=pygame.time.Clock()
        
        #clear the screen
        self.screen.fill(0)
        
        self.locations = []
        self.locations.append(LocationIcon(500, 100, "study.jpg"))
        self.locations.append(LocationIcon(700, 100, "hall.jpg"))
        self.locations.append(LocationIcon(900, 100, "lounge.jpg"))
        
        self.locations.append(LocationIcon(500, 300, "library.jpg"))
        self.locations.append(LocationIcon(700, 300, "billiard.jpg"))
        self.locations.append(LocationIcon(900, 300, "dining.jpg"))
        
        self.locations.append(LocationIcon(500, 500, "conservatory.jpg"))
        self.locations.append(LocationIcon(700, 500, "ballroom.jpg"))
        self.locations.append(LocationIcon(900, 500, "kitchen.jpg"))
        
        #Hallways
        self.locations.append(LocationIcon(600, 100, "hallway_horiz.jpg"))
        self.locations.append(LocationIcon(800, 100, "hallway_horiz.jpg"))
        
        self.locations.append(LocationIcon(500, 200, "hallway_vert.jpg"))
        self.locations.append(LocationIcon(700, 200, "hallway_vert.jpg"))
        self.locations.append(LocationIcon(900, 200, "hallway_vert.jpg"))
        
        self.locations.append(LocationIcon(600, 300, "hallway_horiz.jpg"))
        self.locations.append(LocationIcon(800, 300, "hallway_horiz.jpg"))
        
        self.locations.append(LocationIcon(500, 400, "hallway_vert.jpg"))
        self.locations.append(LocationIcon(700, 400, "hallway_vert.jpg"))
        self.locations.append(LocationIcon(900, 400, "hallway_vert.jpg"))
        
        self.locations.append(LocationIcon(600, 500, "hallway_horiz.jpg"))
        self.locations.append(LocationIcon(800, 500, "hallway_horiz.jpg"))
        
        self.playerIcons = []
        self.playerIcons.append(PlayerIcon("scarlet.jpg"))
        self.playerIcons.append(PlayerIcon("mustard.jpg"))
        self.playerIcons.append(PlayerIcon("white.jpg"))
        self.playerIcons.append(PlayerIcon("green.jpg"))
        
        
        self.gameStarted = False
        
        self.numPlayers = 0
        
        self.Connect(('localhost', 1337))
        
        '''
        self.running=False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)
        #determine attributes from player #
        if self.num==0:
            self.turn=True
            self.marker = self.greenplayer
            self.othermarker = self.blueplayer
        else:
            self.turn=False
            self.marker=self.blueplayer
            self.othermarker = self.greenplayer
        '''
    def update(self):
    
        connection.Pump()
        self.Pump()
        
        #sleep to make the game 60 fps
        self.clock.tick(60)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                
                mouse = pygame.mouse.get_pos()
                for l in range(len(self.locations)):
                    if self.locations[l].rect.collidepoint(mouse):
                        print(l)
                        self.Send({"action": "move", 
                            "client": self.myPlayerID,
                            "l":l})
                
            self.screen.fill([0, 0, 0])

        for l in self.locations:
            self.screen.blit(l.image, l.rect)

        for p in self.playerIcons:
            self.screen.blit(p.image, p.rect)            


        # Title message
        #create font
        myfont1 = pygame.font.SysFont(None, 32)
        myfont2 = pygame.font.SysFont(None, 24)

        #create text surface
        labelTitle = myfont1.render(self.titleMessage, 1, (255,255,255))
        labelServer = myfont2.render(self.serverMessage, 1, (255,255,255))

        #draw surface
        self.screen.blit(labelTitle, (10, 20))
        self.screen.blit(labelServer, (50, 70))

        
        pygame.display.flip()
                    
    def Network_startgame(self, data):
        #self.running=True
        self.myPlayerID=data["player"]
        self.numPlayers=data["numPlayers"]
        #self.gameid=data["gameid"]
        self.gameStarted = True
        self.titleMessage = "Welcome " + PLAYER_NAMES[self.myPlayerID] + "!"
        print(self.myPlayerID)

    def Network_updatePositions(self, data):
        #self.running=True
        print("updating positions...")
        print(data)
        #by putting icons on different portions of the square, they won't overlap.
        self.playerIcons[0].rect.topleft = self.locations[data['0']].rect.topleft
        if self.numPlayers > 1:
            self.playerIcons[1].rect.topright = self.locations[data['1']].rect.topright
        if self.numPlayers > 2:
            self.playerIcons[2].rect.bottomleft = self.locations[data['2']].rect.bottomleft
        if self.numPlayers > 3:
            self.playerIcons[3].rect.bottomright = self.locations[data['3']].rect.bottomright
                    
                    
    def Network_message(self, data):
        self.serverMessage = data['message']
    
    
class LocationIcon(object):
    '''
    Room or hallway icon on the board
    '''
    
    def __init__(self, coordX, coordY, iconFile):
        self.name = iconFile
        self.image, self.rect = load_image(iconFile, -1)
        #self.rect.inflate_ip(-100, -100)
        self.rect.center = [coordX, coordY]
        
class PlayerIcon(object):
    '''
    Player Icon on the board
    '''
    
    def __init__(self, iconFile):
        self.name = iconFile
        self.image, self.rect = load_image(iconFile, -1, location = False)    
        #hide unused players off screen
        self.rect.center = [-100, 0]
        
def load_image(name, colorkey=None, location = True):
    fullname = os.path.join('icons/', name)
    #weird python 2 syntax?? Doesn't work.
    '''
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
    '''
    image = pygame.image.load(fullname)
    image = image.convert()
    ##How to resize an image?!?
    if location:
        image = pygame.transform.scale(image, (100,100))
    else:
        image = pygame.transform.scale(image, (30,50))
    return image, image.get_rect()
        
thisUI = GameMenu()

while 1:
    thisUI.update()       

#main()