import random
from items import make_item, item_str, inventory_str

def get_weapon_damage(player):
    '''Суммарный бонус урона от оружия в инвентаре'''
    total = 0
    for k in player.inventory:
        if k.type == 'weapon':
            total += k.props.get('damage', 0)
    return total

def get_block(player):
    '''Суммарный блок от брони в инвентаре'''
    total = 0
    for k in player.inventory:
        if k.type == 'armor':
            total += k.props.get('block', 0)
    return total

def player_has_key(player):
    '''Есть ли ключ в инвентаре'''
    names = [w.name for w in player.inventory]
    return 'Ключ' in names

def change_room(room, player, labirint, visited):
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
        change_monster(room, player)
    elif room.type == 'trap':
        change_trap(room, player)
    elif room.type == 'portal':
        change_portal(room, player, labirint, visited)
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

def change_monster(room, player):
    '''Бой с монстром'''
    if room.data.get('defeated'):
        print('Здесь лежит побеждённый монстр')
        return
    if 'hp' not in room.data:
        room.data['hp'] = random.randint(20, 40)
    monster_hp = room.data['hp']
    print('Монстр! У него ' + str(monster_hp) + ' HP')

    while monster_hp > 0 and player.hp > 0:
        print('Монстр: ' + str(monster_hp) + ' HP | Вы: ' + str(player.hp) + ' HP')
        cmd = input('1 - атака, 2 - предмет, 3 - бег: ')
        if cmd == '1':
            dmg = random.randint(5, 12) + get_weapon_damage(player)
            monster_hp -= dmg
            print('Вы нанесли ' + str(dmg) + ' урона')
        elif cmd == '2':
            use_item_in_combat(player)
        elif cmd == '3':
            if random.random() < 0.5:
                print('Вы сбежали!')
                room.data['hp'] = monster_hp
                return
            print('Не удалось сбежать!')
        else:
            continue

        if monster_hp > 0:
            incoming = random.randint(3, 12) - get_block(player)
            if incoming < 0:
                incoming = 0
            player.hp -= incoming
            print('Монстр бьёт на ' + str(incoming))

    if monster_hp <= 0:
        print('Монстр побеждён!')
        room.data['defeated'] = True
        reward = make_item('Золото', 'treasure', {'amount': 25})
        player.inventory.append(reward)
        print('Награда: ' + item_str(reward))

def use_item_in_combat(player):
    '''Использовать предмет из инвентаря'''
    if not player.inventory:
        print('Инвентарь пуст!')
        return
    print('Инвентарь: ')
    for i in range(len(player.inventory)):
        print(' ' + str(i) + ': ' + item_str(player.inventory[i]))
    ans = input('Индекс предмета (Enter - отмена): ')
    if ans == '':
        return
    try:
        idx = int(ans)
    except ValueError:
        print('Нужно число!')
        return
    if idx < 0 or idx >= len(player.inventory):
        print('Неверный индекс!')
        return
    it = player.inventory[idx]
    if it.type == 'potion':
        heal = it.props.get('heal', 0)
        player.hp += heal
        player.inventory.pop(idx)
        print('Использовано: ' + it.name + ', +' + str(heal) + ' HP')
    else:
        print('Этот предмет нельзя использовать в бою!')

def change_trap(room, player):
    '''Ловушка: урон, смягчается щитом'''
    if room.data.get('triggered'):
        print('Ловушка уже сработала')
        return
    dmg = random.randint(10, 25)
    block = get_block(player)
    final = dmg-block
    if final < 0:
        final = 0
    print('Ловушка! Урон: ' + str(dmg) + ', блок: ' + str(block))
    player.hp -= final
    room.data['triggered'] = True
    print('Потеряно ' + str(final) + ' HP')

def change_portal(room, player, labirint, visited):
    '''Портал: телепорт в другой портал'''
    n = len(labirint)
    m = len(labirint[0])
    other_portals = []
    for i in range(n):
        for j in range(m):
            if labirint[i][j].type == 'portal' and (i, j) != (player.x, player.y):
                other_portals.append((i, j))
    if not other_portals:
        print('Портал никуда не ведёт - других порталов нет')
        return

    dest = random.choice(other_portals)
    print('Портал! Вас телепортирует в (' + str(dest[0]) + ', ' + str(dest[1]) + ')')
    player.x = dest[0]
    player.y = dest[1]
    visited[dest[0]][dest[1]] = True

def use_mana_potion_on_weapon(player, potion_idx, weapon_idx):
    '''Применить зелье маны к оружию: +урон; меняется свойство предмета'''
    potion = player.inventory[potion_idx]
    weapon = player.inventory[weapon_idx]

    if potion.type != 'mana_potion':
        print('Это не зелье маны!')
        return

    if weapon.type != 'weapon':
        print('Маной можно усилить только оружие!')
        return

    bonus = potion.props.get('mana', 10)
    old = weapon.props.get('damage', 0)
    weapon.props['damage'] = old + bonus
    player.inventory.pop(potion_idx)
    print('Меч усилен! damage: ' + str(old) + ' -> ' + str(old + bonus))

def use_heal_potion_outside_combat(player, idx):
    '''Выпить зелье здоровья вне боя'''
    if idx < 0 or idx >= len(player.inventory):
        print('Неверный индекс!')
        return
    k = player.inventory[idx]
    if k.type != 'potion':
        print('Это не зелье здоровья!')
        return
    heal = k.props.get('heal', 0)
    player.hp = player.hp + heal
    player.inventory.pop(idx)
    print('Выпито: +' + str(heal) + ' HP, теперь HP = ' + str(player.hp))
