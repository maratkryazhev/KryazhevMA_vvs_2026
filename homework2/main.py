from functions import *

while True:
    print('Введите номер уровня: ', end = '')
    try:
        x = int(input())
    except ValueError:
        print('Данные некорректны!')
        continue
    if x == 1:
        def1()
    elif x == 2:
        def2()
    elif x == 3:
        def3()
    elif x == 4:
        def4()
    elif x == 5:
        def5()
    else:
        print('Такого уровня не существует!')
    w = str(input('Продолжить? Введите "да" или "нет": '))
    if w.strip().lower() == 'нет':
        break
