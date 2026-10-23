import random
from labirint import generate_labirint, show_labirint
from player import make_player, player_pos, try_move
from items import inventory_str
from events import change_room, player_has_key


def main():
    random.seed(1)
    n, m = 5, 6

    labirint, visited = generate_labirint(n, m)
    player = make_player(0, 0)
    visited[0][0] = True

    while True:
        print()
        show_labirint(labirint, visited, player_pos(player), n, m)
        print('HP:', player.hp, '| Ключ:', 'да' if player_has_key(player) else 'нет')
        print('Инвентарь:', inventory_str(player.inventory))
        print('w/a/s/d - идти, q - выход')

        cmd = input('Ваш ход: ').lower()
        if cmd == 'q':
            print('Пока!')
            break
        if not try_move(player, cmd, n, m):
            print('Туда нельзя!')
            continue

        px, py = player_pos(player)
        if not visited[px][py]:
            visited[px][py] = True
            change_room(labirint[px][py], player)


if __name__ == '__main__':
    main()
