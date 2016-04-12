from __future__ import print_function
from itertools import permutations

ROOK_SYMBOL = "R"
QUEEN_SYMBOL = "Q"
KING_SYMBOL = "K"
BISHOP_SYMBOL = "B"
KNIGHT_SYMBOL = "Kn"

VALID_PIECES = {ROOK_SYMBOL, QUEEN_SYMBOL, KING_SYMBOL, BISHOP_SYMBOL,
                KNIGHT_SYMBOL}


def _get_bishop_pos(board_size, row, col):
    """Return a list of tuples with the positions reachable by a bishop in the
    position identified by row and column."""
    res = []
    diag_row, diag_col = row+1, col+1
    # get SE diagonal
    while diag_row < board_size and diag_col < board_size:
        res.append((diag_row, diag_col))
        diag_row +=1
        diag_col +=1
    # get NW diagonal
    diag_row, diag_col = row-1, col-1
    while diag_row >= 0 and diag_col >= 0:
        res.append((diag_row, diag_col))
        diag_row -=1
        diag_col -=1
    # get SW diagonal
    diag_row, diag_col = row+1, col-1
    while diag_row < board_size and diag_col >= 0:
        res.append((diag_row, diag_col))
        diag_row +=1
        diag_col -=1
    # get NE diagonal
    diag_row, diag_col = row-1, col+1
    while diag_row >=0 and diag_col < board_size:
        res.append((diag_row, diag_col))
        diag_row -=1
        diag_col +=1
    return res


def _get_rook_pos(board_size, row, column):
    """Return a list of tuples with the positions reachable by a rook in the
    position identified by row and column."""
    # get whole column except place where rook is
    res = [(r, column) for r in range(board_size) if r != row]
    # add row except for place where rook is
    res.extend(((row, c) for c in range(board_size) if c != column))
    return res


def _get_king_pos(board_size, row, column):
    """Return a list of tuples with the positions reachable by a king in the
    position identified by row and column."""
    res = []
    # Get list of tuple deltas of row and column of how a king can move.
    king_pos_deltas = ((r, c) for r in range(-1,2) for c in range(-1,2))
    for (r, c) in king_pos_deltas:
        if 0 <= row + r <board_size and 0 <= column + c < board_size:
            res.append((row+r, column+c))
    return res


def _get_knight_pos(board_size, row, column):
    """Return a list of tuples with the positions reachable by a knight in the
    position identified by row and column."""
    res = []
    # Get list of tuple deltas of row and column of how a king can move.
    knight_pos_deltas = [(-2,-1), (-2, 1), (-1, -2), (-1, 2), (2, -1), (2, 1),
                         (1, -2), (1, 2)]
    for (r, c) in knight_pos_deltas:
        if 0 <= row + r <board_size and 0 <= column + c < board_size:
            res.append((row+r, column+c))

    return res


def _get_queen_pos(board_size, row, column):
    """Return a list of tuples with the positions reachable by a queen in the
    position identified by row and column."""
    # A queen can move like a rook
    res = _get_rook_pos(board_size, row, column)
    # and like a bishop
    res.extend(_get_bishop_pos(board_size, row, column))
    return res


def get_positions(board, position_list):
    res = []
    # TODO remove this assert after testing
    assert len(position_list) == len(set(position_list)), "ups, repeated elems"
    for (row, col) in position_list:
        res.append(board[row][col])
    return res


def set_positions(board, position_list, mark="x"):
    for (row, col) in position_list:
        board[row][col] = mark


def try_place_piece(board, piece, row, column):
    """"Function that tries to place a piece on the board. If able to to so,
     it will return True and a new board with the piece in it, else it will
     return False and None (since the board hasn't been modified).
     :param board: board where we will try to place the piece
     :param piece: type of piece we want to place on the board
     :param row: row where we want to place the piece
     :param column: column where we want to place the piece
    """
    piece_pos_dict = {
        KNIGHT_SYMBOL: _get_knight_pos,
        QUEEN_SYMBOL: _get_queen_pos,
        KING_SYMBOL: _get_king_pos,
        ROOK_SYMBOL: _get_rook_pos,
        BISHOP_SYMBOL: _get_bishop_pos,
    }
    if piece.capitalize() not in piece_pos_dict:
        raise ValueError("Invalid type of piece")
    piece_pos_func = piece_pos_dict[piece]
    piece_pos = piece_pos_func(len(board), row, column)
    # if any of the positions our piece covers has already another chess piece
    # on it we cannot place it.
    if set(get_positions(board, piece_pos)).intersection(set(VALID_PIECES)):
        return False, None
    else:
        # Copy the board
        board_cp = [r[:] for r in board]
        # The piece can be safely placed, mark the board positions
        set_positions(board_cp, piece_pos)
        board_cp[row][column] = piece.capitalize()
        return True, board_cp


def _solve_board(board, starting_row, starting_col, piece_set, sol_number):
    """tries to solve board starting at a given position for a given set
    of pieces"""
    if not piece_set:
        print_board(board)
        sol_number[0] += 1
        return True

    board_size = len(board)
    pieces = list(piece_set)
    row = starting_row
    column = starting_col
    while row < board_size:
        while column < board_size:
            if not board[row][column]:
                piece = pieces[0]
                placed, new_board = try_place_piece(board, piece, row, column)
                if placed:
                    _solve_board(new_board, row, column, pieces[1:],
                                 sol_number)
                column += 1
            else:
                column += 1
        column = 0
        row += 1
    if pieces:
        return None


def print_board(board, cell_size=5):
    board_size = len(board)
    print("*"*(board_size*cell_size+board_size+1))
    for row in board:
        formatted_row = []
        for column in row:
            if column not in VALID_PIECES:
                formatted_row.append(" "*cell_size)
            else:
                formatted_row.append("{0:^{1}}".format(column, cell_size))
        print ("|", end="")
        print(*formatted_row, sep="|", end="")
        print("|")
        print("*"*(board_size*cell_size+board_size+1))


def solve(board_size, pieces):
    board = [[False]*board_size for _ in range(board_size)]
    total_solutions = [0]
    for piece_set in (set(permutations(pieces))):
        _solve_board(board, 0, 0, piece_set, total_solutions)
    print("Total number of solutions: {0}".format(total_solutions[0]))



if __name__ == "__main__":
    #solve(4, ["Kn", "Kn", "R", "R", "Kn", "Kn"])
    #solve(8, ["Q"]*8)
    #solve(3, ["K", "K", "R"])
    #solve(7, ["K", "K", "Q", "Q", "B", "B", "Kn"])
    solve(12, ["Q"]*12)
