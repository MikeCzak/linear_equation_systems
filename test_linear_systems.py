import unittest
from linear_systems import MatrixForm


class TestLinearSystems(unittest.TestCase):
    def setUp(self) -> None:
        self.sut = MatrixForm([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ], [13, 14, 15], False)

    def test_init_not_square(self):
        with self.assertRaises(IndexError):
            self.sut = MatrixForm([
                [1, 2, 3, 10],
                [4, 5, 6, 11],
                [7, 8, 9, 12]
            ], [13, 14, 15], False)
            del self.sut
        with self.assertRaises(IndexError):
            self.sut = MatrixForm([
                [1, 2],
                [4, 5],
                [7, 8]
            ], [13, 14, 15], False)
            del self.sut
        with self.assertRaises(IndexError):
            self.sut = MatrixForm([
                [1, 2, 3],
                [4, 5, 6, 5],
                [7, 8, 9, 4]
            ], [13, 14, 15], False)

    def test_init_b_not_equal(self):
        with self.assertRaises(IndexError):
            self.sut = MatrixForm([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ], [13, 14, 15, 4], False)
        with self.assertRaises(IndexError):
            self.sut = MatrixForm([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ], [13, 14], False)

    def test_diag_matrix(self):
        self.assertEqual(self.sut.diag_matrix, [[1, 0, 0], [0, 5, 0], [0, 0, 9]])

    def test_inv_diag_matrix(self):
        expected = [
            [1.0, 0, 0],
            [0, 0.2, 0],
            [0, 0, 0.1111111111111111]
        ]
        self.assertListEqual(self.sut.inv_diag_matrix, expected)
