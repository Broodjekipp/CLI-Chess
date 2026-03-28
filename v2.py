from collections import namedtuple
from types import SimpleNamespace

piece = SimpleNamespace(
    EMPTY="-",
    W_PAWN="p",
    W_ROOK="r",
    W_KNIGHT="n",
    W_BISHOP="b",
    W_QUEEN="q",
    W_KING="k",
    B_PAWN="P",
    B_ROOK="R",
    B_KNIGHT="N",
    B_BISHOP="B",
    B_QUEEN="Q",
    B_KING="K",
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

Rook_moved = namedtuple("Rook_moved", ["w_rook_l", "w_rook_r", "b_rook_l", "b_rook_r"])
rook_moved = Rook_moved(w_rook_l=False, w_rook_r=False, b_rook_l=False, b_rook_r=False)

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


def display_board(board):
    print("+---------------+")
    for row in range(len(board)):
        print("|", end="")
        for col in range(len(board[row])):
            print(board[row][col], end="|" if col != 7 else "")
        print("| " + str(8 - row))
    print("+---------------+")
    print(" A B C D E F G H ")


def get_move(white_turn):
    move_str = (
        input(f"{"White" if white_turn else "Black"}'s turn: ")
        .lower()
        .strip()
        .replace(" ", "")
    )
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


def validate_move(move, board, piece, white_turn, white_pieces, black_pieces, rook_moved):
    from_piece = board[move.from_row][move.from_col]
    to_piece = board[move.to_row][move.to_col]
    to_is_white = to_piece in white_pieces
    to_is_black = to_piece in black_pieces
    from_is_white = from_piece in white_pieces
    from_is_black = from_piece in black_pieces
    valid = False

    if from_piece == piece.EMPTY:
        return False

    if [move.from_row, move.from_col] == [move.to_row, move.to_col]:
        return False

    # Move your own piece
    if white_turn and not from_is_white:
        return False
    elif not white_turn and not from_is_black:
        return False



    if to_piece != piece.EMPTY and white_turn and to_is_white:
        return False
    if to_piece != piece.EMPTY and not white_turn and to_is_black:
        return False

    if from_piece in (piece.W_PAWN, piece.B_PAWN):
        valid = validate_pawn(move, board, white_turn, piece.EMPTY, to_piece)
    if from_piece in (piece.W_ROOK, piece.B_ROOK):
        valid = validate_rook(move, board, piece)
    if from_piece in (piece.W_KNIGHT, piece.B_KNIGHT):
        valid = validate_knight(move)
    if from_piece in (piece.W_BISHOP, piece.B_BISHOP):
        valid = validate_bishop(move, board)
    if from_piece in (piece.W_QUEEN, piece.B_QUEEN):
        valid = validate_queen(move, board)
    if from_piece in (piece.W_KING, piece.B_KING):
        valid, castling = validate_king(move, board)
    
    if valid:
        if test_move(move, rook_moved, board, white_turn, piece.EMPTY):
            return True

    return False


def validate_pawn(move, board, white_turn, empty_piece, to_piece):
    start_row = 6 if white_turn else 1
    direction = -1 if white_turn else 1

    # Move forwards
    if move.from_col == move.to_col and board[move.to_row][move.to_col] == empty_piece:
        if move.to_row == move.from_row + direction:
            return True
        if move.from_row == start_row and move.to_row == move.from_row + 2 * direction:
            return True

    # Capture a piece
    elif (
        abs(move.from_col - move.to_col) == 1
        and move.to_row == move.from_row + direction
    ):
        if to_piece != empty_piece:
            return True

    return False


def validate_rook(move, board, piece):
    if not move.from_col == move.to_col and not move.from_row == move.to_row:
        return False
    if not move.from_col == move.to_col:
        for col in range(move.from_col, move.to_col):
            if board[move.from_row][col] != piece.EMPTY:
                return False
    elif not move.from_row == move.to_row:
        for row in range(move.from_row, move.to_row):
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
    if abs(move.from_row - move.to_row) != abs(move.from_col - move.to_row):
        return False

    return True


def validate_queen(move, board):
    return True


def validate_king(move, board):
    if check_castling(rook_moved, board, white_turn):
        pass
    return True, False


def make_move(
    move,
    rook_moved,
    board,
    white_turn,
    empty_piece="-",
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
    empty_piece="-",
):
    make_move(
        move,
        rook_moved,
        board,
        white_turn,
        empty_piece="-",
    )
    if check_check(board, white_turn):
        return False
    return True


def check_castling(
    rook_moved,
    board,
    white_turn,
):
    return False


def check_check(board, white_turn):
    pass


def check_mate():
    pass


def win(player):
    pass


while True:
    display_board(board)
    success, move = get_move(white_turn)
    if not success:
        input("Invalid format! Correct format: e7 e5. Press ENTER...")
        continue
    if validate_move(move, board, piece, white_turn, white_pieces, black_pieces, rook_moved):
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
    check_mate()
    white_turn = not white_turn
