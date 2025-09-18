from board import GameSquare
from board import Player
from random import randrange
from pathlib import Path
from gsheets import get_load_from_cloud
import json


descriptions = [
    'Описание 1', 'Описание 2', 'Описание 3', 'Описание 4', 'Описание 5',
    'Описание 6', 'Описание 7', 'Описание 8', 'Описание 9', 'Описание 10',
    'Описание 11', 'Описание 12', 'Описание 13', 'Описание 14', 'Описание 15',
    'Описание 16', 'Описание 17', 'Описание 18', 'Описание 19', 'Описание 20',
    'Описание 21', 'Описание 22', 'Описание 23', 'Описание 24', 'Описание 25'
]

names = [
    'Имя 1', 'Имя 2', 'Имя 3', 'Имя 4', 'Имя 5',
    'Имя 6', 'Имя 7', 'Имя 8', 'Имя 9', 'Имя 10',
    'Имя 11', 'Имя 12', 'Имя 13', 'Имя 14', 'Имя 15',
    'Имя 16', 'Имя 17', 'Имя 18', 'Имя 19', 'Имя 20',
    'Имя 21', 'Имя 22', 'Имя 23', 'Имя 24', 'Имя 25'
]


def generate_game_field(game_field):
    for row in range(5):
        rows = []
        for column in range(5):
            index = randrange(len(names))
            name, description = names.pop(index), descriptions.pop(index)
            rows.append(GameSquare(column, row, name, description))
        game_field.append(rows)
    return game_field


def open_squares(square, player):
    coordinates = square.coordinates()
    for i in range(max(0, int(coordinates[0])-1), min(5, int(coordinates[0])+2)):
        for j in range(max(0, int(coordinates[1])-1), min(5, int(coordinates[1])+2)):
            player.field[i][j].change_to_available()


def save_game(player):
    filename = f'savegame_{player.name.lower()}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(player.save(), f, ensure_ascii=False)


def load_game(player=None):
    path = Path()
    files = list(path.glob(f"{'savegame'}*{'.json'}"))
    print('Выберите сохранение:')
    for i, file in enumerate(files, 1):
        print(f'{i}. {file.name[9:-5]}')
    print(f'0. Отмена')
    savegame = int(input()) - 1
    if savegame == -1:
        return player
    with open(files[savegame], 'r', encoding='utf-8') as f:
        data = json.load(f)
    load_player = Player(data['name'], [], data['tokens'])
    for row in data['field']:
        row_temp = []
        for square_data in row:
            square = GameSquare(
                square_data['column'],
                square_data['row'],
                square_data['name'],
                square_data['description']
                )
            square.status, square.mark = square_data['status'], square_data['mark']
            row_temp.append(square)
        load_player.field.append(row_temp)
    return load_player

def load_game_from_cloud(player=None):
    data = json.loads(get_load_from_cloud())
    load_player = Player(data['name'], [], data['tokens'])
    for row in data['field']:
        row_temp = []
        for square_data in row:
            square = GameSquare(
                square_data['column'],
                square_data['row'],
                square_data['name'],
                square_data['description']
                )
            square.status, square.mark = square_data['status'], square_data['mark']
            row_temp.append(square)
        load_player.field.append(row_temp)
    return load_player

def check_victory(player):
    for row in range(5):
        if all(player.field[row][col].status == 'cleared' for col in range(5)):
            return True

    for col in range(5):
        if all(player.field[row][col].status == 'cleared' for row in range(5)):
            return True

    if all(player.field[i][i].status == 'cleared' for i in range(5)):
        return True

    if all(player.field[i][4 - i].status == 'cleared' for i in range(5)):
        return True
    return False


def show_menu():
    print('Введите номер команды:')
    print('1. Имя и описание клетки')
    print('2. Открыть клетку')
    print('3. Зачистить клетку')
    print('4. Показать карту')
    print('5. Сохранить')
    print('6. Загрузка')
    print('0. Выход')


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


def show_full_map(player):
    for row in player.field:
        for square in row:
            if isinstance(square, GameSquare):
                print(square.mark.rjust(3), end=' ')
            else:
                print(square.rjust(3), end=' ')
        print()


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


def new_game():
    player = Player(input('Введите свое имя:\n'), [], 3)
    generate_game_field(player.field)
    player.field[2][2].status = 'cleared'
    player.field[2][2].mark = '!!'
    open_squares(player.field[2][2], player)
    main_game(player)


def main_game(player):
    if player is None:
        return None
    show_full_map(player)
    print()
    show_tokens(player)
    show_menu()
    menu(player)


def menu(player):
    while True:
        command = input()
        match command:
            case '1':
                coords = input('Введите координаты клетки:\n')
                x, y = int(coords[0]), int(coords[1])
                if isinstance(player.field[x][y], GameSquare):
                    print(player.field[x][y].data())
                    print(player.field[x][y].status)
                else:
                    print('Заглушка')

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

            case '5':
                save_game(player)

            case '6':
                new_player = load_game(player)
                if new_player is not None:
                    player = new_player

            case '0':
                break

        if check_victory(player):
            print('Ура, победа!')
            break
        print()
        show_tokens(player)
        show_menu()
