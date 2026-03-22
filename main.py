"""
TODO:
* Add check_mate
* Add en passant
* Add promotion choose menu
* Add castling
* Add standard chess notation
"""
from os import system, name

EMPTY_PIECE = "."
LETTER_TO_INDEX = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
}

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
    print(f"+-{"-" * 16}+")
    for row in range(len(board)):
        print("| ", end="")
        for col in range(len(board[row])):
            print(board[row][col], end=" ")
        print(f"|{8 - row}")
    print(f"+-{"-" * 16}+")
    print(f"  {" ".join(str(i) for i in LETTER_TO_INDEX)}")


def get_move(player_turn):
    move = input(
        f"{"White" if player_turn else "Black"}'s turn: ").lower().strip()
    if move == "exit":
        exit()
    try:
        from_col, from_row = [LETTER_TO_INDEX[move[0]], 8 - int(move[1])]
        to_col, to_row = [LETTER_TO_INDEX[move[-2]], 8 - int(move[-1])]
    except (ValueError, IndexError, KeyError):
        input("Invalid notation!")
        return False, None, None, None, None

    if not (0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8):
        input("Invalid notation!")
        return False, None, None, None, None

    if not move_is_legal(board, player_turn, from_row, from_col, to_row, to_col, True):
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

    if board[to_row][to_col].lower() == "p" and to_row in (0, 7):  # Pawn promotion
        board[to_row][to_col] = "q" if player_turn else "Q"

    return True


def move_is_legal(board, player_turn, from_row, from_col, to_row, to_col, include_king):
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
        return is_legal_pawn(from_row, from_col, to_row, to_col, to_piece, player_turn, board)
    if from_piece.lower() == "r":  # Rook
        return is_legal_rook(board, from_row, from_col, to_row, to_col)
    if from_piece.lower() == "n":  # Knight
        return is_legal_knight(from_row, from_col, to_row, to_col)
    if from_piece.lower() == "b":  # Bishop
        return is_legal_bishop(board, from_row, from_col, to_row, to_col)
    if from_piece.lower() == "k" and include_king:  # King
        return is_legal_king(board, from_row, from_col, to_row, to_col, player_turn)
    if from_piece.lower() == "q":  # Queen
        return is_legal_queen(board, from_row, from_col, to_row, to_col)

    return False


def is_legal_pawn(from_row, from_col, to_row, to_col, to_piece, player_turn, board):
    direction = -1 if player_turn else 1
    start_row = 6 if player_turn else 1

    if from_col == to_col:
        if to_row == from_row + direction and to_piece == EMPTY_PIECE:
            return True
        if from_row == start_row and to_row == from_row + 2 * direction:
            if to_piece == EMPTY_PIECE and board[from_row + direction][from_col] == EMPTY_PIECE:
                return True

    elif abs(from_col - to_col) == 1 and to_row == from_row + direction:
        if to_piece != EMPTY_PIECE:
            return True

    return False


def is_legal_rook(board, from_row, from_col, to_row, to_col):
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


def is_legal_bishop(board, from_row, from_col, to_row, to_col):
    row_diff = abs(from_row - to_row)
    col_diff = abs(from_col - to_col)

    if row_diff != col_diff:
        return False

    row_step = 1 if to_row > from_row else -1
    col_step = 1 if to_col > from_col else -1

    r, c = from_row + row_step, from_col + col_step
    while (r, c) != (to_row, to_col):
        if board[r][c] != EMPTY_PIECE:
            return False
        r += row_step
        c += col_step

    return True


def is_legal_king(board, from_row, from_col, to_row, to_col, player_turn):
    if abs(from_row - to_row) > 1 or abs(from_col - to_col) > 1:
        return False
    if check_check(board, to_row, to_col, player_turn)[0]:
        return False

    return True


def is_legal_queen(board, from_row, from_col, to_row, to_col):
    return (is_legal_rook(board, from_row, from_col, to_row, to_col) or
            is_legal_bishop(board, from_row, from_col, to_row, to_col))


def is_black(piece):
    return piece.isupper()


def is_white(piece):
    return piece.islower()


def find_kings(board):
    return [
        (r, c)
        for r in range(len(board))
        for c in range(len(board[r]))
        if board[r][c].lower() == "k"
    ]


def king_can_escape(board, r, c, player_turn):
    return any(
        not check_check(board, to_r, to_c, player_turn)[0]
        for to_r in range(len(board))
        for to_c in range(len(board[to_r]))
        if is_legal_king(board, r, c, to_r, to_c, player_turn)
    )


def check_mate(board, player_turn):
    for r, c in find_kings(board):  # Find the kings in the game
        king_is_white = is_white(board[r][c])
        if king_is_white != player_turn:
            continue
        king_checked, attacker_row, attacker_col = check_check(
            board, r, c, king_is_white)

        if not king_checked:
            continue

        if attacker_row is not None and attacker_col is not None:
            attacker_defended, *_ = check_check(board, attacker_row, attacker_col, not king_is_white)
            if attacker_defended:
                return False, None
        
        if king_can_escape(board, r, c, player_turn):
            return False, None
        
        return True, king_is_white
    return False, None


def check_check(board, target_row, target_col, player_piece):
    for r in range(len(board)):
        for c in range(len(board[r])):
            if move_is_legal(board, not player_piece, r, c, target_row, target_col, False):
                return True, r, c

    enemy_king = "K" if player_piece else "k"
    subgrid = [r[target_col - 1:target_col + 2]
               for r in board[target_row - 1:target_row + 2]]
    if any(enemy_king in r for r in subgrid):
        return True, None, None

    return False, None, None


def player_win(winner):
    pass


while True:
    display_board(board)
    if move_piece(board):
        checkmate, winner = check_mate(board, player_turn)
        if checkmate:
            player_win(winner)
        player_turn = not player_turn
    else:
        continue
