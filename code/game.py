from card_controller import CardController
from player import Player
from location import Location

class Game(object):
    """An instance of a single game of "Clue-less"

    Attributes:
        player: A list of players
        locations: A set of locations
        whosTurn: The index of the player whos 
        cardController: CardController object for this game.
    """

    def __init__(self):
        """Return an initialized Game object"""
        #start with zero indexed player
        self.whosTurn = 0
        #todo: initialize empty players list
        self.players = []
        #todo: initialize complete list of all rooms and hallways
        self.locations = []
        #todo: initialize CardControllerClass
        self.cardController = CardController()
        print("game initialized!")
        

    def addPlayer(self, Player):
        """Adds player to game, by initializing
        player object into the player list and 
        returning the index of the new player"""
        #todo: add player to end of player list
        #self.players = ...???
        
    def notify(self, amount):
        """Does this return information up??"""
        #???
        
    def initializeGame(self):
        ## This is run once all players are signed in and ready to start... right?
        self.cardController.distributeCards()