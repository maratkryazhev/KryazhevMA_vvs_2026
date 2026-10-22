a = int(input('Введите первое число: '))
zn = str(input('Введите знак операции: '))
b = int(input('Введите второе число: '))

print('Ответ:', end=' ')
if zn == '+':
    print(a + b)
elif zn == '-':
    print(a - b)
elif zn == '*':
    print(a * b)
elif zn == '/':
    print(a / b)
else:
    print('Введены неверные значения!')
