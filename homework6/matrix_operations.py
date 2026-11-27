def transpose(matrix):
    '''Возвращает транспонированную матрицу'''
    return [list(row) for row in zip(*matrix)]

def add_matrices(A, B):
    '''Сложение двух матриц одинакового размера'''
    rows = len(A)
    cols = len(A[0])
    return [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]

def multiply_by_scalar(A, scalar):
    '''Умножение матрицы A на число'''
    return [[elem * scalar for elem in row] for row in A]

def multiply_matrices(A, B):
    '''Умножение матрицы A на матрицу B'''
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    # Матрица результата
    C = [[0 for j in range(cols_B)] for i in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def get_identity(n):
    '''Генерирует единичную матрицу размера n*n'''
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def get_zero(n, m):
    '''Генерирует нулевую матрицу размера n*m'''
    return [[0.0 for j in range(m)] for i in range(n)]

def get_main_diagonal(matrix):
    '''Возвращает список элементов главной диагонали (только для квадратных матриц)'''
    return [matrix[i][i] for i in range(len(matrix))]

def get_determinant(A):
    '''Поиск определителя, поддерживает любую размерность'''
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]

    det = 0
    for c in range(n):
        det += ((-1)**c) * A[0][c] * get_determinant(get_minor(A, 0, c))
    return det

# Вспомогательный функции для обратной матрицы

def get_minor(A, i, j):
    '''Возвращает минор для элемента с индексом (i, j)'''
    return [k[:j] + k[j+1:] for k in (A[:i] + A[i+1:])]

def inverse_matrix(A):
    '''Нахождение обратной матрицы через алгебраические дополнения'''
    n = len(A)
    det = get_determinant(A)
    
    if det == 0:
        raise ValueError('Определитель равен нулю. Обратной матрицы не существует!')
        
    # Матрица алгебраических дополнений
    cofactors = []
    for r in range(n):
        row = []
        for c in range(n):
            minor = get_minor(A, r, c)
            minor_det = get_determinant(minor)
            cofactor = ((-1) ** (r + c)) * minor_det
            row.append(cofactor)
        cofactors.append(row)
    
    # Транспонируем и делим на определитель
    A_01 = transpose(cofactors)
    return [[elem / det for elem in row] for row in A_01]
