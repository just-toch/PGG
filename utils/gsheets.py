from queue import Queue
from threading import Thread
from time import sleep

import gspread
import json

from board import GameSquare
from board import Player

class GoogleSheets:
    def __init__(self):
        self.players_cache = {}
        self.worksheet_list_cache = None
        self.gc = None
        self.sh = None
        print('Начинаю авторизацию')
        self.connect_to_google()

    def connect_to_google(self):
        def connect_thread(q: Queue):
            gc_inner = gspread.service_account(filename='credentials.json')
            sh_inner = gc_inner.open("pgg test")
            # q.put((gc_inner, sh_inner))
            # sleep(5)
            self.gc = gc_inner
            self.sh = sh_inner
            print('Авторизация завершена')
        q = Queue()
        thread_connect = Thread(target=connect_thread, daemon=True, args=(q,))
        thread_connect.start()
        # return q.get()

    def get_load_from_cloud(self, name=None):
        if name is None:
            worksheet_list = self.get_worksheet_list()
            print('Выберите сохранение:')
            for i, worksheet_name in enumerate(worksheet_list[1:], 1):
                print(f'{i}. {worksheet_name.title}')
            print(f'0. Отмена')
            savegame = int(input())
            if savegame == 0:
                return None
            worksheet = self.sh.worksheet(worksheet_list[savegame].title)
            square = worksheet.cell(1000, 26).value
            return square
        else:
            worksheet = self.sh.worksheet(name)
            square = worksheet.cell(1000, 26).value
            return square


    def load_game_from_cloud(self, name=None):
        try:
            data = json.loads(self.get_load_from_cloud(name))
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

    def create_player_worksheet(self, name):
        try:
            self.sh.worksheet(name.lower())
            return False
        except gspread.WorksheetNotFound:
            self.sh.add_worksheet(title=name.lower(), rows=1000, cols=26)
            return True

    def create_review(self, player_name, gamename, review):
        worksheet = self.sh.worksheet(player_name)
        values_list = worksheet.col_values(1)
        empty_cell = len(values_list) + 1
        worksheet.update_cell(empty_cell, 1, gamename) # название игры хранится в 1 столбце
        worksheet.update_cell(empty_cell, 2, review) # обзор игры хранится во 2 столбце

    def get_column(self, worksheet_name, column_number):
        worksheet = self.sh.worksheet(worksheet_name)
        values_list = worksheet.col_values(column_number)
        return values_list

    def save_to_cloud(self, name, data):
        worksheet = self.sh.worksheet(name)
        json_data = json.dumps(data, ensure_ascii=False)
        worksheet.update_cell(1000, 26, json_data) # сохранение всегда хранится в ячейке 1000, 26 (она же Z1000)

    def get_worksheet_list(self):
        global worksheet_list_cache
        if worksheet_list_cache is None:
            worksheet_list_cache = self.sh.worksheets()
        return worksheet_list_cache

    def get_player(self, worksheet):
        global players_cache
        if worksheet.title not in players_cache:
            player = self.load_game_from_cloud(worksheet.title)
            player.games_list = worksheet.col_values(1)
            player.review_list = worksheet.col_values(2)
            players_cache[worksheet.title] = player
        else:
            player = players_cache.get(worksheet.title)
        return player

    def get_player_stats(self, player_list, player_number):
        worksheet = self.sh.worksheet(player_list[player_number].title)
        player = self.get_player(worksheet)
        return player
