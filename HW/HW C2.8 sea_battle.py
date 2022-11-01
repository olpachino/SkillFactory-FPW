# Импорт библиотек
from random import randint


# Класс ошибки выхода за переделы поля
class BoardOutError(Exception):
    def __str__(self):
        return 'Точка выходит за пределы поля'


# Класс ошибки ввод уже используемой координаты
class PointUsedError(Exception):
    def __str__(self):
        return 'Выбранная точка уже открыта'


# Класс точки на доске
class Point:
    """ Point - класс точек на доске
    Аргументы: x - номер строки, y - номер столбца"""

    def __init__(self, x, y):  # инициализация аргументов класса
        self.x = x
        self.y = y

    def __eq__(self, other):  # метод для сравнения точек
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # метод для вывода точки
        return f"Point({self.x}, {self.y})"


# Класс корабля на игровом поле
class Ship:
    """ Ship - класс кораблей на доске
    Аргументы: start - начало корабля,
               length - длина корабля,
               direction - направление корабря (0 - горизонтально, 1 - вертикально),
               lives - жизни корабля
    Методы (свойства): body - тело корабля, то есть список точек из которых состоит корабль"""

    def __init__(self, start, length, direction):  # инициализация аргументов класса
        self.start = start
        self.l = length
        self.d = direction
        self.lives = length

    @property
    def body(self):  # свойство тело корабля
        ship_body = [self.start]  # список точек корабля
        x_next = self.start.x  # фиксируем начальное значение x
        y_next = self.start.y  # фиксируем начальное значение y

        for i in range(1, self.l):  # цикл по длине корабля
            # исходя из ориентации корректируем координаты следующей точки корабля
            if self.d == 0:
                x_next += 1
            elif self.d == 1:
                y_next += 1

            ship_body.append(Point(x_next, y_next))  # добавляем следующую точку корабля

        return ship_body


# Класс доски на игровом поле
class Board:
    """ Board - класс доски на игровом поле
    Аргументы: size - размер поля (по умолчанию 6),
               vis - видимость кораблей на доске (по умолчанию False),
               count - количество подбитых кораблей,
               field - визуальное отображение на доске,
               busy - список занятых точек на доске,
               ships - список кораблей на доске

    Методы: point_out - метод-проверка на выход значения точки за пределы доски,
            point_busy - метод-проверка что точка уже использовалась,
            contour_ship - обводит контуром корабль,
            add_ship - добавление корабля на доску,
            shot - выстрел по кораблю,
            begin - обновление списка занятых точек"""

    def __init__(self, vis=False, size=6):  # инициализируем аргументы класса
        self.size = size
        self.vis = vis

        self.count = 0
        self.field = [["O"] * size for _ in range(size)]  # заполняем доску "O"
        self.busy = []
        self.ships = []

    def __str__(self):  # вывод доски на экран
        res = "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        res += "\n----------------------------"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1}  | " + " | ".join(row) + " |"

        if self.vis:  # если видимость True, показываем корабли на доске
            res = res.replace("■", "O")

        return res

    def point_out(self, point):
        # проверка на выход точки за пределы доски
        if not ((0 <= point.x < self.size) and (0 <= point.y < self.size)):
            raise BoardOutError  # вызываем ошибку, если точка за пределами доски

    def point_busy(self, point):
        # проверка на вхождение в список с занятыми точками
        if point in self.busy:
            raise PointUsedError  # вызываем ошибку, если такая точка уже используется

    def contour_ship(self, ship, vis=False):
        # создаем список сдвигов, для выделения контура фигуры
        area = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)]

        for dot in ship.body:  # идем по точкам корабля
            for arx, ary in area:  # перебираем сдвиги для выделения
                area_point = Point(dot.x + arx, dot.y + ary)
                # конструкция для отлавливания ошибок выхода за пределы доски и занятой точки
                try:
                    self.point_out(area_point)
                    self.point_busy(area_point)
                except BoardOutError:
                    continue
                except PointUsedError:
                    continue
                else:
                    if vis:  # если видимость True оказываем выделение корабля
                        self.field[area_point.x][area_point.y] = '*'

                    self.busy.append(area_point)  # добавляем точки выделения к занятым точкам на доске

    def add_ship(self, ship):
        # идем по точкам корабля
        for dot in ship.body:
            self.point_out(dot)  # проверка на выход за пределы доски
            self.point_busy(dot)  # проверка на занятость точки

            self.field[dot.x][dot.y] = "■"  # отображение корабля на доске
            self.busy.append(dot)  # добавление точки в список занятых

        self.ships.append(ship)  # добавление в список кораблей
        self.contour_ship(ship)  # вызов метода для выделения корабля

    def shot(self, shot):
        self.point_out(shot)  # проверка на выход за пределы доски
        self.point_busy(shot)  # проверка на занятость точки

        self.busy.append(shot)  # добавлем точку в список занятых

        for ship in self.ships:  # идем по караблям в списке кораблей
            if shot in ship.body:  # проверяем попадание выстрела в корабль
                ship.lives -= 1  # уменьшаем жизни корабля
                self.field[shot.x][shot.y] = "X"  # меняем отображение на доске

                if ship.lives == 0:  # проверка на крушение корабля
                    self.count += 1  # добавляем в список уничтоженных кораблей
                    self.contour_ship(ship, vis=True)  # обводим корабль
                    print('Корабль разрушен!')
                else:
                    print('Корабль подбит!')

                return True  # игрок может сделать еще один ход

        self.field[shot.x][shot.y] = "T"  # меняем отображение на доске на промах
        print('Промах!')
        return False  # ход переходит другому игроку

    def begin(self):
        self.busy = []  # обнуляем список занятых точек, для дальнейшей игры


