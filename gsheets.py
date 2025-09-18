import gspread


gc = gspread.service_account(filename='credentials.json')
sh = gc.open("pgg test")

def get_load_from_cloud():
    worksheet = sh.worksheet('saves')
    saves = worksheet.col_values(1)
    print('Выберите сохранение:')
    for i, name in enumerate(saves, 1):
        print(f'{i}. {name}')
    print(f'0. Отмена')
    savegame = int(input())
    cell = worksheet.cell(savegame, 2).value
    return cell

# print('Введите имя')
# s = input().lower()
# try:
#     worksheet = sh.worksheet(s)
#     print(f'Лист {s} найден')
# except gspread.WorksheetNotFound:
#     worksheet = sh.add_worksheet(title=s, rows=100, cols=20)
#     print(f'Лист {s} создан')

# path = Path()
# files = list(path.glob(f"{'savegame'}*{'.json'}"))
# print(files)
# with open(files[1], 'r', encoding='utf-8') as f:
#     data = json.load(f)
# print(data)
# print(type(data))
#
# worksheet = sh.worksheet('saves')
# cell = worksheet.acell('B1').value
# print(cell)
# print(type(cell))

