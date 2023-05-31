import math
import time
import os
from enum import Enum


class PivotSort(Enum):  # TODO: ask for callability, how do I make min/max a callback?
    MAX = 1
    NO_SORT = False
    MIN = -1


class MatrixForm:
    def __init__(self, matrix: list[list[int]], b: list[list[int]], pivot_sort: PivotSort):
        if not isinstance(pivot_sort, PivotSort):
            raise TypeError("pivot_sort must be MAX, NO_SORT, or MIN")
        if len(matrix) != len(matrix[0]):
            raise IndexError("Only square matrices are allowed - one equation per variable")
        for row in matrix:
            if len(row) != len(matrix):
                raise IndexError("Only square matrices allowed - number of rows and columns must be equal in each row")
        if len(matrix[0]) != len(b):
            raise IndexError("Matrix size does not match result vector")
        self.matrix = matrix
        self.b = b
        if pivot_sort == PivotSort.NO_SORT:
            self.pivot_sorted_matrix = self.matrix
        else:
            self.pivot_sorted_matrix = self.get_pivot_sorted_matrix(pivot_sort)
        self._zero_matrix = [[0 for _ in self.matrix] for _ in self.matrix]
        self.diag_matrix = self._get_diag_matrix()
        self.inv_diag_matrix = self.get_inv_diag_matrix()
        self.bottom_left_matrix = self.get_bottom_left_matrix()
        self.top_right_matrix = self.get_top_right_matrix()
        self.left_and_right_matrix = self.add_matrices(self.bottom_left_matrix, self.top_right_matrix)
        self.inv_diag_matrix_times_b = self.get_inv_diag_times_b()
        self.inv_diag_matrix_times_lr = self.get_inv_diag_times_lr()

    def get_pivot_sorted_matrix(self, pivot_sort) -> list[list[int]]:
        matrix = [x[:] for x in self.matrix]

        for col in range(len(matrix[0])):
            row_with_max_el_in_col = self.get_row_of_min_or_max_value_of_column(matrix[col:], col, pivot_sort)
            temp_row = [x for x in matrix[col]]
            temp_b = self.b[col]
            matrix[col] = [x for x in matrix[row_with_max_el_in_col + col]]
            self.b[col] = self.b[row_with_max_el_in_col + col]
            matrix[row_with_max_el_in_col + col] = [x for x in temp_row]
            self.b[row_with_max_el_in_col + col] = temp_b
        return matrix

    @staticmethod
    def get_row_of_min_or_max_value_of_column(matrix, col, pivot_sort):
        """
        returns the matrix\' row that contains the highest value in column
        :param matrix: matrix to check
        :param col: specified column
        :param pivot_sort: sort min or max value to diagonal
        :return: row number (posInt)
        """
        column = []
        for row in range(len(matrix)):
            column.append(matrix[row][col])
        match pivot_sort:
            case PivotSort.MAX:
                return column.index(max(column))
            case PivotSort.MIN:
                return column.index(min(column))

    def _get_diag_matrix(self) -> list[list[int]]:
        diag_matrix = [x[:] for x in self._zero_matrix]
        for row in range(0, len(self.pivot_sorted_matrix)):
            diag_matrix[row][row] = self.pivot_sorted_matrix[row][row]
        return diag_matrix

    def get_inv_diag_matrix(self) -> list[list[int]]:
        diag_inv_matrix = [x[:] for x in self.diag_matrix]
        for row in range(len(diag_inv_matrix)):
            for _ in range(len(diag_inv_matrix)):
                diag_inv_matrix[row][row] = 1 / diag_inv_matrix[row][row]
        return diag_inv_matrix

    def get_bottom_left_matrix(self) -> list[list[int]]:
        left_matrix = [x[:] for x in self._zero_matrix]
        i = 1
        for row in range(1, len(self.pivot_sorted_matrix)):
            for col in range(i):
                left_matrix[row][col] = self.pivot_sorted_matrix[row][col]
            i += 1
        return left_matrix

    def get_top_right_matrix(self) -> list[list[int]]:
        right_matrix = [x[:] for x in self._zero_matrix]
        i = 1
        for row in range(len(self.pivot_sorted_matrix)):
            for col in range(i, len(self.pivot_sorted_matrix[row])):
                right_matrix[row][col] = self.pivot_sorted_matrix[row][col]
            i += 1
        return right_matrix

    def get_inv_diag_times_b(self):
        return self.multiply_matrices(self.inv_diag_matrix, self.b)

    def get_inv_diag_times_lr(self):
        return self.multiply_matrices(self.inv_diag_matrix, self.left_and_right_matrix)

    @staticmethod
    def add_matrices(l, r) -> list[list[int]]:
        lr_matrix = [x[:] for x in l]
        for row in range(len(l)):
            for col in range(len(l[row])):
                lr_matrix[row][col] = r[row][col] + l[row][col]
        return lr_matrix

    @staticmethod
    def multiply_matrices(matrix1, matrix2):
        def get_product(row: int, col: int):
            prod = 0
            for i in range(len(matrix2)):
                prod += matrix1[row][i] * matrix2[i][col]
            return prod

        if len(matrix1[0]) != len(matrix2):
            raise ValueError("Width of matrix 1 must match height of matrix 2")
        multiplied_matrix = []
        for row in range(len(matrix1)):
            multiplied_matrix.append([])
            for col in range(len(matrix2[row])):
                multiplied_matrix[row].append(get_product(row, col))

        return multiplied_matrix

    def jacobi_step(self, start_value: int, epsilon: float = 10**-5):
        iterations = 0
        x0 = [start_value] * len(self.inv_diag_matrix_times_lr)
        xnext = [x for x in x0]
        difference = 1000
        while difference > epsilon or iterations == 1:
            os.system('clear')
            iterations += 1
            print(f"iteration {iterations}:")
            for equation in range(len(self.inv_diag_matrix_times_lr)):
                summands = []
                for coefficient in range(len(self.inv_diag_matrix_times_lr[equation])):
                    summands.append(self.inv_diag_matrix_times_lr[equation][coefficient] * x0[coefficient])
                xnext[equation] = -sum(summands) + self.inv_diag_matrix_times_b[equation][0]
                print(f"x{equation} = {xnext[equation]}")
            xnext_vector_length = 0
            for x in xnext:
                xnext_vector_length += x**2
            xnext_vector_length = math.sqrt(xnext_vector_length)
            x0_vector_length = 0
            for x in x0:
                x0_vector_length += x**2
            x0_vector_length = math.sqrt(x0_vector_length)
            difference = abs(xnext_vector_length - x0_vector_length)
            x0 = [x for x in xnext]
            print(f"Difference: {difference}")
            print(f"Epsilon   : {epsilon}")
            time.sleep(0.05)


