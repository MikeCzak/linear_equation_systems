class MatrixForm:
    def __init__(self, matrix: list[list[int]], b: list[int], pivot_sort=True):
        if len(matrix) != len(matrix[0]):
            raise IndexError("Only square matrices are allowed - one equation per variable")
        for row in matrix:
            if len(row) != len(matrix):
                raise IndexError("Only square matrices are allowed - number of rows and columns must be equal in each row")

        self.matrix = matrix
        if pivot_sort:
            self.pivot_sorted_matrix = self.get_pivot_sorted_matrix()
        else:
            self.pivot_sorted_matrix = self.matrix
        self.b = b
        self._zero_matrix = [[0 for _ in self.matrix] for _ in self.matrix]
        self.diag_matrix = self._get_diag_matrix()
        self.inv_diag_matrix = self.get_inv_diag_matrix()
        self.bottom_left_matrix = self.get_bottom_left_matrix()
        self.top_right_matrix = self.get_top_right_matrix()
        self.left_and_right_matrix = self.add_matrices(self.bottom_left_matrix, self.top_right_matrix)

    def get_pivot_sorted_matrix(self) -> list[list[int]]:
        matrix = [x[:] for x in self.matrix]

        for col in range(len(matrix[0])):
            row_with_max_el_in_col = self.get_row_of_max_value_of_column(matrix[col:], col)
            temp_row = [x for x in matrix[col]]
            matrix[col] = [x for x in matrix[row_with_max_el_in_col + col]]
            matrix[row_with_max_el_in_col + col] = [x for x in temp_row]
        return matrix

    @staticmethod
    def get_row_of_max_value_of_column(matrix, col):
        """
        returns the matrix\' row that contains the highest value in column
        :param matrix: matrix to check
        :param col: specified column
        :return: row number (posInt)
        """
        column = []
        for row in range(len(matrix)):
            column.append(matrix[row][col])
        return column.index(max(column))

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



class LinearSystem:
    pass



if __name__ == "__main__":
    ausgeben = True


    m6 = MatrixForm([
        [1,   2,  3,  4,  5,  6],
        [7,   8,  9, 10, 11, 12],
        [13, 14, 15, 16, 17, 18],
        [19, 20, 21, 22, 23, 24],
        [25, 26, 27, 28, 29, 30],
        [31, 32, 33, 34, 35, 36],
    ], [13, 14, 15, 1, 1, 1], False)

    m3 = MatrixForm([
        [-7, 4, -2],
        [4, 6, 1],
        [-1, 1, 3]
    ], [2, -5, 4], False)


    ausgabe = m3


    if ausgeben:

        print(f"\nMatrix nach Spaltenpivotisierung:")
        for row in range(len(ausgabe.pivot_sorted_matrix)):
            print(ausgabe.pivot_sorted_matrix[row])

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

