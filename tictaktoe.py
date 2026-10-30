
# Tic-Tac-Toe Game
# Two Player Console Based Game

def display_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2-i] == player for i in range(3)):
        return True

    return False


def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        display_board(board)

        print("Player", current_player, "'s turn")

        try:
            position = input("Enter position (1-9): ").strip()

            if position == "":
                print("Input cannot be empty!")
                continue

            position = int(position)

            if position < 1 or position > 9:
                print("Please enter a number between 1 and 9!")
                continue

            row = (position - 1) // 3
            col = (position - 1) % 3

            if board[row][col] != " ":
                print("Cell already occupied! Try again.")
                continue

            board[row][col] = current_player


            if check_winner(board, current_player):
                display_board(board)
                print("Player", current_player, "WINS!")
                break


            if all(cell != " " for row in board for cell in row):
                display_board(board)
                print("Game is a DRAW!")
                break


            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"

        except ValueError:
            print("Invalid input! Please enter a number.")



while True:
    play_game()

    again = input("\nDo you want to play again? (yes/no): ").strip().lower()

    if again != "yes":
        print("Thank you for playing Tic-Tac-Toe!")
        break
