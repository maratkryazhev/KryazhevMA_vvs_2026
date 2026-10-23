from items import item_str, inventory_str

def player_has_key(player):
    '''Есть ли ключ в инвентаре'''
    names = [w.name for w in player.inventory]
    return 'Ключ' in names

def change_room(room, player):
    '''Обработать события в комнате при ПЕРВОМ входе'''
    print()
    if room.type == 'empty':
        print('Пустая комната, ничего интересного')
    elif room.type == 'start':
        print('Это стартовая комната')
    elif room.type == 'chest':
        change_chest(room, player)
    elif room.type == 'key':
        change_key_room(room, player)
    elif room.type == 'monster':
        print('Монстр!')
    elif room.type == 'trap':
        print('Ловушка!')
    elif room.type == 'portal':
        print('Портал!')
    elif room.type == 'exit':
        print('Выход! Нужен ключ')

def change_chest(room, player):
    '''Сундук: забрать 1 предмет или несколько'''
    if not room.items:
        print('Сундук пуст')
        return

    print('В сундуке лежит: ' + inventory_str(room.items))
    ans = input('Забрать всё? (да/нет): ').lower()
    if ans != 'да':
        print('Вы оставили предметы в сундуке')
        return
    if len(room.items) == 1:
        player.inventory.append(room.items[0])
        print('Добавлено: ' + item_str(room.items[0]))
    else:
        player.inventory.extend(room.items)
        print('Добавлено предметов: ' + str(len(room.items)))
    room.items = []

def change_key_room(room, player):
    '''Комната с ключом: забрать ключ'''
    if not room.items:
        print('Здесь уже пусто')
        return

    print('В комнате находится ключ')
    ans = input('Забрать ключ? (да/нет): ').lower()
    if ans != 'да':
        print('Ключ остался на месте')
        return
    player.inventory.append(room.items[0])
    room.items = []
    print('Ключ добавлен в инвентарь')
