
import os
import time
from minimax import Minimax

class Game:
    """
    Game object that holds the state of the Connect 4 board and game values.
    """

    def __init__(self):
        # Initialize game variables
        self.round = 1
        self.finished = False
        self.winner = None
        self.turn = None
        self.players = [None, None]
        self.game_name = u"Connect four IA_LAB06"
        self.colors = ["x", "o"]

        # Clear the screen and display the welcome message
        os.system(['clear', 'cls'][os.name == 'nt'])
        print(u"Welcome to {0}!".format(self.game_name))

        # Prompt for player types and create player objects
        self.create_players()

        # Set the first player's turn
        self.turn = self.players[0]

        # Initialize the board
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
