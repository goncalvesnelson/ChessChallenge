from __future__ import print_function
from functools import wraps

ROOK_SYMBOL = "R"
QUEEN_SYMBOL = "Q"
KING_SYMBOL = "K"
BISHOP_SYMBOL = "B"
KNIGHT_SYMBOL = "Kn"

VALID_PIECES = {ROOK_SYMBOL, QUEEN_SYMBOL, KING_SYMBOL, BISHOP_SYMBOL,
                KNIGHT_SYMBOL}


def memoize(func):
    """Memoize function to use with get_x_pos functions"""
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = res = func(*args)
            return res
        return cache[args]
    return wrapper


@memoize
def _get_bishop_pos(board_size, row, col):
    """Return a set of tuples with the positions reachable by a bishop in the
    position identified by row and column."""
    res = set()
    diag_row, diag_col = row+1, col+1
    # get SE diagonal
    while diag_row < board_size and diag_col < board_size:
        res.add((diag_row, diag_col))
        diag_row += 1
        diag_col += 1
    # get NW diagonal
    diag_row, diag_col = row-1, col-1
    while diag_row >= 0 and diag_col >= 0:
        res.add((diag_row, diag_col))
        diag_row -= 1
        diag_col -= 1
    # get SW diagonal
    diag_row, diag_col = row+1, col-1
    while diag_row < board_size and diag_col >= 0:
        res.add((diag_row, diag_col))
        diag_row += 1
        diag_col -= 1
    # get NE diagonal
    diag_row, diag_col = row-1, col+1
    while diag_row >= 0 and diag_col < board_size:
        res.add((diag_row, diag_col))
        diag_row -= 1
        diag_col += 1

    return res


@memoize
def _get_rook_pos(board_size, row, column):
    """Return a set of tuples with the positions reachable by a rook in the
    position identified by row and column."""
    # get whole column
    res = set([(r, column) for r in range(board_size)])
    # add row
    res.update(((row, c) for c in range(board_size)))
    res.remove((row, column))
    return res


@memoize
def _get_king_pos(board_size, row, column):
    """Return a set of tuples with the positions reachable by a king in the
    position identified by row and column."""
    res = set()
    # Get list of tuple deltas of row and column of how a king can move.
    king_pos_deltas = ((r, c) for r in range(-1, 2) for c in range(-1, 2))
    for r, c in king_pos_deltas:
        if 0 <= row + r < board_size and 0 <= column + c < board_size:
            res.add((row + r, column + c))
    res.remove((row, column))
    return res


@memoize
def _get_knight_pos(board_size, row, column):
    """Return a set of tuples with the positions reachable by a knight in the
    position identified by row and column."""
    res = set()
    # Get list of tuple deltas of row and column of how a king can move.
    knight_pos_deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (2, -1), (2, 1),
                         (1, -2), (1, 2)]
    for r, c in knight_pos_deltas:
        if 0 <= row + r < board_size and 0 <= column + c < board_size:
            res.add((row + r, column + c))

    return res


@memoize
def _get_queen_pos(board_size, row, column):
    """Return a set of tuples with the positions reachable by a queen in the
    position identified by row and column."""
    # A queen can move like a rook
    rook = _get_rook_pos(board_size, row, column)
    # and like a bishop
    bishop = _get_bishop_pos(board_size, row, column)
    return rook.union(bishop)


def get_positions(board, position_list):
    """ Return the contents of board in the positions from position_list
    :param board: board from where we will retrieve the contents.
    :param position_list: list of tuples (row, column) to which we want to
        retrieve the contents from.
    """
    res = []
    for (row, col) in position_list:
        res.append(board[row][col])
    return res


def set_positions(board, position_list, mark="x"):
    """ Set the contents of board in the positions from position_list to mark.
    :param board: board where we will set the positions.
    :param position_list: list of tuples (row, column) we wish to set
    :param mark: what we want to use to set the positions.
    """
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


def _solve_board(board, starting_row, starting_col, piece_set, sol_number,
                 print_solutions):
    """tries to solve board starting at a given position for a given set
    of pieces"""
    if not piece_set:
        if print_solutions:
            print_board(board)
        sol_number[0] += 1
        return True

    board_size = len(board)
    row = starting_row
    column = starting_col
    while row < board_size:
        while column < board_size:
            if not board[row][column]:
                piece = piece_set[0]
                placed, new_board = try_place_piece(board, piece, row, column)
                if placed:
                    _solve_board(new_board, row, column, piece_set[1:],
                                 sol_number, print_solutions)
            column += 1

        column = 0
        row += 1
    # if we got to the end of the board and still have pieces to place, return
    if piece_set:
        return None


def print_board(board, cell_size=3):
    """Prints the board passed as argument.
    :param board: Board to be printed.
    :param cell_size: size that each square will occupy on the board.

    """
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


def solve(board_size, pieces, print_solutions=True):
    """Function to solve a board a given size with a given set of pieces
    :param board_size: Size of the board to solve.
    :param pieces: List with strings representing the pieces to try putting
        on the board.
    """
    board = [[False]*board_size for _ in range(board_size)]
    total_solutions = [0]
    for piece_set in unique_permutations(pieces):
        _solve_board(board, 0, 0, piece_set, total_solutions, print_solutions)
    print("Total number of solutions: {0}".format(total_solutions[0]))
    return total_solutions[0]


# unique_permutations code taken from http://stackoverflow.com/a/12837695
def unique_permutations(seq):
    """
    Yield only unique permutations of seq in an efficient way.

    A python implementation of Knuth's "Algorithm L", also known from the
    std::next_permutation function of C++, and as the permutation algorithm
    of Narayana Pandita.
    :param seq: sequence to which we want the unique permutations.
    """
    # Precalculate the indices we'll be iterating over for speed
    i_indices = range(len(seq) - 1, -1, -1)
    k_indices = i_indices[1:]

    # The algorithm specifies to start with a sorted version
    seq = sorted(seq)

    while True:
        yield seq

        # Working backwards from the last-but-one index,
        # we find the index of the first decrease in value.
        for k in k_indices:
            if seq[k] < seq[k + 1]:
                break
        else:
            # Introducing the slightly unknown python for-else syntax:
            # else is executed only if the break statement was never reached.
            # If this is the case, seq is weakly decreasing, and we're done.
            return

        # Get item from sequence only once, for speed
        k_val = seq[k]

        # Working backwards starting with the last item,
        # find the first one greater than the one at k
        for i in i_indices:
            if k_val < seq[i]:
                break

        # Swap them in the most efficient way
        (seq[k], seq[i]) = (seq[i], seq[k])

        # Reverse the part after but not
        # including k, also efficiently.
        seq[k + 1:] = seq[-1:k:-1]

if __name__ == "__main__":
    solve(7, ["K", "K", "Q", "Q", "B", "B", "Kn"])
