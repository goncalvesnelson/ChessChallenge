
import unittest
from src import chess


class Test(unittest.TestCase):

    def setUp(self):
        # Create 4*4 board to run tests
        self.board = [[False] * 4 for _ in range(4)]
        self.board_size = len(self.board)

    def test_get_bishop_pos(self):
        self.assertEquals(chess._get_bishop_pos(self.board_size, 0, 0),
                          set([(1, 1), (2, 2), (3, 3)]))
        self.assertEquals(chess._get_bishop_pos(self.board_size, 2, 2),
                          set([(3, 3), (1, 1), (0, 0), (3, 1), (1, 3)]))
        self.assertEquals(chess._get_bishop_pos(self.board_size, 0, 3),
                          set([(1, 2), (2, 1), (3, 0)]))
        self.assertEquals(chess._get_bishop_pos(self.board_size, 3, 0),
                          set([(1, 2), (0, 3), (2, 1)]))
        self.assertEquals(chess._get_bishop_pos(self.board_size, 3, 3),
                          set([(0, 0), (1, 1), (2, 2)]))

    def test_get_king_pos(self):
        self.assertEquals(chess._get_king_pos(self.board_size, 0, 0),
                          set([(0, 1), (1, 0), (1, 1)]))
        self.assertEquals(chess._get_king_pos(self.board_size, 2, 2),
                          set([(1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (2, 1),
                               (2, 3), (1, 1)]))
        self.assertEquals(chess._get_king_pos(self.board_size, 0, 3),
                          set([(1, 2), (1, 3), (0, 2)]))
        self.assertEquals(chess._get_king_pos(self.board_size, 3, 0),
                          set([(2, 0), (3, 1), (2, 1)]))
        self.assertEquals(chess._get_king_pos(self.board_size, 3, 3),
                          set([(3, 2), (2, 3), (2, 2)]))

    def test_get_knight_pos(self):
        self.assertEquals(chess._get_knight_pos(self.board_size, 0, 0),
                          set([(1, 2), (2, 1)]))
        self.assertEquals(chess._get_knight_pos(self.board_size, 2, 2),
                          set([(0, 1), (3, 0), (0, 3), (1, 0)]))
        self.assertEquals(chess._get_knight_pos(self.board_size, 0, 3),
                          set([(1, 1), (2, 2)]))
        self.assertEquals(chess._get_knight_pos(self.board_size, 3, 0),
                          set([(1, 1), (2, 2)]))
        self.assertEquals(chess._get_knight_pos(self.board_size, 3, 3),
                          set([(1, 2), (2, 1)]))

    def test_get_rook_pos(self):
        self.assertEquals(chess._get_rook_pos(self.board_size, 0, 0),
                          set([(0, 1), (3, 0), (0, 2), (2, 0), (1, 0),
                               (0, 3)]))
        self.assertEquals(chess._get_rook_pos(self.board_size, 2, 2),
                          set([(1, 2), (3, 2), (2, 1), (2, 0), (2, 3),
                               (0, 2)]))
        self.assertEquals(chess._get_rook_pos(self.board_size, 0, 3),
                          set([(0, 0), (0, 1), (0, 2), (1, 3), (2, 3),
                               (3, 3)]))
        self.assertEquals(chess._get_rook_pos(self.board_size, 3, 0),
                          set([(3, 2), (0, 0), (3, 3), (3, 1), (2, 0),
                               (1, 0)]))
        self.assertEquals(chess._get_rook_pos(self.board_size, 3, 3),
                          set([(3, 2), (1, 3), (3, 0), (3, 1), (2, 3),
                               (0, 3)]))

    def test_get_queen_pos(self):
        self.assertEquals(chess._get_queen_pos(self.board_size, 0, 0),
                          set([(0, 1), (3, 3), (3, 0), (0, 2), (2, 0), (2, 2),
                               (1, 0), (0, 3), (1, 1)]))
        self.assertEquals(chess._get_queen_pos(self.board_size, 2, 2),
                          set([(1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (2, 1),
                               (0, 2), (2, 0), (0, 0), (2, 3), (1, 1)]))
        self.assertEquals(chess._get_queen_pos(self.board_size, 0, 3),
                          set([(0, 1), (1, 2), (1, 3), (3, 3), (3, 0), (2, 1),
                               (0, 0), (2, 3), (0, 2)]))
        self.assertEquals(chess._get_queen_pos(self.board_size, 3, 0),
                          set([(1, 2), (3, 2), (0, 0), (3, 3), (3, 1), (2, 1),
                               (2, 0), (1, 0), (0, 3)]))
        self.assertEquals(chess._get_queen_pos(self.board_size, 3, 3),
                          set([(3, 2), (1, 3), (3, 0), (3, 1), (0, 0), (2, 3),
                               (2, 2), (0, 3), (1, 1)]))

    def test_get_positions(self):
        self.board[0][0] = True
        self.assertEquals(chess.get_positions(self.board, [(0, 0), (0, 1)]),
                          [True, False])

    def test_set_positions(self):
        self.assertEquals(self.board[0][0], False)
        self.assertEquals(self.board[0][1], False)
        chess.set_positions(self.board, [(0, 0), (0, 1)], True)
        self.assertEquals(self.board[0][0], True)
        self.assertEquals(self.board[0][1], True)

    def test_try_place_piece(self):
        # Try placing unknown type of piece
        with self.assertRaises(ValueError):
            chess.try_place_piece(self.board, "NON_existing", 0, 0)
        # try placing piece in empty board
        placed, queen_board = chess.try_place_piece(self.board,
                                                    chess.QUEEN_SYMBOL, 0, 0)
        self.assertEquals(placed, True)

        # cannot place piece in place where threatens existing piece
        self.assertEquals(
            chess.try_place_piece(queen_board, chess.KNIGHT_SYMBOL, 1, 2),
            (False, None)
        )
        # can place piece where it does not threaten nor is threatened by
        # another piece
        self.assertEquals(
            chess.try_place_piece(queen_board, chess.KNIGHT_SYMBOL, 1, 3),
            (True, [['Q', 'x', 'x', 'x'],  ['x', 'x', False, 'Kn'],
                    ['x', 'x', 'x', False], ['x', False, 'x', 'x']])
        )

    def test_unique_permutations(self):
        self.assertEquals(len(list(chess.unique_permutations(["Q"]*9))), 1)
        self.assertEquals(
            len(list(chess.unique_permutations(["Q", "Q", "R"]))), 3)

    def test_solve(self):
        self.assertEquals(chess.solve(8, ["Q"]*8, False), 92)
        self.assertEquals(chess.solve(3, ["K", "K", "R"], False), 4)
        self.assertEquals(chess.solve(4, ["Kn", "Kn", "Kn", "Kn", "R", "R"],
                                      False), 8)

if __name__ == "__main__":
    unittest.main()
