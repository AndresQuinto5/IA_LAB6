
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

    def create_players(self):
        """
        Prompts the user to choose player types (Human or Computer) and creates player objects.
        """
        for i in range(2):
            while self.players[i] is None:
                choice = input(f"Should Player {i + 1} be a Human or a Computer? Type 'H' or 'C': ").lower()
                if choice == 'h':
                    name = input(f"What is Player {i + 1}'s name? ")
                    self.players[i] = Player(name, self.colors[i])
                elif choice == 'c':
                    name = input(f"What is Player {i + 1}'s name? ")
                    use_alpha_beta = input(f"Do you want to use alpha-beta pruning for {name}? (y/n) ").lower() == 'y'
                    self.players[i] = AIPlayer(name, self.colors[i], 5, use_alpha_beta)
                else:
                    print("Invalid choice, please try again.")
            print(f"{self.players[i].name} will be {self.colors[i]}")

    def new_game(self):
        """
        Resets the game state for a new game.
        """
        self.round = 1
        self.finished = False
        self.winner = None
        self.turn = self.players[0]
        self.board = [[' ' for _ in range(7)] for _ in range(6)]

    def switch_turn(self):
        """
        Switches the turn between players and increments the round.
        """
        self.turn = self.players[1] if self.turn == self.players[0] else self.players[0]
        self.round += 1

    def next_move(self):
        """
        Handles the next move in the game.
        """
        player = self.turn

        # Check if the game has reached the maximum number of moves
        if self.round > 42:
            self.finished = True
            return

        # Get the move from the current player
        move = player.move(self.board)

        # Check if the move is valid and make the move
        for i in range(6):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switch_turn()
                self.check_for_fours()
                self.print_state()
                return

        # If the column is full, print an error message
        print("Invalid move (column is full)")

    def check_for_fours(self):
        """
        Checks the board for any four-in-a-row and updates the game status accordingly.
        """
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    if self.vertical_check(i, j):
                        self.finished = True
                        return
                    if self.horizontal_check(i, j):
                        self.finished = True
                        return
                    diag_fours, _ = self.diagonal_check(i, j)
                    if diag_fours:
                        self.finished = True
                        return
