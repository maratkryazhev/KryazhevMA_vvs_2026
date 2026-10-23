class Player:
    '''Игрок в лабиринте'''
    x = 0
    y = 0
    hp = 100
    inventory = None

def make_player(x, y):
    '''Создать игрока'''
    p = Player()
    p.x = x
    p.y = y
    p.hp = 100
    p.inventory = []
    return p

def player_pos(player):
    '''Координаты игрока кортежем'''
    return (player.x, player.y)

def try_move(player, dv, n, m):
    '''Попытка сдвинуть игрока'''
    nx = player.x
    ny = player.y
    if dv == 'w':
        nx = nx-1
    elif dv == 's':
        nx = nx+1
    elif dv == 'a':
        ny = ny-1
    elif dv == 'd':
        ny = ny+1
    else:
        return False

    if nx < 0 or nx >= n or ny < 0 or ny >= m:
        return False

    player.x = nx
    player.y = ny
    return True
