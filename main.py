from gui.gui_game import new_game_ui
from utils.game import load_game, show_full_map
from utils.gsheets import get_player_stats, load_game_from_cloud


def main():
    while True:
        print('1. Новая игра')
        print('2. Загрузка')
        print('3. Загрузка из облака')
        print('4. Посмотреть статистику других игроков')
        print('0. Выход')

        command = input()
        match command:
            case '1':
                new_game_ui()

            case '2':
                main_game(load_game())

            case '3':
                main_game(load_game_from_cloud())

            case '4':
                player = get_player_stats()
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


if __name__ == "__main__":
    main()
