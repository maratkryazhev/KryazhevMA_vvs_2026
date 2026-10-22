from calculator import Calculator
calc = Calculator()

while True:
    try:
        a = int(input('Введите первое число: '))
    except ValueError:
        print('Нужно было ввести число!')
        break
    zn = str(input('Введите знак операции: '))
    try:
        b = int(input('Введите второе число: '))
    except ValueError:
        print('Нужно было ввести число!')
        break
    if zn == '/' and b == 0:
        print('На ноль делить нельзя!')
    elif zn in ('+', '-', '*', '/'):
        print('Ответ:', calc.calculate(a, b, zn))
    else:
        print('Введены неверные значения!')
    pr = str(input('Продолжить? '))
    if pr.strip().lower() == 'нет':
        break
