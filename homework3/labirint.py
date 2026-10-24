import random
import copy
from items import make_item

class Room:
    '''Одна клетка лабиринта'''
    type = ''
    items = None
    data = None

def make_room(type_, items, data):
    '''Создать комнату'''
    room = Room()
    room.type = type_
    room.items = items
    room.data = data
    return room

#Легенда карты
icons = {
    'start': 'S',
    'exit': 'E',
    'empty': '.',
    'chest': 'C',
    'monster': 'M',
    'trap': 'T',
    'key': 'K',
    'portal': 'P',
}
player_icon = '@'
unknown_icon = '?'
room_types = ['empty', 'chest', 'monster', 'trap', 'portal']
loot = [
    ('Золото', 'treasure', {'amount': 50}),
    ('Зелье здоровья', 'potion', {'heal': 30}),
    ('Зелье маны', 'mana_potion', {'mana': 10}),
    ('Меч', 'weapon', {'damage': 10}),
    ('Щит', 'armor', {'block': 5}),
    ('Свиток', 'scroll', {}),
    ]



def generate_labirint(n, m):
    '''Сгенерировать лабиринт n*m'''
    labirint = []
    for i in range(n):
        row = []
        for j in range(m):
            room = make_room(random.choice(room_types), [], {})
            row.append(room)
        labirint.append(row)

    visited = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(False)
        visited.append(row)

    labirint[0][0].type = 'start'
    labirint[n-1][m-1].type = 'exit'

    free = []
    for i in range(n):
        for j in range(m):
            if not(i == 0 and j == 0) and not(i == n-1 and j == m-1):
                free.append((i, j))
    kx, ky = random.choice(free)
    labirint[kx][ky].type = 'key'
    labirint[kx][ky].items = [make_item('Ключ', 'key', {})]

    for i in range(n):
        for j in range(m):
            if labirint[i][j].type == 'chest':
                if random.random() < 0.3:
                    labirint[i][j].items = []
                else:
                    count = random.randint(1, 3)
                    chosen = random.sample(loot, count)
                    items = []
                    for name, tp, props in chosen:
                        items.append(make_item(name, tp, copy.deepcopy(props)))
                    labirint[i][j].items = items
    
    return labirint, visited

def show_labirint(labirint, visited, pos, n, m):
    '''Нарисовать лабиринт'''
    for i in range(n):
        row = ''
        for j in range(m):
            if (i, j) == pos:
                row += player_icon + ' '
            elif visited[i][j]:
                row += icons[labirint[i][j].type] + ' '
            else:
                row += unknown_icon + ' '
        print(row)
