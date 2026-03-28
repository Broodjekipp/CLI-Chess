"""
TODO:
* Castling
* Pawn promotion
 * Pawn promotion choose menu
* En passant
* Add standard chess notation
* Move history
* Stalemate
"""

from collections import namedtuple
from types import SimpleNamespace
from enum import Enum

# For users with light mode, black and white pawns should be swapped
piece = SimpleNamespace(
    EMPTY="·",
    B_PAWN="♙",
    B_ROOK="♖",
    B_KNIGHT="♘",
    B_BISHOP="♗",
    B_QUEEN="♕",
    B_KING="♔",
    W_PAWN="♟",
    W_ROOK="♜",
    W_KNIGHT="♞",
    W_BISHOP="♝",
    W_QUEEN="♛",
    W_KING="♚",
)

white_pieces = {
    piece.W_ROOK,
    piece.W_KNIGHT,
    piece.W_BISHOP,
    piece.W_QUEEN,
    piece.W_KING,
    piece.W_PAWN,
}
black_pieces = {
    piece.B_ROOK,
    piece.B_KNIGHT,
    piece.B_BISHOP,
    piece.B_QUEEN,
    piece.B_KING,
    piece.B_PAWN,
}

Move = namedtuple(
    "Move",
    ["from_row", "from_col", "to_row", "to_col"],
)

rook_moved = {
    "w_rook_l": False,
    "w_rook_r": False,
    "b_rook_l": False,
    "b_rook_r": False,
}

LETTERS_TO_NUMBERS = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

board = [
    [
        piece.B_ROOK,
        piece.B_KNIGHT,
        piece.B_BISHOP,
        piece.B_QUEEN,
        piece.B_KING,
        piece.B_BISHOP,
        piece.B_KNIGHT,
        piece.B_ROOK,
    ],
    [piece.B_PAWN] * 8,
    [piece.EMPTY] * 8,
    [piece.EMPTY] * 8,
    [piece.EMPTY] * 8,
    [piece.EMPTY] * 8,
    [piece.W_PAWN] * 8,
    [
        piece.W_ROOK,
        piece.W_KNIGHT,
        piece.W_BISHOP,
        piece.W_QUEEN,
        piece.W_KING,
        piece.W_BISHOP,
        piece.W_KNIGHT,
        piece.W_ROOK,
    ],
]

white_turn = True


def is_white(p):
    return p in white_pieces


def is_black(p):
    return p in black_pieces


def display_board(board):
    print("╔═══════════════╗")
    for row in range(len(board)):
        print("║", end="")
        for col in range(len(board[row])):
            print(board[row][col], end="│" if col != 7 else "")
        print("║ " + str(8 - row))
    print("╚═══════════════╝")
    print(" A B C D E F G H ")


def get_move(white_turn):
    player = "White" if white_turn else "Black"
    move_str = input(f"{player}'s turn: ").lower().strip().replace(" ", "")
    try:
        move = Move(
            from_row=8 - int(move_str[1]),
            from_col=LETTERS_TO_NUMBERS[move_str[0]],
            to_row=8 - int(move_str[-1]),
            to_col=LETTERS_TO_NUMBERS[move_str[-2]],
        )
    except (ValueError, IndexError, KeyError):
        return False, None
    return True, move


def validate_move(
    move,
    board,
    white_turn,
    white_pieces,
    black_pieces,
    rook_moved,
    check_for_check=True,
):
    from_piece = board[move.from_row][move.from_col]
    to_piece = board[move.to_row][move.to_col]
    valid = False

    if from_piece == piece.EMPTY:
        return False

    if [move.from_row, move.from_col] == [move.to_row, move.to_col]:
        return False

    # Move your own piece
    my_pieces = white_pieces if white_turn else black_pieces
    if from_piece not in my_pieces: 
        return False
    if to_piece in my_pieces: 
        return False

    if from_piece in (piece.W_PAWN, piece.B_PAWN):
        valid = validate_pawn(move, board, white_turn, to_piece)
    if from_piece in (piece.W_ROOK, piece.B_ROOK):
        valid = validate_rook(move, board)
    if from_piece in (piece.W_KNIGHT, piece.B_KNIGHT):
        valid = validate_knight(move)
    if from_piece in (piece.W_BISHOP, piece.B_BISHOP):
        valid = validate_bishop(move, board)
    if from_piece in (piece.W_QUEEN, piece.B_QUEEN):
        valid = validate_queen(move, board)
    if from_piece in (piece.W_KING, piece.B_KING):
        valid = validate_king(move, board)

    if valid:
        if check_for_check:
            if test_move(move, rook_moved, board, white_turn):
                return True
        else:
            return True  # skip the check test when already inside one

    return False


