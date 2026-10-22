def f(a, b, zn):
    '''Вернуть результат действия с двумя числами'''
    if zn == '+':
        return a+b
    elif zn == '-':
        return a-b
    elif zn == '*':
        return a*b
    else:
        return a/b
