import random

# Constants
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'
BOARD_SIZE = 3

def print_board(board):
    """Display the current state of the board."""
    print("\nHere's the current board:")
    for row in board:
        print(' | '.join(row))
        print('-' * (BOARD_SIZE * 4 - 1))
    print()

def check_winner(board, player):
    """Check if the given player has won the game."""
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(BOARD_SIZE):
        if all(board[row][col] == player for row in range(BOARD_SIZE)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_SIZE)) or \
       all(board[i][BOARD_SIZE - i - 1] == player for i in range(BOARD_SIZE)):
        return True
    return False

def is_board_full(board):
    """Check if the board is completely filled with no empty cells."""
    return all(cell != EMPTY for row in board for cell in row)

def get_empty_cells(board):
    """Get a list of coordinates for empty cells on the board."""
    return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == EMPTY]

def minimax(board, depth, is_maximizing):
    """Minimax algorithm to decide the best move for the AI."""
    if check_winner(board, PLAYER_X):
        return -10
    if check_winner(board, PLAYER_O):
        return 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r, c in get_empty_cells(board):
            board[r][c] = PLAYER_O
            score = minimax(board, depth + 1, False)
            board[r][c] = EMPTY
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r, c in get_empty_cells(board):
            board[r][c] = PLAYER_X
            score = minimax(board, depth + 1, True)
            board[r][c] = EMPTY
            best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    """Find the best move for the AI to make."""
    best_move = None
    best_score = -float('inf')
    for r, c in get_empty_cells(board):
        board[r][c] = PLAYER_O
        move_score = minimax(board, 0, False)
        board[r][c] = EMPTY
        if move_score > best_score:
            best_score = move_score
            best_move = (r, c)
    return best_move

def player_move(board):
    """Prompt the player to make their move and update the board."""
    while True:
        try:
            r, c = map(int, input("Your turn! Enter row and column (0, 1, or 2) separated by a space: ").split())
            if board[r][c] == EMPTY:
                board[r][c] = PLAYER_X
                break
            else:
                print("Oops! That spot is already taken. Try another one.")
        except (ValueError, IndexError):
            print("Hmm, that doesn't seem right. Please enter valid row and column numbers (0, 1, or 2) separated by a space.")

def play_game():
    """Main game loop where the player and AI take turns."""
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        player_move(board)
        if check_winner(board, PLAYER_X):
            print_board(board)
            print("Congratulations! You win! 🎉")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw! Well played! 👏")
            break

        print("The AI is making its move...")
        r, c = find_best_move(board)
        board[r][c] = PLAYER_O
        print_board(board)
        if check_winner(board, PLAYER_O):
            print("Oh no! The AI wins this time. Better luck next time! 🤖")
            break
        if is_board_full(board):
            print("It's a draw! Well played! 👏")
            break

if __name__ == "__main__":
    play_game()
