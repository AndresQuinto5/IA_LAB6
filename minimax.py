import random
class Minimax:
    """
    Minimax object that takes a current Connect 4 board state and performs the minimax algorithm with alpha-beta pruning.
    """

    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.colors = ["x", "o"]

    # def random_move(self, state, curr_player):
    #     """
    #     Selects a random legal move from the available moves.
    #     """
    #     legal_moves = [col for col in range(7) if self.is_legal_move(col, state)]
    #     if legal_moves:
    #         return random.choice(legal_moves)
    #     else:
    #         return None
        
    def minimax(self, depth, state, curr_player, use_alpha_beta=True):
        """
        Implements the minimax algorithm with optional alpha-beta pruning to find the best move and its associated value.
        Returns the best move (as a column number) and the associated value.
        """
        best_move = None
        best_value = -float('inf')

        # Determine the opponent's color
        opp_player = self.colors[1] if curr_player == self.colors[0] else self.colors[0]

        # Enumerate all legal moves
        legal_moves = [col for col in range(7) if self.is_legal_move(col, state)]

        # Base case: If the game is over or the depth is 0, return the evaluation value
        if depth == 0 or not legal_moves or self.game_is_over(state):
            return None, self.evaluate(state, curr_player)

        # Iterate over all legal moves
        for move in legal_moves:
            new_state = self.make_move(state, move, curr_player)
            _, value = self.minimax(depth - 1, new_state, opp_player, use_alpha_beta)
            value = -value  # Negate the value because we're switching players

            # Update the best move and value if necessary
            if value > best_value:
                best_value = value
                best_move = move

            # Alpha-beta pruning (only if enabled)
            if use_alpha_beta:
                alpha = best_value
                if alpha >= 100000:
                    break

        return best_move, best_value


