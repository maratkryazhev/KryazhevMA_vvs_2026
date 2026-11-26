class MatrixError(Exception):
    '''Кастомное исключение для ошибок валидации матриц'''
    pass

def parse_matrix(raw_data):
    '''
    Принимает список списков строк (текст из полей ввода GUI)
    Возвращает список списков float
    Если есть не-числа, выбрасывает MatrixError
    '''
    matrix = []
    for i, row in enumerate(raw_data):
        parsed_row = []
        for j, cell in enumerate(row):
            cell_str = str(cell).strip().replace(',', '.')
            if not cell_str:
                raise MatrixError(f"Пустая ячейка в строке {i+1}, столбце {j+1}")
            try:
                # Пробуем перевести в число с плавающей точкой
                val = float(cell_str)
                parsed_row.append(val)
            except ValueError:
                raise MatrixError(f"В ячейке ({i+1}, {j+1}) введено не число: '{cell}'")
        matrix.append(parsed_row)
    return matrix

def check_square(matrix):
    '''Проверяет, является ли матрица квадратной'''
    rows = len(matrix)
    cols = len(matrix[0])
    if rows != cols:
        raise MatrixError('Операция возможна только для квадратных матриц!')

def check_same_size(A, B):
    '''Проверяет, можно ли сложить матрицы (размеры должны совпадать)'''
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    if rows_A != rows_B or cols_A != cols_B:
        raise MatrixError(
            f"Размеры матриц не совпадают!\n"
            f"Матрица A: {rows_A}x{cols_A}\n"
            f"Матрица B: {rows_B}x{cols_B}\n"
            f"Для сложения они должны быть одинаковыми!"
        )

def check_multiplication(A, B):
    '''Проверяет, можно ли умножить A на B (кол-во столбцов A равно кол-ву строк B)'''
    cols_A = len(A[0])
    rows_B = len(B)
    
    if cols_A != rows_B:
        raise MatrixError(
            f"Число столбцов матрицы A ({cols_A}) не равно числу строк матрицы B ({rows_B}).\n"
            f"Матрицы нельзя умножить!"
        )

def check_scalar(scalar_str):
    '''Проверяет, что введенное число корректно'''
    s_str = str(scalar_str).strip().replace(',', '.')
    if not s_str:
        raise MatrixError('Введите число, на которое нужно умножить')
    try:
        return float(s_str)
    except ValueError:
        raise MatrixError(f"Введено некорректное число: '{scalar_str}'")
