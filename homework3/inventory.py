import copy
from items import item_str, inventory_str
from events import use_mana_potion_on_weapon, use_heal_potion_outside_combat

type_order = {
    'weapon': 0,
    'armor': 1,
    'potion': 2,
    'mana_potion': 3,
    'key': 4,
    'scroll': 5,
    'treasure': 6,
}

def sort_key(item):
    '''Критерий сортировки: сначала по типу, потом по имени'''
    order = type_order.get(item.type, 99)
    return (order, item.name)

def find_index_by_name(player, name):
    '''Позиция предмета по имени через index(); -1, если нет'''
    names = [k.name for k in player.inventory]
    if name in names:
        return names.index(name)
    return -1

def open_inventory(player):
    '''Меню инвентаря, возвращает None'''
    while True:
        print()
        print('=== ИНВЕНТАРЬ ===')
        if not player.inventory:
            print('Пусто')
            print('0 - назад')
            c = input('> ')
            if c == '0':
                return
            continue

        for i in range(len(player.inventory)):
            print('  ' + str(i) + ': ' + item_str(player.inventory[i]))
        
        print('Действия:')
        print('  1 - выбросить по имени')
        print('  2 - выбросить по индексу')
        print('  3 - сортировать по типу и имени')
        print('  4 - сортировать по убыванию')
        print('  5 - перевернуть порядок')
        print('  6 - найти предмет')
        print('  7 - копия и срез')
        print('  8 - ДЕМОНСТРАЦИЯ: copy() VS deepcopy()')
        print('  9 - применить предмет к предмету')
        print('  0 - назад')

        c = input('> ')
        if c == '0':
            return

        elif c == '1':
            # remove по имени
            name = input('Имя предмета: ')
            names = [k.name for k in player.inventory]
            if name in names:
                for k in player.inventory:
                    if k.name == name:
                        player.inventory.remove(k)
                        print('Удалено: ' + item_str(k))
                        break
            else:
                print('Нет такого предмета')

        elif c == '2':
            # pop по индексу
            ans = input('Индекс: ')
            try:
                idx = int(ans)
            except ValueError:
                print('Нужно число!')
                continue
            if idx < 0 or idx >= len(player.inventory):
                print('Неверный индекс!')
                continue
            removed = player.inventory.pop(idx)
            print('Удалено: ' + item_str(removed))

        elif c == '3':
            # sort с критерием
            player.inventory.sort(key=sort_key)
            print('Отсортировано по типу и имени')

        elif c == '4':
            # sort(reverse=True): и sort, и reverse за раз
            player.inventory.sort(key=sort_key, reverse=True)
            print('Отсортировано по убыванию')

        elif c == '5':
            # reverse: переворачивает текущий порядок
            player.inventory.reverse()
            print('Порядок перевёрнут')

        elif c == '6':
            # index + in
            name = input('Что ищем? ')
            idx = find_index_by_name(player, name)
            if idx == -1:
                print('Не найдено')
            else:
                print('Найдено на позиции ' + str(idx) + ': ' + item_str(player.inventory[idx]))

        elif c == '7':
            # copy + slice
            inv_copy = player.inventory.copy()
            print()
            print('Копия: ' + str(len(inv_copy)) + ' предметов')
            print('  ' + inventory_str(inv_copy))

            first_three = inv_copy[:3]
            print('Первые три:')
            print('  ' + inventory_str(first_three))

            print()
            print('ВНИМАНИЕ: copy() — поверхностное!')
            print('Предметы в копии — те же объекты, что в оригинале.')
            print('Команда 8 покажет, почему это проблема.')

        elif c == '8':
            demonstrate_copy_problem(player)

        elif c == '9':
            # применить предмет к предмету
            print('Что применяем?')
            for i in range(len(player.inventory)):
                print('  ' + str(i) + ': ' + item_str(player.inventory[i]))
            ans1 = input('Индекс: ')
            try:
                idx1 = int(ans1)
            except ValueError:
                print('Нужно число!')
                continue
            if idx1 < 0 or idx1 >= len(player.inventory):
                print('Неверный индекс!')
                continue
            
            item_a = player.inventory[idx1]

            # зелье здоровья - применяется к игроку (второй индекс не нужен)
            if item_a.type == 'potion':
                use_heal_potion_outside_combat(player, idx1)
                continue

            # зелье маны - применяется к оружию (нужен второй индекс)
            if item_a.type == 'mana_potion':
                ans2 = input('К какому оружию? индекс: ')
                try:
                    idx2 = int(ans2)
                except ValueError:
                    print('Нужно число!')
                    continue
                if idx2 < 0 or idx2 >= len(player.inventory):
                    print('Неверный индекс!')
                    continue
                use_mana_potion_on_weapon(player, idx1, idx2)
                continue
            
            print('Этот предмет нельзя применить')
        
        else:
            print('Нет такой команды')

def demonstrate_copy_problem(player):
    '''Показать разницу между copy() и deepcopy() на практике'''
    if not player.inventory:
        print('Инвентарь пуст — нечего копировать')
        return

    # ищем первый предмет, у которого есть хоть одно свойство (props)
    idx = -1
    for i in range(len(player.inventory)):
        if player.inventory[i].props:
            idx = i
            break

    if idx == -1:
        print('Нет предметов со свойствами — не на чем демонстрировать')
        return

    prop_key = None
    for k in player.inventory[idx].props:
        prop_key = k
        break
    old_value = player.inventory[idx].props[prop_key]

    print()
    print('=== ДЕМОНСТРАЦИЯ: copy() VS deepcopy() ===')
    print('Работаем с предметом: ' + item_str(player.inventory[idx]))
    print('Свойство: ' + prop_key + ' (сейчас ' + str(old_value) + ')')

    print()
    print('--- copy() (поверхностное) ---')
    shallow = player.inventory.copy()
    print('Создана копия: .copy()')
    shallow[idx].props[prop_key] = old_value + 100
    print('У копии поменяли ' + prop_key + ': ' + str(old_value) + ' -> ' + str(old_value + 100))
    print()
    print('Что стало:')
    print('  Копия:    ' + inventory_str(shallow))
    print('  Оригинал: ' + inventory_str(player.inventory))

    if player.inventory[idx].props[prop_key] == old_value + 100:
        print()
        print('!!! ПРОБЛЕМА: оригинал ТОЖЕ изменился!')
        print('copy() копирует только список, а предметы внутри - те же объекты')
        print('Поменяли в копии - поменяли и в оригинале')
        # восстанавливаем оригинал, чтобы игра не сломалась
        player.inventory[idx].props[prop_key] = old_value
        print('(восстановили оригинал на ' + str(old_value) + ')')

    print()
    print('--- deepcopy() (глубокое) ---')
    deep = copy.deepcopy(player.inventory)
    print('Создана копия: copy.deepcopy()')
    deep[idx].props[prop_key] = old_value + 100
    print('У копии поменяли ' + prop_key + ': ' + str(old_value) + ' -> ' + str(old_value + 100))
    print()
    print('Что стало:')
    print('  Копия:    ' + inventory_str(deep))
    print('  Оригинал: ' + inventory_str(player.inventory))

    if player.inventory[idx].props[prop_key] == old_value:
        print()
        print('Хмм, оригинал НЕ изменился - deepcopy скопировал и предметы тоже.')

    print()
    print('Вывод: в игре используем deepcopy, чтобы предметы в копиях были независимы')
    print('Именно так мы делаем в labirint.py при создании предметов из loot_pool')
