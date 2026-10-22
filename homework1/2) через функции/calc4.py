from functions4 import *

a = int(input('Введите первое число: '))
zn = str(input('Введите знак операции: '))
b = int(input('Введите второе число: '))
print('Ответ:', end = ' ')
if zn == '+':
    print(summa(a,b))
elif zn == '-':
    print(raznost(a,b))
elif zn == '*':
    print(proizvedenie(a,b))
elif zn == '/':
    print(delenie(a,b))
else:
    print('Введены неверные значения!')
доп. файл: def summa(a, b):
    '''возвращает сумму двух чисел'''
    return (a+b)
