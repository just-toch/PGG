# сгенерированно Дипсиком на основе остального кода

import tkinter as tk
from tkinter import messagebox, simpledialog
from board.game_square import GameSquare
from board.player import Player
from random import randrange
from pathlib import Path
import json

# Ваши данные
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


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.player = None
        self.selected_cell = None
        self.setup_ui()
        self.show_main_menu()

    def setup_ui(self):
        """Настройка интерфейса"""
        self.root.configure(bg='lightgray')

        # Основные фреймы
        self.main_frame = tk.Frame(self.root, bg='lightgray')
        self.game_frame = tk.Frame(self.root, bg='lightgray')

        # Создаем сетку клеток
        self.cell_buttons = [[None for _ in range(5)] for _ in range(5)]
        for row in range(5):
            for col in range(5):
                btn = tk.Button(self.game_frame, text='', width=8, height=4,
                                command=lambda r=row, c=col: self.select_cell(r, c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.cell_buttons[row][col] = btn

        # Панель информации
        self.info_frame = tk.Frame(self.root, bg='lightgray')
        self.info_label = tk.Label(self.info_frame, text="", font=("Arial", 12), bg='lightgray')
        self.info_label.pack(pady=10)

        # Кнопки действий
        self.action_frame = tk.Frame(self.root, bg='lightgray')
        self.create_action_buttons()

    def create_action_buttons(self):
        """Создание кнопок действий"""
        actions = [
            ("ℹ️ Информация о клетке", self.show_cell_info),
            ("🔓 Открыть клетку", self.open_cell),
            ("✅ Зачистить клетку", self.clear_cell),
            ("🗺️ Показать карту", self.show_full_map),
            ("💾 Сохранить игру", self.save_game),
            ("📂 Загрузить игру", self.load_game),
            ("🏠 Главное меню", self.show_main_menu)
        ]

        for text, command in actions:
            btn = tk.Button(self.action_frame, text=text, command=command, width=20)
            btn.pack(pady=2)

    def show_main_menu(self):
        """Показать главное меню"""
        self.hide_all_frames()
        self.main_frame.pack(expand=True)

        tk.Label(self.main_frame, text="🎮 ИГРА", font=("Arial", 24), bg='lightgray').pack(pady=20)

        tk.Button(self.main_frame, text="🎮 Новая игра", command=self.new_game,
                  width=20, height=2, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.main_frame, text="📂 Загрузить игру", command=self.load_game_menu,
                  width=20, height=2, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.main_frame, text="🚪 Выход", command=self.root.quit,
                  width=20, height=2, font=("Arial", 14)).pack(pady=10)

    def new_game(self):
        """Начать новую игру"""
        name = simpledialog.askstring("Имя игрока", "Введите ваше имя:", parent=self.root)
        if not name:
            return

        self.player = Player(name, [], 3)
        self.generate_game_field(self.player.field)
        self.player.field[2][2].status = 'cleared'
        self.player.field[2][2].mark = '!!'
        self.open_squares(self.player.field[2][2], self.player)

        self.start_game()

    def start_game(self):
        """Начать игровой процесс"""
        self.hide_all_frames()
        self.game_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)
        self.action_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        self.update_display()

    def update_display(self):
        """Обновить отображение игры"""
        if not self.player:
            return

        # Обновляем информацию
        tokens_text = f"Игрок: {self.player.name} | Токены: {self.player.tokens}"
        self.info_label.config(text=tokens_text)

        # Обновляем клетки
        for row in range(5):
            for col in range(5):
                cell = self.player.field[row][col]
                btn = self.cell_buttons[row][col]

                # Цвет в зависимости от статуса
                if cell.status == 'cleared':
                    btn.config(bg='green', text=cell.mark)
                elif cell.status == 'opened':
                    btn.config(bg='lightblue', text=cell.mark)
                elif cell.status == 'available':
                    btn.config(bg='yellow', text=f"{row},{col}")
                else:
                    btn.config(bg='gray', text=f"{row},{col}")

                # Выделение выбранной клетки
                if self.selected_cell == (row, col):
                    btn.config(relief=tk.SUNKEN)
                else:
                    btn.config(relief=tk.RAISED)

    def select_cell(self, row, col):
        """Выбрать клетку"""
        self.selected_cell = (row, col)
        self.update_display()

    def show_cell_info(self):
        """Показать информацию о клетке"""
        if not self.selected_cell:
            messagebox.showinfo("Информация", "Сначала выберите клетку!")
            return

        row, col = self.selected_cell
        cell = self.player.field[row][col]

        info = f"Координаты: {row},{col}\n"
        info += f"Название: {cell.name}\n"
        info += f"Описание: {cell.description}\n"
        info += f"Статус: {cell.status}\n"
        info += f"Маркер: {cell.mark}"

        messagebox.showinfo("Информация о клетке", info)

    def open_cell(self):
        """Открыть клетку"""
        if not self.selected_cell:
            messagebox.showinfo("Ошибка", "Сначала выберите клетку!")
            return

        if self.player.tokens <= 0:
            messagebox.showinfo("Ошибка", "Недостаточно токенов!")
            return

        row, col = self.selected_cell
        cell = self.player.field[row][col]

        if cell.status == 'available':
            cell.change_to_opened()
            self.open_squares(cell, self.player)
            self.player.tokens -= 1
            self.update_display()
            messagebox.showinfo("Успех", f"Клетка {row},{col} открыта!")

            if self.check_victory():
                messagebox.showinfo("ПОБЕДА!", "🎉 Вы выиграли! Собрана линия из 5 клеток!")
        else:
            messagebox.showinfo("Ошибка", "Нельзя открыть эту клетку!")

    def clear_cell(self):
        """Зачистить клетку"""
        if not self.selected_cell:
            messagebox.showinfo("Ошибка", "Сначала выберите клетку!")
            return

        row, col = self.selected_cell
        cell = self.player.field[row][col]

        if cell.status == 'opened':
            cell.change_to_cleared()
            self.player.tokens += 3
            self.update_display()
            messagebox.showinfo("Успех", "Клетка зачищена! +3 токена")

            if self.check_victory():
                messagebox.showinfo("ПОБЕДА!", "🎉 Вы выиграли! Собрана линия из 5 клеток!")
        else:
            messagebox.showinfo("Ошибка", "Нельзя зачистить эту клетку!")

    def show_full_map(self):
        """Показать полную карту"""
        map_text = "Полная карта:\n\n"
        for row in range(5):
            for col in range(5):
                cell = self.player.field[row][col]
                map_text += f"[{row},{col}]: {cell.mark} ({cell.status})\n"
            map_text += "\n"

        messagebox.showinfo("Полная карта", map_text)

    def save_game(self):
        """Сохранить игру"""
        if not self.player:
            messagebox.showinfo("Ошибка", "Нет активной игры для сохранения!")
            return

        filename = f'savegame_{self.player.name.lower()}.json'
        data = self.player.save()

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        messagebox.showinfo("Сохранение", f"Игра сохранена в файл: {filename}")

    def load_game_menu(self):
        """Меню загрузки игры"""
        path = Path()
        files = list(path.glob("savegame_*.json"))

        if not files:
            messagebox.showinfo("Загрузка", "Нет сохраненных игр!")
            return

        # Создаем диалог выбора
        dialog = tk.Toplevel(self.root)
        dialog.title("Выберите сохранение")
        dialog.geometry("300x400")

        tk.Label(dialog, text="Выберите сохранение:", font=("Arial", 12)).pack(pady=10)

        listbox = tk.Listbox(dialog, width=40, height=15)
        for file in files:
            listbox.insert(tk.END, file.name[9:-5])  # Убираем 'savegame_' и '.json'
        listbox.pack(pady=10)

        def load_selected():
            selection = listbox.curselection()
            if selection:
                filename = files[selection[0]]
                self.load_game(filename)
                dialog.destroy()

        tk.Button(dialog, text="Загрузить", command=load_selected).pack(pady=5)
        tk.Button(dialog, text="Отмена", command=dialog.destroy).pack(pady=5)

    def load_game(self, filename):
        """Загрузить игру"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.player = Player(data['name'], [], data['tokens'])

            for row_data in data['field']:
                row_temp = []
                for square_data in row_data:
                    square = GameSquare(
                        square_data['column'],
                        square_data['row'],
                        square_data['name'],
                        square_data['description']
                    )
                    square.status = square_data['status']
                    square.mark = square_data['mark']
                    row_temp.append(square)
                self.player.field.append(row_temp)

            self.start_game()
            messagebox.showinfo("Загрузка", f"Игра {data['name']} загружена!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {e}")

    def hide_all_frames(self):
        """Скрыть все фреймы"""
        for frame in [self.main_frame, self.game_frame, self.info_frame, self.action_frame]:
            frame.pack_forget()

    # Ваши игровые функции
    def generate_game_field(self, game_field):
        for row in range(5):
            rows = []
            for column in range(5):
                index = randrange(len(names))
                name, description = names.pop(index), descriptions.pop(index)
                rows.append(GameSquare(column, row, name, description))
            game_field.append(rows)
        return game_field

    def open_squares(self, square, player):
        coordinates = square.coordinates()
        for i in range(max(0, int(coordinates[0]) - 1), min(5, int(coordinates[0]) + 2)):
            for j in range(max(0, int(coordinates[1]) - 1), min(5, int(coordinates[1]) + 2)):
                player.field[i][j].change_to_available()

    def check_victory(self):
        if not self.player:
            return False

        for row in range(5):
            if all(self.player.field[row][col].status == 'cleared' for col in range(5)):
                return True

        for col in range(5):
            if all(self.player.field[row][col].status == 'cleared' for row in range(5)):
                return True

        if all(self.player.field[i][i].status == 'cleared' for i in range(5)):
            return True

        if all(self.player.field[i][4 - i].status == 'cleared' for i in range(5)):
            return True

        return False

"""Запуск графической версии игры"""
root = tk.Tk()
root.title("Игровое поле")
root.geometry("800x600")

app = GameGUI(root)
root.mainloop()
