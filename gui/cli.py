from utils.game import new_game, open_squares, load_game, save_game, check_victory
from pathlib import Path
from board import GameSquare
from json import decoder


def main_menu():
    while True:
        print('1. Новая игра')
        print('2. Загрузка')
        print('3. Загрузка из облака')
        print('4. Посмотреть статистику других игроков')
        print('0. Выход')

        command = input()
        match command:
            case '1':
                player = new_game_ui()
                menu(player)

            case '2':
                player = load_game_ui()
                menu(player)

            case '3':
                worksheet_list = get_worksheet_list()
                print('Выберите сохранение:')
                for i, worksheet_name in enumerate(worksheet_list[1:], 1):
                    print(f'{i}. {worksheet_name.title}')
                print(f'0. Отмена')
                savegame = int(input())
                if savegame == 0:
                    continue
                name = worksheet_list[savegame].title
                menu(load_game_from_cloud(name))

            case '4':
                player_list = get_worksheet_list()
                print('Выберите игрока:')
                for i, worksheet_name in enumerate(player_list[1:], 1):
                    print(f'{i}. {worksheet_name.title}')
                print(f'0. Отмена')
                player_number = int(input())
                player = get_player_stats(player_list, player_number)
                print('1. Посмотреть карту')
                print('2. Посмотреть обзоры')
                print('0. Выход')
                command = input()
                match command:
                    case '1':
                        show_full_map(player)

                    case '2':
                        for i in range(len(player.games_list)):
                            print(f'{i + 1}. {player.games_list[i]}')
                            print(player.review_list[i])
                            print()

            case '0':
                break


def new_game_ui():
    player_name = input('Введите свое имя:\n')
    if create_player_worksheet(player_name):
        player = new_game(player_name)
    else:
        print('Такой игрок уже существует')
        try:
            player = load_game_from_cloud(player_name)
        except (decoder.JSONDecodeError, TypeError):
            print('Однако данных по нему нет или они повреждены, создаю нового пользователя')
            player = new_game(player_name)
    return player

def main_game(player):
    if player is None:
        return None
    show_full_map(player)
    print()
    menu(player)
    return None

def load_game_ui():
    path = Path()
    files = list(path.glob(f"{'savegame'}*{'.json'}"))
    print('Выберите сохранение:')
    for i, file in enumerate(files, 1):
        print(f'{i}. {file.name[9:-5]}')
    print(f'0. Отмена')
    savegame = int(input()) - 1
    if savegame == -1:
        return None
    player = load_game(savegame, files)
    return player

def show_map(status, player):
    for row in player.field:
        for square in row:
            if isinstance(square, GameSquare) and square.status == status:
                print(square.coordinates().rjust(3), end=' ')
            elif isinstance(square, GameSquare):
                print(square.mark.rjust(3), end=' ')
            else:
                print('X'.rjust(3), end=' ')
        print()

def show_full_map(player):
    for row in player.field:
        for square in row:
            if isinstance(square, GameSquare):
                print(square.mark.rjust(3), end=' ')
            else:
                print(square.rjust(3), end=' ')
        print()

def show_tokens(player):
    if player.tokens <= 0:
        print('Сейчас вы не можете открыть новую клетку, пройдите игру для получения токенов')
        return False
    if player.tokens == 1:
        print('Вы можете открыть 1 клетку')
    elif 5 > player.tokens > 1:
        print(f'Вы можете открыть {player.tokens} клетки')
    else:
        print(f'Вы можете открыть {player.tokens} клеток')
    return True

def show_menu():
    print('Введите номер команды:')
    print('1. Имя и описание клетки')
    print('2. Открыть клетку')
    print('3. Зачистить клетку')
    print('4. Показать карту')
    # print('5. Сохранить')
    # print('5. Загрузка')
    print('6. Написать отзыв')
    print('0. Сохранить и выйти')

def menu(player):
    show_tokens(player)
    show_menu()
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

            # case '5':
            #     new_player = load_game(player)
            #     if new_player is not None:
            #         player = new_player

            case '6':
                print('Напишите название игры')
                gamename = input()
                print('Напишите отзыв')
                review = input()
                create_review(player.name.lower(), gamename, review)

            case '0':
                save_game(player)
                break

        if check_victory(player):
            print('Ура, победа!')
            break
        print()
        show_tokens(player)
        show_menu()