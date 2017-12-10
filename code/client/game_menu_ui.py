from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import os, sys
import pygame
from pygame.locals import *

from socket import socket, SOCK_DGRAM, AF_INET 
import socketserver

#def main():

PLAYER_NAMES = ["Miss Scarlet",
    "Col Mustard",
    "Mrs White",
    "Mr Green",
    "Mrs Peacock",
    "Prof Plum"]
    
WEAPONS = ["Rope",
    "Lead Pipe",
    "Knife",
    "Wrench",
    "Candlestick",
    "Revolver"]
    
ROOM_NAMES = ["Study",
    "Hall",
    "Lounge",
    "Library",
    "Billiard Room",
    "Dining Room",
    "Conservatory",
    "Ballroom",
    "Kitchen"]

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
        self.serverOptions = []
        self.serverOptionsButtons = []
        self.cardsP = []
        self.cardsR = []
        self.cardsW = []
        
        #initialize pygame clock
        self.clock=pygame.time.Clock()
        
        #clear the screen
        self.screen.fill(0)
        
        self.locations = []
        self.locations.append(LocationIcon(530, 130, "study.jpg"))
        self.locations.append(LocationIcon(730, 130, "hall.jpg"))
        self.locations.append(LocationIcon(930, 130, "lounge.jpg"))
        
        self.locations.append(LocationIcon(530, 330, "library.jpg"))
        self.locations.append(LocationIcon(730, 330, "billiard.jpg"))
        self.locations.append(LocationIcon(930, 330, "dining.jpg"))
        
        self.locations.append(LocationIcon(530, 530, "conservatory.jpg"))
        self.locations.append(LocationIcon(730, 530, "ballroom.jpg"))
        self.locations.append(LocationIcon(930, 530, "kitchen.jpg"))
        
        #Hallways
        self.locations.append(LocationIcon(630, 130, "hallway_horiz.jpg"))
        self.locations.append(LocationIcon(830, 130, "hallway_horiz.jpg"))
       
        self.locations.append(LocationIcon(530, 230, "hallway_vert.jpg"))
        self.locations.append(LocationIcon(730, 230, "hallway_vert.jpg"))
        self.locations.append(LocationIcon(930, 230, "hallway_vert.jpg"))
        
        self.locations.append(LocationIcon(630, 330, "hallway_horiz.jpg"))
        self.locations.append(LocationIcon(830, 330, "hallway_horiz.jpg"))
       
        self.locations.append(LocationIcon(530, 430, "hallway_vert.jpg"))
        self.locations.append(LocationIcon(730, 430, "hallway_vert.jpg"))
        self.locations.append(LocationIcon(930, 430, "hallway_vert.jpg"))
        
        self.locations.append(LocationIcon(630, 530, "hallway_horiz.jpg"))
        self.locations.append(LocationIcon(830, 530, "hallway_horiz.jpg"))
        
        self.playerIcons = []
        self.playerIcons.append(PlayerIcon("scarlet.jpg"))
        self.playerIcons.append(PlayerIcon("mustard.jpg"))
        self.playerIcons.append(PlayerIcon("white.jpg"))
        self.playerIcons.append(PlayerIcon("green.jpg"))
        
        
        self.gameStarted = False
        
        self.numPlayers = 0
        
        try:
            #To use local active IP address
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            localIP = s.getsockname()
            #print(localIP)   
            s.close()
            splitIP = str(localIP).split('.')
            onlyIP = str(localIP).split('\'')
            splitIP[3:] = (['0/24'])
            IPRange = ".".join(splitIP)
            #Not needed but saving it
            splitFields = str(localIP).split(',')
            splitIP[1:] = (['1338)'])
            newAddress = ",".join(splitFields)
            myLink = (str(onlyIP[1]),1338)
        except:
            print("No network connection found, trying localhost.")
            myLink = ('localhost',1339)
        
        #wanLink = ('bw.nathansdoorway.com', 55123)
        
        #print("STARTING CLIENT ON " + str(wanLink))
        
        #self.Connect(wanLink)
        self.Connect(myLink)
        
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
                            
                for b in range(len(self.serverOptionsButtons)):
                    if self.serverOptionsButtons[b].rect.collidepoint(mouse):
                        print(b)
                        self.Send({"action": "selectOption", 
                            "client": self.myPlayerID,
                            "o":b})                    
                
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
        self.screen.blit(labelServer, (20, 40))
        
        self.screen.blit(labelTitle, (10, 8))
        curY = 80
        curX = 50
        
        for o in range(len(self.serverOptions)):
            button = self.serverOptionsButtons[o]
            button.rect.topleft = [curX - 3, curY - 3]
            self.screen.blit(button.image, button.rect)
            labelOption = myfont2.render(str(o+1) + ")  " + self.serverOptions[o], 1, (255,255,255))
            self.screen.blit(labelOption, (50, curY))
            curY += 30
        
        # List cards
        
        topY = 360
                
        labelCards = myfont2.render("My Cards:", 1, (255,255,255))
        self.screen.blit(labelCards, (curX, topY))
        
        curX0 = curX
        curX1 = curX + 120
        curX2 = curX + 240

        #Players
        curY = topY + 60
        labelCardsP = myfont2.render("Players:", 1, (255,255,255))
        self.screen.blit(labelCardsP, (curX0, topY + 30))
        for c in self.cardsP:
            thisCard = myfont2.render(c, 1, (255,255,255))
            self.screen.blit(thisCard, (curX0, curY))
            curY += 22

        #Rooms
        curY = topY + 60
        labelCardsR = myfont2.render("Rooms:", 1, (255,255,255))
        self.screen.blit(labelCardsR, (curX1, topY + 30))
        for c in self.cardsR:
            thisCard = myfont2.render(c, 1, (255,255,255))
            self.screen.blit(thisCard, (curX1, curY))
            curY += 22           

        #Weapons
        curY = topY + 60
        labelCardsW = myfont2.render("Weapons:", 1, (255,255,255))
        self.screen.blit(labelCardsW, (curX2, topY + 30))
        for c in self.cardsW:
            thisCard = myfont2.render(c, 1, (255,255,255))
            self.screen.blit(thisCard, (curX2, curY))
            curY += 22            
            
        pygame.display.flip()
                    
    def Network_startgame(self, data):
        #self.running=True
        self.myPlayerID=data["player"]
        self.numPlayers=data["numPlayers"]
        #self.gameid=data["gameid"]
        self.gameStarted = True
        self.titleMessage = "Welcome " + PLAYER_NAMES[self.myPlayerID] + "!"

    def Network_setCards(self, data):
        
        #Set cards to corresponding list
        if data["cardType"] == "P":
            for c in range(data["numCards"]):
                self.cardsP.append(PLAYER_NAMES[data[str(c)]])
        elif data["cardType"] == "R":
            for c in range(data["numCards"]):
                self.cardsR.append(ROOM_NAMES[data[str(c)]])
        elif data["cardType"] == "W":
            for c in range(data["numCards"]):
                self.cardsW.append(WEAPONS[data[str(c)]])
            
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
    
    def Network_options(self, data):
        
        #reset options to blank
        self.serverOptions = []
        self.serverOptionsButtons = []
        
        for o in range(data['numOptions']):
            self.serverOptions.append(data[str(o)])
            self.serverOptionsButtons.append(ButtonIcon("button2.jpg"))
            
    
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
        self.image, self.rect = load_image(iconFile, -1, xDim = 30, yDim = 50)    
        #hide unused players off screen
        self.rect.center = [-100, 0]

class ButtonIcon(object):
    '''
    Button Icon on the board
    '''
    
    def __init__(self, iconFile):
        self.name = iconFile
        self.image, self.rect = load_image(iconFile, -1, xDim = 350, yDim = 24)    
        #hide unused players off screen
        self.rect.center = [-100, 0]
        
def load_image(name, colorkey=None, xDim = 100, yDim = 100):
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
    image = pygame.transform.scale(image, (xDim,yDim))
    #image = pygame.transform.scale(image, (30,50))
    return image, image.get_rect()
        
thisUI = GameMenu()

while 1:
    thisUI.update()       

#main()