if __name__ == "__main__":
    ausgeben = True

    m3 = MatrixForm([
        [-7, 4, -2],
        [4, 6, 1],
        [-1, 1, 3]
    ], [[2], [-5], [4]], pivot_sort=PivotSort.MAX)


    ausgabe = m3


    if ausgeben:

        print(f"\nMatrix nach Spaltenpivotisierung:")
        for row in range(len(ausgabe.pivot_sorted_matrix)):
            print(f"{ausgabe.pivot_sorted_matrix[row]} | {ausgabe.b[row]}")

        print(f"\nDiagonalmatrix:")
        for row in range(len(ausgabe.diag_matrix)):
            print(ausgabe.diag_matrix[row])

        print(f"\nInverse Diagonalmatrix:")
        for row in range(len(ausgabe.inv_diag_matrix)):
            print(ausgabe.inv_diag_matrix[row])

        print(f"\nLinke untere Matrix:")
        for row in range(len(ausgabe.bottom_left_matrix)):
            print(ausgabe.bottom_left_matrix[row])

        print(f"\nRechte obere Matrix:")
        for row in range(len(ausgabe.top_right_matrix)):
            print(ausgabe.top_right_matrix[row])

        print(f"\nL+R:")
        for row in range(len(ausgabe.left_and_right_matrix)):
            print(ausgabe.left_and_right_matrix[row])

        print(f"\nD-1 * L+R:")
        for row in range(len(ausgabe.inv_diag_matrix_times_lr)):
            print(ausgabe.inv_diag_matrix_times_lr[row])

        print(f"\nD-1 * b:")
        for row in range(len(ausgabe.inv_diag_matrix_times_b)):
            print(ausgabe.inv_diag_matrix_times_b[row])
