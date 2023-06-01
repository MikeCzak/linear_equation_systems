from linear_systems import MatrixForm, PivotSort

# Beispiel aus Foliensatz:
m3 = MatrixForm([
        [-7, 4, -2],
        [4, 6, 1],
        [-1, 1, 3]
    ], [[2], [-5], [4]], PivotSort.NO_SORT)

print(m3)
m3.jacobi_step(0, epsilon=10**-6)

# m3sortmax = MatrixForm([
#         [4, 6, 1],
#         [-7, 4, -2],
#         [-1, 1, 3]
#     ], [[-5], [2], [4]], PivotSort.NO_SORT)
# m3sortmax.jacobi_step(0, epsilon=10**-6)

# 2 Direkte Lösungsverfahren
# 2.1 a

# m3 = MatrixForm([
#     [4, -2, 6],
#     [3, 2, 0],
#     [1, 2, -1]
# ], [[-49], [9], [9]], pivot_sort=PivotSort.NO_SORT)




