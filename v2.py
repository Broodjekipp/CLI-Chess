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

w_pieces = [
    piece.W_ROOK,
    piece.W_KNIGHT,
    piece.W_BISHOP,
    piece.W_QUEEN,
    piece.W_KING,
    piece.W_BISHOP,
    piece.W_KNIGHT,
    piece.W_ROOK,
]

b_pieces = [
    piece.B_ROOK,
    piece.B_KNIGHT,
    piece.B_BISHOP,
    piece.B_QUEEN,
    piece.B_KING,
    piece.B_BISHOP,
    piece.B_KNIGHT,
    piece.B_ROOK,
]

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
    except (ValueError, IndexError):
        input("Invalid format! Correct format: e7 e5. Press ENTER...")
        return False, None
    return True, move


def validate_move(move, board, piece, white_turn, w_pieces, b_pieces):
    from_piece = board[move.from_row][move.from_col]
    to_piece = board[move.to_row][move.to_col]

    if from_piece == piece.EMPTY:
        return False

    if [move.from_row, move.from_col] == [move.to_row, move.to_col]:
        return False

    # Move your own piece
    if white_turn and from_piece not in w_pieces:
        return False
    elif not white_turn and from_piece not in b_pieces:
        return False

    return True


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


def check_castling(
    rook_moved,
    board,
    white_turn,
):
    return False


def check_check():
    pass


def check_mate():
    pass


def win(player):
    pass


while True:
    display_board(board)
    success, move = get_move(white_turn)
    if not success:
        continue
    if validate_move(move, board, piece, white_turn, w_pieces, b_pieces):
        make_move(
            move,
            rook_moved,
            board,
            white_turn,
            piece.EMPTY,
        )
    check_mate()
    white_turn = not white_turn
