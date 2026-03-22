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
        from_coords = [int(move[0])-1, int(move[1])-1]
        to_coords = [int(move[-2])-1, int(move[-1])-1]
    except (ValueError, IndexError):
        print("Invalid notation! Format: 42 44")
        return None
    if not move_is_legal(from_coords, to_coords):
        print("Illegal move!")
        return False
    
    from_col, from_row = from_coords
    to_col, to_row = to_coords
    board[from_col][from_row] = "."
    board[to_row][to_col] = f"{"p" if player_turn else "P"}"
    return True


def is_black(piece):
    return piece.isupper()


def is_white(piece):
    return piece.islower()


def is_legal_pawn(from_coords, to_coords, from_row, from_col, to_row, to_col, to_piece):
    if from_col != to_col:  # Column changed
        if to_piece != ".":
            return True
        else:
            return False

    elif abs(from_row - to_row) == 2:  # Made 2 steps
        if from_row == 1 and not player_turn:
            return True
        if from_row == 6 and player_turn:
            return True
        return False

    elif abs(from_row - to_row) == 1:  # Made 1 step
        if to_piece == ".":
            return True
        
    return False


def is_legal_rook(from_coords, to_coords, from_row, from_col, to_row, to_col, to_piece):
    pass


def is_legal_knight(from_coords, to_coords, from_row, from_col, to_row, to_col, to_piece):
    pass


def is_legal_bishop(from_coords, to_coords, from_row, from_col, to_row, to_col, to_piece):
    pass


def is_legal_king(from_coords, to_coords, from_row, from_col, to_row, to_col, to_piece):
    pass


def is_legal_queen(from_coords, to_coords, from_row, from_col, to_row, to_col, to_piece):
    pass


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

    # Capture opponent's piece
    if to_piece != "." and player_turn and is_white(to_piece):
        return False
    if to_piece != "." and not player_turn and is_black(to_piece):
        return False

    if from_piece.lower() == "p":  # Piece is a pawn
        return is_legal_pawn(from_coords, to_coords, from_row,
                      from_col, to_row, to_col, to_piece)

    if from_piece.lower() == "r":  # Piece is a rook
        return is_legal_rook(from_coords, to_coords, from_row,
                      from_col, to_row, to_col, to_piece)

    if from_piece.lower() == "n":  # Piece is a knight
        return is_legal_knight(from_coords, to_coords, from_row,
                      from_col, to_row, to_col, to_piece)

    if from_piece.lower() == "b":  # Piece is a bishop
        return is_legal_bishop(from_coords, to_coords, from_row,
                      from_col, to_row, to_col, to_piece)

    if from_piece.lower() == "k":  # Piece is a king
        return is_legal_king(from_coords, to_coords, from_row,
                      from_col, to_row, to_col, to_piece)

    if from_piece.lower() == "q":  # Piece is a queen
        return is_legal_queen(from_coords, to_coords, from_row,
                      from_col, to_row, to_col, to_piece)

    return True


def check_mate():
    pass


while True:
    display_board()
    if move_piece():
        check_mate()
        player_turn = not player_turn
    else:
        continue
