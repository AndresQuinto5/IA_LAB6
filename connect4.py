
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

    def vertical_check(self, row, col):
        """
        Checks for a vertical four-in-a-row starting at the given position.
        """
        consecutive_count = 0
        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break

        if consecutive_count >= 4:
            self.winner = self.players[0] if self.board[row][col].lower() == self.players[0].color.lower() else self.players[1]
            return True
        return False

    def horizontal_check(self, row, col):
        """
        Checks for a horizontal four-in-a-row starting at the given position.
        """
        consecutive_count = 0
        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break

        if consecutive_count >= 4:
            self.winner = self.players[0] if self.board[row][col].lower() == self.players[0].color.lower() else self.players[1]
            return True
        return False

    def diagonal_check(self, row, col):
        """
        Checks for a diagonal four-in-a-row (positive or negative slope) starting at the given position.
        Returns a tuple containing a boolean indicating if a four-in-a-row was found and the slope ('positive', 'negative', or 'both').
        """
        four_in_a_row = False
        slope = None

        # Check for diagonals with positive slope
        consecutive_count = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1

        if consecutive_count >= 4:
            four_in_a_row = True
            slope = 'positive'
            self.winner = self.players[0] if self.board[row][col].lower() == self.players[0].color.lower() else self.players[1]

        # Check for diagonals with negative slope
        consecutive_count = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1

        if consecutive_count >= 4:
            four_in_a_row = True
            slope = 'negative' if slope is None else 'both'
            self.winner = self.players[0] if self.board[row][col].lower() == self.players[0].color.lower() else self.players[1]

        return four_in_a_row, slope

    def print_state(self):
        """
        Clears the screen and prints the current game state.
        """
        os.system(['clear', 'cls'][os.name == 'nt'])
        print(u"{0}!".format(self.game_name))
        print("Round: " + str(self.round))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner is not None:
                print(f"{self.winner.name} is the winner")
            else:
                print("Game was a draw")

class Player:
    """
    Player object for human players.
    """

    def __init__(self, name, color):
        self.type = "Human"
        self.name = name
        self.color = color

    def move(self, state):
        """
        Prompts the human player to enter a move (by column number).
        """
        print(f"{self.name}'s turn. {self.name} is {self.color}")
        column = None
        while column is None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column

class AIPlayer(Player):
    """
    AIPlayer object that extends the Player class.
    The AI algorithm is minimax with optional alpha-beta pruning.
    """

    def __init__(self, name, color, difficulty=5, use_alpha_beta=True):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty
        self.use_alpha_beta = use_alpha_beta

    def move(self, state):
        """
        Determines the best move for the AI player using the minimax algorithm with optional alpha-beta pruning.
        """
        print(f"{self.name}'s turn. {self.name} is {self.color}")
        minimax = Minimax(state)
        best_move, _ = minimax.minimax(self.difficulty, state, self.color, self.use_alpha_beta)
        return best_move
