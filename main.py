from game import new_game, load_game, main_game, load_game_from_cloud


def main():

    while True:
        print('1. Новая игра')
        print('2. Загрузка')
        print('3. Загрузка из облака')
        print('0. Выход')

        command = input()
        match command:
            case '1':
                new_game()

            case '2':
                main_game(load_game())

            case '3':
                main_game(load_game_from_cloud())

            case '0':
                break


if __name__ == "__main__":
    main()