class Player:
    """ Player - класс игроков
        Аргументы: board - доска игрока,
                   enemy - доска противника

        Методы: ask - требует переопределения,
                move - ход игрока"""

    def __init__(self, board, enemy):  # инициализируем аргументы класса
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()  # вызов ошибки, при попытки прямого вызова

    def move(self):
        while True:
            try:
                target = self.ask()  # определение цели
                result = self.enemy.shot(target)  # вывод результата выстрела
                return result
            except BoardOutError as e:
                print(e)
            except PointUsedError as e:
                print(e)


class AI(Player):
    def ask(self):
        shot = Point(randint(0, 5), randint(0, 5))
        print("Выстрел компьютера: ({}, {})".format(shot.x + 1, shot.y + 1))
        return shot


class User(Player):
    def ask(self):
        while True:
            user_input = input('Ваш ход, введите 2 координаты через пробел: ').split()

            if len(user_input) != 2:
                print('Неверное кол-во координат!')
                continue

            try:
                x, y = int(user_input[0]), int(user_input[1])
            except ValueError as e:
                print(f'{e} Необходимо ввести 2 числовые координаты')
                continue
            else:
                return Point(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        ai_board = self.random_board(vis=True)
        user_board = self.random_board()

        self.ai = AI(ai_board, user_board)
        self.user = User(user_board, ai_board)

    def creat_board(self, vis=False):
        ship_len = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size, vis=vis)
        iteration = 0
        for l in ship_len:
            while True:
                iteration += 1
                if iteration > 500:
                    return None
                ship = Ship(Point(randint(0, self.size), randint(0, self.size)),
                            l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardOutError:
                    pass
                except PointUsedError:
                    pass

        board.begin()
        return board

    def random_board(self, vis=False):
        board = None
        while board is None:
            board = self.creat_board(vis=vis)

        return board

    def hello(self):
        print(' ----------------------------')
        print('|       Новая игра           |')
        print('|       Морской бой          |')
        print(' ----------------------------')
        print('|   формат выстрела: x, y    |')
        print('|    x - номер строки        |')
        print('|    y - номер столбца       |')
        print(' ----------------------------')

    def gameplay(self):
        step = 0
        while True:
            print(' ----------------------------')
            print('  Поле пользовател:')
            print(self.user.board)
            print(' ----------------------------')
            print('  Поле компьютера:')
            print(self.ai.board)

            if step % 2 == 0:
                print('Ход игрока:')
                repeat = self.user.move()
            else:
                print('Ход компьютера:')
                repeat = self.ai.move()

            if repeat:
                step -= 1

            if self.ai.board.count == len(self.ai.board.ships):
                print(' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('  ПОЗДРАВЛЯЕМ! ВЫ ПОБЕДИЛИ!  ')
                print(' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                break

            if self.user.board.count == len(self.user.board.ships):
                print(' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('   УВЫ! ПОБЕДИЛ КОМПЬЮТОР    ')
                print(' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                break

            step += 1

    def start(self):
        self.hello()
        self.gameplay()


g = Game()
g.start()
