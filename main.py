from copy import deepcopy

start_board = [
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["r", "n", "b", "k", "q", "b", "n", "r"],
]

board = deepcopy(start_board)
player_turn = True  # True is white, False is black


def display_board():
    print(f"+ {"- " * 8}+")
    for row in range(len(board)):
        print("| ", end="")
        for col in range(len(board[row])):
            print(board[row][col], end=" ")
        print(f"|{row + 1}")
    print(f"+ {"- " * 8}+")
    print(f"  {" ".join(str(i + 1) for i in range(len(board)))}")


def move_piece():
    # Format is 42 44
    move = input(f"{"White" if player_turn else "Black"}'s turn: ")
    try:
        from_coords = [int(move[0]), int(move[1])]
        to_coords = [int(move[-1]), int(move[-2])]
    except:
        print("Invalid notation! Format: 42 44")
        return None
    if move_is_legal(from_coords, to_coords):
        pass
    else:
        print("Illegal move!")


def is_black(piece):
    return piece.isupper()


def is_white(piece):
    return piece.islower()


def move_is_legal(from_coords, to_coords):
    from_row, from_col = from_coords
    to_row, to_col = to_coords

    from_piece = board[from_row][from_col]
    to_piece = board[to_row][to_col]

    if from_piece == ".":
        return False

    # Move your own piece
    if player_turn and not is_white(from_piece):
        return False
    if not player_turn and not is_black(from_piece):
        return False    


def check_mate():
    pass


while True:
    display_board()
    move_piece()
    check_mate()
