import os, sys
import pygame
from pygame.locals import *

def main():
    from game_menu_ui import GameMenu

    thisUI = GameMenu()

    while 1:
        thisUI.update()       


class GameMenu(object):
    """
    GameMenu is the UI for the clue game (client side)
    
    Many code snippets taken from 
    
    
        pygame.org tutorials
        (especially https://www.pygame.org/docs/tut/ChimpLineByLine.html),
        https://www.raywenderlich.com/38732/multiplayer-game-programming-for-teens-with-python
        and
        https://www.raywenderlich.com/46843/multiplayer-game-programming-for-teens-with-python-part-2
    
    """
    
    def __init__(self):
        pygame.init()
        self.size = width, height = 1000, 600
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Clue-Less!")
        
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
        
        

    def update(self):
        #sleep to make the game 60 fps
        self.clock.tick(60)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                
                print("Clickity-click!")
                
                mouse = pygame.mouse.get_pos()
                for l in range(len(self.locations)):
                    if self.locations[l].rect.collidepoint(mouse):
                        print(l)
                
            self.screen.fill([0, 0, 0])

        for l in self.locations:
            self.screen.blit(l.image, l.rect)
            
            
        #if pygame.mouse.get_pressed()[0]:
        #    print("hello!")
            
        pygame.display.flip()
                
class LocationIcon(object):
    """
    Room or hallway icon on the board
    """
    
    def __init__(self, coordX, coordY, iconFile):
        self.name = iconFile
        self.image, self.rect = load_image(iconFile, -1)
        #self.rect.inflate_ip(-100, -100)
        self.rect.center = [coordX, coordY]
        
def load_image(name, colorkey=None):
    fullname = os.path.join('icons/', name)
    #weird python 2 syntax?? Doesn't work.
    """
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
    """
    image = pygame.image.load(fullname)
    image = image.convert()
    ##How to resize an image?!?
    image = pygame.transform.scale(image, (100,100))
    return image, image.get_rect()
    
    
main()