"""
TODO:
* Add bishop moving logic
* Add queen moving logic
* Add check_mate
* Add check_check
"""
from os import system, name

EMPTY_PIECE = "."

board = [
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    [EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE,
        EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE],
    [EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE,
        EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE],
    [EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE,
        EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE],
    [EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE,
        EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE, EMPTY_PIECE],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["r", "n", "b", "q", "k", "b", "n", "r"],
]

player_turn = True  # True is white, False is black


def display_board(board):
    system('cls' if name == 'nt' else 'clear')  # Clear terminal
    print(f"+ {"- " * 8}+")
    for row in range(len(board)):
        print("| ", end="")
        for col in range(len(board[row])):
            print(board[row][col], end=" ")
        print(f"|{row + 1}")
    print(f"+ {"- " * 8}+")
    print(f"  {" ".join(str(i + 1) for i in range(len(board)))}")


def get_move(player_turn):
    move = input(f"{"White" if player_turn else "Black"}'s turn: ")
    try:
        from_row, from_col = [int(move[0])-1, int(move[1])-1]
        to_row, to_col = [int(move[-2])-1, int(move[-1])-1]
    except (ValueError, IndexError):
        input("Invalid notation! Format: 42 44")
        return False, None, None, None, None
    
    if not (0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8):
        input("Invalid notation! Format: 42 44")
        return False, None, None, None, None
    
    if not move_is_legal(board, player_turn, from_row, from_col, to_row, to_col):
        input("Illegal move!")
        return False, None, None, None, None
    
    return True, from_row, from_col, to_row, to_col


def move_piece(board):
    success, from_row, from_col, to_row, to_col = get_move(player_turn)

    if not success:
        return False

    from_piece = board[from_row][from_col]
    board[from_row][from_col] = EMPTY_PIECE
    board[to_row][to_col] = from_piece
    return True


def move_is_legal(board, player_turn, from_row, from_col, to_row, to_col):
    from_piece = board[from_row][from_col]
    to_piece = board[to_row][to_col]

    if from_piece == EMPTY_PIECE:
        return False

    if [from_row, from_col] == [to_row, to_col]:
        return False

    # Move your own piece
    if player_turn and not is_white(from_piece):
        return False
    if not player_turn and not is_black(from_piece):
        return False

    # Capture opponent's piece
    if to_piece != EMPTY_PIECE and player_turn and is_white(to_piece):
        return False
    if to_piece != EMPTY_PIECE and not player_turn and is_black(to_piece):
        return False

    # Piece-specific legality tests
    if from_piece.lower() == "p":  # Pawn
        return is_legal_pawn(from_row, from_col, to_row, to_col, to_piece, player_turn)

    if from_piece.lower() == "r":  # Rook
        return is_legal_rook(from_row, from_col, to_row, to_col)

    if from_piece.lower() == "n":  # Knight
        return is_legal_knight(from_row, from_col, to_row, to_col)

    if from_piece.lower() == "b":  # Bishop
        return is_legal_bishop(from_row, from_col, to_row, to_col)

    if from_piece.lower() == "k":  # King
        return is_legal_king(from_row, from_col, to_row, to_col)

    if from_piece.lower() == "q":  # Queen
        return is_legal_queen(from_row, from_col, to_row, to_col)

    return False


def is_black(piece):
    return piece.isupper()


def is_white(piece):
    return piece.islower()


def is_legal_pawn(from_row, from_col, to_row, to_col, to_piece, player_turn):
    direction = -1 if player_turn else 1
    steps = abs(from_row - to_row)
    same_col = (from_col == to_col)

    if to_row != from_row + direction:
        return False
        
    if same_col:
        if steps == 1:
            if to_piece == EMPTY_PIECE:
                return True

        elif steps == 2:
            if from_row == 1 and not player_turn:
                if board[from_row + 1][from_col] == EMPTY_PIECE:
                    return True
            if from_row == 6 and player_turn:
                if board[from_row - 1][from_col] == EMPTY_PIECE:
                    return True
            return False
    
    else:
        if to_piece != EMPTY_PIECE and steps == 1:
            return True
        else:
            return False

    return False


def is_legal_rook(from_row, from_col, to_row, to_col):
    if from_col != to_col and from_row != to_row:
        return False  # moving diagonally

    if from_col != to_col:  # horizontal move
        for piece in board[from_row][min(from_col, to_col)+1: max(from_col, to_col)]:
            if piece != EMPTY_PIECE:
                return False

    if from_row != to_row:  # vertical move
        for r in range(min(from_row, to_row)+1, max(from_row, to_row)):
            if board[r][from_col] != EMPTY_PIECE:
                return False

    return True


def is_legal_knight(from_row, from_col, to_row, to_col):
    row_diff = abs(from_row - to_row)
    col_diff = abs(from_col - to_col)
    if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
        return True
    return False


def is_legal_bishop(from_row, from_col, to_row, to_col):
    return True


def is_legal_king(from_row, from_col, to_row, to_col):
    if abs(from_row - to_row) > 1 or abs(from_col - to_col) > 1:
        return False
    if check_check(to_row, to_col):
        return False
    return True


def is_legal_queen(from_row, from_col, to_row, to_col):
    return True


def check_mate():
    pass


def check_check(row, col):
    return False


while True:
    display_board(board)
    if move_piece(board):
        check_mate()
        player_turn = not player_turn
    else:
        continue
