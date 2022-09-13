def hello_game():
    print()
    print("*********************")
    print("      ИГРА ")
    print("  крестики-нолики ")
    print("*********************")
    print(" формат ввода: h1 h2 ")
    print(" через пробел ")
    print(" h1 - номер строки  ")
    print(" h2 - номер столбца ")
    print("*********************")
    print()


def show_field(field):
    print()
    print("    0 1 2 ")
    for i, row in enumerate(field):
        row_str = f"  {i} {' '.join(row)} "
        print(row_str)
    print()


def check_input(field):
    while True:
        cords = input().split(' ')

        if len(cords) != 2:
            print(" Пожалуйста, введите 2 координаты.")
            continue

        try:
            h1, h2 = int(cords[0]), int(cords[1])
        except ValueError:
            print(' Пожалуйста, введите числовые значения.')
            continue

        if any([not 0 <= h1 < 3,
               not 0 <= h2 < 3]):
            print(" Пожалуйста, введите координаты от 0 до 2.")
            continue

        if field[h1][h2] != "-":
            print(" Пожалуйста, введите другие координаты.")
            print(" Эта клетка занята!")
            continue

        return h1, h2


def game_win(field):
    win = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
           ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
           ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0)))

    for line_win in win:
        line = []

        for cords in line_win:
            line.append(field[cords[0]][cords[1]])

        if all([line[0] == line[1] == line[2],
                line[0] != "-"]):
            print()
            print(f" Выиграл {line[0]}!")
            show_field(field)
            return True
    return False


hello_game()
field = [["-"] * 3 for i in range(3)]
count = 0
win = False

while not win:
    count += 1
    show_field(field)

    if count % 2 == 1:
        print(" Ход крестика: ")
    else:
        print(" Ход нолика: ")

    h1, h2 = check_input(field)

    if count % 2 == 1:
        field[h1][h2] = "X"
    else:
        field[h1][h2] = "0"

    win = game_win(field)

    if count == 9:
        print(" Победила дружба!")
        break