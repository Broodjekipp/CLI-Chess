"""
TODO:
* En passant
* Add standard chess notation
* Stalemate
  * Draw by repetition
  * 50 moves w/out check
"""

from collections import namedtuple
from types import SimpleNamespace
from os import system, name

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

castling_moved = {
    "w_rook_l": False,
    "w_rook_r": False,
    "w_king": False,
    "b_rook_l": False,
    "b_rook_r": False,
    "b_king": False,
}

LETTERS_TO_NUMBERS = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
board = [
    [
        piece.EMPTY,
        piece.EMPTY,
        piece.EMPTY,
        piece.EMPTY,
        piece.EMPTY,
        piece.EMPTY,
        piece.EMPTY,
        piece.B_KING,
    ],
    [
        piece.EMPTY,
        piece.EMPTY,
        piece.EMPTY,
        piece.W_PAWN,
        piece.EMPTY,
        piece.EMPTY,
        piece.EMPTY,
        piece.EMPTY,
    ],
    [piece.EMPTY] * 8,
    [piece.EMPTY] * 8,
    [piece.EMPTY] * 8,
    [piece.EMPTY] * 8,
    [piece.EMPTY] * 8,
    [
        piece.W_ROOK,
        piece.EMPTY,
        piece.EMPTY,
        piece.EMPTY,
        piece.W_KING,
        piece.EMPTY,
        piece.EMPTY,
        piece.W_ROOK,
    ],
]


"""board = [
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
]"""

white_turn = True


def is_white(p):
    return p in white_pieces


def is_black(p):
    return p in black_pieces


def display_board(board):
    system("cls" if name == "nt" else "clear")
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
    move_str = input(f"\n{player}'s turn: ").lower().strip().replace(" ", "")
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


def get_promotion_piece(white_turn):
    piece_str = input("Piece to promote pawn to: ").lower().strip().replace(" ", "")

    try:
        if piece_str[0] == "q":
            return piece.W_QUEEN if white_turn else piece.B_QUEEN
        if piece_str[0] == "p":
            return piece.W_PAWN if white_turn else piece.B_PAWN
        if piece_str[0] in ("n", "k") or piece_str == "knight":
            return piece.W_KNIGHT if white_turn else piece.B_KNIGHT
        if piece_str[0] == "r":
            return piece.W_ROOK if white_turn else piece.B_ROOK
        if piece_str[0] == "b":
            return piece.W_BISHOP if white_turn else piece.B_BISHOP
    except IndexError:
        return piece.W_QUEEN if white_turn else piece.B_QUEEN

    return None


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
    castling = 1  # 1 for not castling, 2 for castling so the function only has to return 1 value

    if from_piece == piece.EMPTY:
        return False

    if [move.from_row, move.from_col] == [move.to_row, move.to_col]:
        return False

    # Castling
    CASTLING_PARAMS = {
        True: (piece.W_KING, 7, "w_king", "w_rook_l", "w_rook_r"),
        False: (piece.B_KING, 0, "b_king", "b_rook_l", "b_rook_r"),
    }

    king_piece, king_row, king_key, rook_l_key, rook_r_key = CASTLING_PARAMS[white_turn]

    if check_for_check:
        if (
            from_piece == king_piece
            and move.to_row == king_row  # king stays on its row
            and not castling_moved[king_key]
        ):
            squares_empty = lambda *cols: all(
                board[king_row][c] == piece.EMPTY for c in cols
            )
            square_safe = lambda col: not check_check(
                board, [king_row, col], castling_moved.copy()
            )[0]

            if move.to_col == 2 and not castling_moved[rook_l_key]:
                if squares_empty(1, 2, 3) and square_safe(2) and square_safe(3):
                    castling = 2

            elif move.to_col == 6 and not castling_moved[rook_r_key]:
                if squares_empty(5, 6) and square_safe(5) and square_safe(6):
                    castling = 2

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
        valid = validate_king(move, board) or castling == 2

    if valid:
        if check_for_check:
            if test_move(move, rook_moved, board, white_turn):
                return castling
        else:
            return castling  # skip the check test when already inside one

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
    castling_moved,
    board,
    white_turn,
    empty_piece,
    is_test=False,
    castling=False,
):
    from_piece = board[move.from_row][move.from_col]

    # Check if king or rook is moved
    if white_turn:
        if from_piece == piece.W_KING:
            castling_moved["w_king"] = True
        if from_piece == piece.W_ROOK:
            if move.from_row == 7 and move.from_col == 0:
                castling_moved["w_rook_l"] = True
            elif move.from_row == 7 and move.from_col == 7:
                castling_moved["w_rook_r"] = True
    else:
        if from_piece == piece.B_KING:
            castling_moved["b_king"] = True
        if from_piece == piece.B_ROOK:
            if move.from_row == 7 and move.from_col == 0:
                castling_moved["b_rook_l"] = True
            elif move.from_row == 7 and move.from_col == 7:
                castling_moved["b_rook_r"] = True

    board[move.to_row][move.to_col] = board[move.from_row][move.from_col]
    board[move.from_row][move.from_col] = empty_piece

    if castling:
        rook_row = move.to_row  # Same row as king
        if move.to_col == 2:  # Queenside
            board[rook_row][3] = board[rook_row][0]
            board[rook_row][0] = piece.EMPTY
        elif move.to_col == 6:  # Kingside
            board[rook_row][5] = board[rook_row][7]
            board[rook_row][7] = piece.EMPTY

    # Check pawn promotion
    end = 0 if white_turn else 7
    if (
        not is_test
        and move.to_row == end
        and board[move.to_row][move.to_col]
        in (
            piece.W_PAWN,
            piece.B_PAWN,
        )
    ):
        while True:
            piece_to_promote = get_promotion_piece(white_turn)
            if piece_to_promote:
                break
            print("Invalid piece! Pieces: Q, R, K, B")
        board[move.to_row][move.to_col] = piece_to_promote


def test_move(
    move,
    rook_moved,
    board,
    white_turn,
):
    test_board = [row[:] for row in board]

    make_move(move, rook_moved, test_board, white_turn, piece.EMPTY, is_test=True)

    king_row, king_col = find_piece(
        test_board, piece.W_KING if white_turn else piece.B_KING
    )

    if check_check(test_board, [king_row, king_col], rook_moved.copy())[0]:
        return False

    return True


def find_piece(board, piece_to_find):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == piece_to_find:
                return row, col
    return None, None


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

    checked, _ = check_check(board, [king_row, king_col], rook_moved.copy())
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
    validation = validate_move(
        move, board, white_turn, white_pieces, black_pieces, castling_moved
    )
    if validation:
        make_move(
            move, castling_moved, board, white_turn, piece.EMPTY, False, validation
        )
    else:
        input("Illegal move! Press ENTER...")
        continue
    white_turn = not white_turn
    if check_mate(board, white_turn, castling_moved):
        winner = "Black" if white_turn else "White"
        print(f"Checkmate! {winner} wins!")
        break
