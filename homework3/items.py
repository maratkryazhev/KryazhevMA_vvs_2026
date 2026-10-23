class Item:
    '''Предмет в инвентаре'''
    name = ''
    type = ''
    props = None

def make_item(name, type_, props):
    '''Создать предмет'''
    item = Item()
    item.name = name
    item.type = type_
    item.props = props
    return item

def item_str(item):
    '''Печать одного предмета строкой'''
    if not item.props:
        return item.name + ' [' + item.type + ']'
    arr = []
    for k in item.props:
        arr.append(k + '=' + str(item.props[k]))
    return item.name + ' [' + item.type + '] (' + ', '.join(arr) + ')'

def inventory_str(inv):
    '''Печать всего инвентаря одной строкой'''
    if not inv:
        return '[]'
    arr = []
    for k in inv:
        arr.append(item_str(k))
    return '[' + ', '.join(arr) + ']'
