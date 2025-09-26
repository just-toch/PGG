from board import GameSquare
from utils.gsheets import create_review
from utils.game import new_game, show_full_map, show_tokens, names, descriptions, show_map, open_squares, load_game, \
    save_game, check_victory


def new_game_ui():
    player_name = input('Введите свое имя:\n')
    player = new_game(player_name)
    main_game(player)

def main_game(player):
    if player is None:
        return None
    show_full_map(player)
    print()
    show_tokens(player)
    show_menu()
    menu(player)
    return None

def show_menu():
    print('Введите номер команды:')
    print('1. Имя и описание клетки')
    print('2. Открыть клетку')
    print('3. Зачистить клетку')
    print('4. Показать карту')
    # print('5. Сохранить')
    print('5. Загрузка')
    print('6. Написать отзыв')
    print('0. Сохранить и выйти')

def menu(player):
    while True:
        command = input()
        match command:
            case '1':
                coords = input('Введите координаты клетки:\n')
                x, y = int(coords[0]), int(coords[1])
                if (isinstance(player.field[x][y], GameSquare) and player.field[x][y].status != 'closed' or
                        player.field[x][y].status != 'available'):
                    name_index, description_index = player.field[x][y].data()
                    print(names[name_index])
                    print(descriptions[description_index])
                    print(player.field[x][y].status)
                else:
                    print('Вы не можете смотреть описание клетки, если она не открыта')

            case '2':
                if player.tokens > 0:
                    print('Доступные клетки:')
                    show_map('available', player)
                    coords = input('Введите координаты клетки:\n')
                    x, y = int(coords[0]), int(coords[1])
                    if player.field[x][y].status == 'available':
                        player.field[x][y].change_to_opened()
                        print(f'Клетка {player.field[x][y].coordinates()} открыта')
                        open_squares(player.field[x][y], player)
                        player.tokens -= 1
                    else:
                        print('Выбрана неверная клетка')
                else:
                    print('Сейчас вы не можете открыть клетку')

            case '3':
                print('Доступные клетки:')
                show_map('opened', player)
                coords = input('Введите координаты клетки:\n')
                x, y = int(coords[0]), int(coords[1])
                if player.field[x][y].status == 'opened':
                    # command = input('Вы прошли игру?\n1. Да\n2. Нет\n')
                    # if command == '1':
                    player.field[x][y].change_to_cleared()
                    print('Игра пройдена, клетка зачищена')
                    print(player.field[x][y].coordinates())
                    print(player.field[x][y].status)
                    player.tokens += 3
                    # elif command == '2':
                    #     print('На нет и суда нет')
                else:
                    print('Выбрана неверная клетка')

            case '4':
                show_full_map(player)

            # case '5':
            #     save_game(player)

            case '5':
                new_player = load_game(player)
                if new_player is not None:
                    player = new_player

            case '6':
                create_review(player.name.lower())

            case '0':
                save_game(player)
                break

        if check_victory(player):
            print('Ура, победа!')
            break
        print()
        show_tokens(player)
        show_menu()