def validate_pawn(move, board, white_turn, to_piece):
    start_row = 6 if white_turn else 1
    direction = -1 if white_turn else 1

    # Move forwards
    if move.from_col == move.to_col and board[move.to_row][move.to_col] == piece.EMPTY:
        if move.to_row == move.from_row + direction:
            return True
        if move.from_row == start_row and move.to_row == move.from_row + 2 * direction:
            middle_row = move.from_row + direction
            if board[middle_row][move.from_col] == piece.EMPTY:
                return True

    # Capture a piece
    elif (
        abs(move.from_col - move.to_col) == 1
        and move.to_row == move.from_row + direction
    ):
        if to_piece != piece.EMPTY:
            return True

    return False


def validate_rook(move, board):
    if move.from_col != move.to_col and move.from_row != move.to_row:
        return False

    if move.from_col != move.to_col:  # horizontal move
        step = 1 if move.from_col < move.to_col else -1
        for col in range(move.from_col + step, move.to_col, step):
            if board[move.from_row][col] != piece.EMPTY:
                return False
    else:  # vertical move
        step = 1 if move.from_row < move.to_row else -1
        for row in range(move.from_row + step, move.to_row, step):
            if board[row][move.from_col] != piece.EMPTY:
                return False

    return True


def validate_knight(move):
    if abs(move.from_row - move.to_row) == 2:
        if abs(move.from_col - move.to_col) == 1:
            return True
    elif abs(move.from_row - move.to_row) == 1:
        if abs(move.from_col - move.to_col) == 2:
            return True
    return False


def validate_bishop(move, board):
    if abs(move.from_row - move.to_row) != abs(move.from_col - move.to_col):
        return False

    row_direction = 1 if move.from_row < move.to_row else -1
    col_direction = 1 if move.from_col < move.to_col else -1

    row = move.from_row + row_direction
    col = move.from_col + col_direction
    while row != move.to_row:
        if board[row][col] != piece.EMPTY:
            return False
        row += row_direction
        col += col_direction

    return True


def validate_queen(move, board):
    if validate_bishop(move, board) or validate_rook(move, board):
        return True
    return False


def validate_king(move, board):
    if max(abs(move.from_col - move.to_col), abs(move.from_row - move.to_row)) == 1:
        return True
    return False


def make_move(
    move,
    rook_moved,
    board,
    white_turn,
    empty_piece,
):
    # Check for castling
    if check_castling(
        rook_moved,
        board,
        white_turn,
    ):
        # Move the king and correct rook
        pass
    board[move.to_row][move.to_col] = board[move.from_row][move.from_col]
    board[move.from_row][move.from_col] = empty_piece


def test_move(
    move,
    rook_moved,
    board,
    white_turn,
):
    test_board = [row[:] for row in board]

    make_move(
        move,
        rook_moved,
        test_board,
        white_turn,
        piece.EMPTY,
    )

    king_row, king_col = find_piece(
        test_board, piece.W_KING if white_turn else piece.B_KING
    )

    if check_check(test_board, [king_row, king_col], rook_moved)[0]:
        return False

    return True


def find_piece(board, piece_to_find):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == piece_to_find:
                return row, col
    return None, None


def check_castling(
    rook_moved,
    board,
    white_turn,
):
    return False


def check_check(board, target, rook_moved):

    for row in range(len(board)):
        for col in range(len(board[row])):
            move_to_check = Move(
                from_row=row,
                from_col=col,
                to_row=target[0],
                to_col=target[1],
            )
            if validate_move(
                move_to_check,
                board,
                is_black(board[target[0]][target[1]]),
                white_pieces,
                black_pieces,
                rook_moved,
                check_for_check=False,
            ):
                return True, [row, col]
    return False, None


def check_mate(board, white_turn, rook_moved):
    king = piece.W_KING if white_turn else piece.B_KING
    king_row, king_col = find_piece(board, king)

    checked, _ = check_check(board, [king_row, king_col], rook_moved)
    if not checked:
        return False

    # Try every possible move
    for from_row in range(8):
        for from_col in range(8):
            for to_row in range(8):
                for to_col in range(8):
                    move = Move(from_row, from_col, to_row, to_col)
                    if validate_move(
                        move, board, white_turn, white_pieces, black_pieces, rook_moved
                    ):
                        return False  # Found an escape

    return True  # Found no escape


while True:
    display_board(board)
    success, move = get_move(white_turn)
    if not success:
        input("Invalid format! Correct format: e7 e5. Press ENTER...")
        continue
    if validate_move(move, board, white_turn, white_pieces, black_pieces, rook_moved):
        make_move(
            move,
            rook_moved,
            board,
            white_turn,
            piece.EMPTY,
        )
    else:
        input("Illegal move! Press ENTER...")
        continue   
    white_turn = not white_turn
    if check_mate(board, white_turn, rook_moved):  
        winner = "Black" if white_turn else "White"
        print(f"Checkmate! {winner} wins!")
        break 
