import os, sys
import pygame
from pygame.locals import *

def main():
    from game_menu_ui import GameMenu

    thisUI = GameMenu()
    


class GameMenu(object):
    """
    GameMenu is the UI for the clue game (client side)
    
    Many code snippets taken from pygame.org tutorials,
        especially https://www.pygame.org/docs/tut/ChimpLineByLine.html
    
    """
    
    def __init__(self):
        pygame.init()
        size = width, height = 1000, 600
        screen = pygame.display.set_mode(size)
        
        locations = []
        locations.append(LocationIcon(150, 100, "study.jpg"))
        locations.append(LocationIcon(500, 100, "hall.jpg"))
        locations.append(LocationIcon(850, 100, "lounge.jpg"))
        
        locations.append(LocationIcon(150, 300, "library.jpg"))
        locations.append(LocationIcon(500, 300, "billiard.jpg"))
        locations.append(LocationIcon(850, 300, "dining.jpg"))
        
        locations.append(LocationIcon(150, 500, "conservatory.jpg"))
        locations.append(LocationIcon(500, 500, "ballroom.jpg"))
        locations.append(LocationIcon(850, 500, "kitchen.jpg"))
                
        
        while 1:
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            
                screen.fill([0, 0, 0])
                for l in locations:
                    screen.blit(l.image, l.rect)
                pygame.display.flip()

class LocationIcon(object):
    """
    Room or hallway icon on the board
    """
    
    def __init__(self, coordX, coordY, iconFile):
        self.image, self.rect = load_image(iconFile, -1)
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
    return image, image.get_rect()
    
    
main()