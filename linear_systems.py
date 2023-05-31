class MatrixForm:
    def __init__(self, matrix: list[list[int]], x: list[int], b: list[int]):
        if len(matrix) != len(matrix[0]):
            raise IndexError("Only square matrices are allowed - one equation per variable")
        for row in matrix:
            if len(row) != len(matrix):
                raise IndexError("Only square matrices are allowed - number of rows and columns must be equal in each row")
        if len(matrix[0]) != len(x):
            raise IndexError("Invalid number of variables - one variable for each constant")
        if len(x) != len(b):
            raise IndexError("Invalid number of equals - each equation mus have a 'right side' of the equals-sign")
        self.matrix = matrix
        self.sorted_matrix = self.get_sorted_matrix()
        self.x = x
        self.b = b
        self._zero_matrix = [[0 for _ in self.sorted_matrix] for _ in self.sorted_matrix]
        self.diag_matrix = self.get_diag_matrix()
        self.bottom_left_matrix = self.get_left_matrix()
        self.top_right_matrix = self.get_right_matrix()
        self.left_and_right_matrix = self.combine_lr(self.bottom_left_matrix, self.top_right_matrix)

    def get_sorted_matrix(self) -> list[list[int]]:
        row = 0
        col = 0
        matrix = [x[:] for x in self.matrix]
        for _ in range(len(matrix)):
            max_el_in_col = matrix[row][col]
            for _ in range(len(matrix)):
                if matrix[row][col] > max_el_in_col:
                    max_el_in_col = row
                row += 1
            temp_row = [x for x in matrix[col]]
            matrix[col] = [x for x in matrix[max_el_in_col]]
            matrix[max_el_in_col] = [x for x in temp_row]
            col += 1
            row = 0

        return matrix


    def get_diag_matrix(self) -> list[list[int]]:
        diag_matrix = [x[:] for x in self._zero_matrix]
        for row in range(0, len(self.sorted_matrix)):
            diag_matrix[row][row] = self.sorted_matrix[row][row]
        return diag_matrix

    def get_left_matrix(self) -> list[list[int]]:
        left_matrix = [x[:] for x in self._zero_matrix]
        i = 1
        for row in range(1, len(self.sorted_matrix)):
            for col in range(i):
                left_matrix[row][col] = self.sorted_matrix[row][col]
            i += 1
        return left_matrix

    def get_right_matrix(self) -> list[list[int]]:
        right_matrix = [x[:] for x in self._zero_matrix]
        i = 1
        for row in range(len(self.sorted_matrix)):
            for col in range(i, len(self.sorted_matrix[row])):
                right_matrix[row][col] = self.sorted_matrix[row][col]
            i += 1
        return right_matrix

    def combine_lr(self, l, r) -> list[list[int]]:
        lr_matrix = [x[:] for x in l]
        for row in range(len(l)):
            for col in range(len(l[row])):
                if l[row][col] == 0:
                    lr_matrix[row][col] = r[row][col]
        return lr_matrix


m6 = MatrixForm([
    [1, 2, 3, 4, 5, 7],
    [2, 2, 3, 4, 5, 6],
    [1, 3, 3, 4, 5, 6],
    [1, 2, 4, 4, 5, 6],
    [1, 2, 3, 5, 5, 6],
    [1, 2, 3, 4, 6, 6],
], [10, 11, 12, 1, 1, 1], [13, 14, 15, 1, 1, 1])


print(f"\nDiagonalmatrix:")
for row in range(len(m6.diag_matrix)):
    print(m6.diag_matrix[row])

print(f"\nLinke untere Matrix:")
for row in range(len(m6.bottom_left_matrix)):
    print(m6.bottom_left_matrix[row])

print(f"\nRechte obere Matrix:")
for row in range(len(m6.top_right_matrix)):
    print(m6.top_right_matrix[row])

print(f"\nL+R:")
for row in range(len(m6.left_and_right_matrix)):
    print(m6.left_and_right_matrix[row])

