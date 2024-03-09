from connect4 import *

def main():
    """
    Play a Connect Four game.
    """
    game = Game()
    game.print_state()

    player1 = game.players[0]
    player2 = game.players[1]

    win_counts = [0, 0, 0]  # [player1 wins, player2 wins, ties]

    while True:
        while not game.finished:
            game.next_move()

        # game.find_fours()  # Remove this line
        game.print_state()

        if game.winner is None:
            win_counts[2] += 1
        elif game.winner == player1:
            win_counts[0] += 1
        else:
            win_counts[1] += 1

        print_stats(player1, player2, win_counts)

        play_again = input("Would you like to play again? (y/n) ").lower()
        if play_again == 'n':
            print("Thanks for playing!")
            break
        elif play_again == 'y':
            game.new_game()
            game.print_state()
        else:
            print("Invalid input. Please try again.")
        
def print_stats(player1, player2, win_counts):
    print("{0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
        win_counts[0], player2.name, win_counts[1], win_counts[2]))
        
if __name__ == "__main__":
    main()
