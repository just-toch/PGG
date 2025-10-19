import gspread
import json

from board import GameSquare
from board import Player


players_cache = {}
worksheet_list_cache = None
print('Начинаю авторизацию')
gc = gspread.service_account(filename='credentials.json')
sh = gc.open("pgg test")
print('Авторизация завершена')

def get_load_from_cloud(name=None):
    if name is None:
        worksheet_list = get_worksheet_list()
        print('Выберите сохранение:')
        for i, worksheet_name in enumerate(worksheet_list[1:], 1):
            print(f'{i}. {worksheet_name.title}')
        print(f'0. Отмена')
        savegame = int(input())
        if savegame == 0:
            return None
        worksheet = sh.worksheet(worksheet_list[savegame].title)
        square = worksheet.cell(1000, 26).value
        return square
    else:
        worksheet = sh.worksheet(name)
        square = worksheet.cell(1000, 26).value
        return square


def load_game_from_cloud(name=None):
    try:
        data = json.loads(get_load_from_cloud(name))
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
    except TypeError:
        return None

def create_player_worksheet(name):
    try:
        sh.worksheet(name.lower())
        return False
    except gspread.WorksheetNotFound:
        sh.add_worksheet(title=name.lower(), rows=1000, cols=26)
        return True

def create_review(player_name, gamename, review):
    worksheet = sh.worksheet(player_name)
    values_list = worksheet.col_values(1)
    empty_cell = len(values_list) + 1
    worksheet.update_cell(empty_cell, 1, gamename) # название игры хранится в 1 столбце
    worksheet.update_cell(empty_cell, 2, review) # обзор игры хранится во 2 столбце

def get_column(worksheet_name, column_number):
    worksheet = sh.worksheet(worksheet_name)
    values_list = worksheet.col_values(column_number)
    return values_list

def save_to_cloud(name, data):
    worksheet = sh.worksheet(name)
    json_data = json.dumps(data, ensure_ascii=False)
    worksheet.update_cell(1000, 26, json_data) # сохранение всегда хранится в ячейке 1000, 26 (она же Z1000)

def get_worksheet_list():
    global worksheet_list_cache
    if worksheet_list_cache is None:
        worksheet_list_cache = sh.worksheets()
    return worksheet_list_cache

def get_player(worksheet):
    global players_cache
    if worksheet.title not in players_cache:
        player = load_game_from_cloud(worksheet.title)
        player.games_list = worksheet.col_values(1)
        player.review_list = worksheet.col_values(2)
        players_cache[worksheet.title] = player
    else:
        player = players_cache.get(worksheet.title)
    return player

def get_player_stats(player_list, player_number):
    worksheet = sh.worksheet(player_list[player_number].title)
    player = get_player(worksheet)
    return player




