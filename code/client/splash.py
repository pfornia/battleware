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
        self.blue = (0,0,255)
        self.white = (255 , 255 , 255)
        self.font = 'freesansbold.ttf'
        self.fontSize = 40
        self.fontPos = (25 , 20)
        self.secSleep = 3
        self.destRect = (0 , 0)
        self.splashSize = (500 , 80)

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init( )

        if not pygame.font.get_init( ):
            pygame.font.init( )
            if not pygame.font.get_init( ):
                raise RuntimeError( "pygame doesn't init" )

        self.font = pygame.font.Font( self.font , self.fontSize )
        if not self.font:
            print( "No font." )

        self.screen = pygame.display.set_mode( self.splashSize , pygame.NOFRAME )
        self.background = pygame.Surface( self.screen.get_size( ) )
        self.background.fill( self.black )

        try:
            s = threading.Thread( name='splash1' , target=self.run )
            s.setDaemon( True )
            s.start( )
            s.join()
        except:
            print("Splash error")

    def run(self):
        print( "Splash message." )
        self.screen.blit( self.background , self.destRect )
        self.screen.blit(self.font.render( 'Starting up Clue-Less...' , True , self.white ),self.fontPos )
        pygame.display.update( )
        time.sleep( self.secSleep )

#showIt=splashScreen()

