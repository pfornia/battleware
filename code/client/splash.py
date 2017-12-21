#! /usr/bin/env python

import pygame
import time
import os
import threading


class splashScreen(object):
    '''
    A simple splash logo with a timer,
    Will eventually make it monitor loading and close once loading done.
    '''

    def __init__(self):
        self.black = (0 , 0 , 0)
        self.white = (255 , 255 , 255)
        self.font = 'freesansbold.ttf'
        self.fontSize = 40
        self.fontPos = (25 , 20)
        self.secSleep = 2
        self.destRect = (0 , 0)
        self.splashSize = (500 , 80)

        print( "Splash load..." )
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init( )
        pygame.font.init( )

        try:
            splashScreen = threading.Thread( name='splash1' , target=self.run )
            splashScreen.setDaemon( True )
            splashScreen.start( )
        except:
            print("Splash out")

    def run(self):

        screen = pygame.display.set_mode( self.splashSize , pygame.NOFRAME )

        background = pygame.Surface( self.screen.get_size( ) )
        background.fill( self.black )
        screen.blit( background , self.destRect )
        screen.blit(pygame.font.Font( self.font , self.fontSize ).render( 'Starting up Clue-Less...' , True , self.white ) ,
            self.fontPos )
        pygame.display.update( )
        time.sleep( self.secSleep )


'''
#! /usr/bin/env python
import pygame
import time
import os, sys
print 'Splash load...'
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((500,80),pygame.NOFRAME)
background = pygame.Surface(screen.get_size())
background.fill((2,24,244))
screen.blit(background, (0,0))
screen.blit(pygame.font.Font('pala.ttf', 72).render('Loading...', 1, (255,255,255)), (90,10))
pygame.display.update()
time.sleep(5)
'''
