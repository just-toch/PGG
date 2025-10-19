import json

from board import GameSquare, Player
from random import randrange

from .gsheets import get_column, save_to_cloud


names = get_column('games', 1)
descriptions = get_column('games', 2)

def generate_game_field(game_field):
    indexes = [i for i in range(len(names))]
    for row in range(5):
        rows = []
        for column in range(5):
            index = randrange(1, len(indexes)-1)
            name, description = indexes[index], indexes[index]
            indexes.pop(index)
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
    data = player.save()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    save_to_cloud(player.name.lower(), data)

def load_game(savegame, files):
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

def new_game(player_name):
    player = Player(player_name, [], 3)
    generate_game_field(player.field)
    player.field[2][2].start_position()
    open_squares(player.field[2][2], player)
    save_game(player)
    return player
