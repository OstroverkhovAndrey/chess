COMPUTER_TO_HUMAN_TRANSLATOR = [
        {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'},
        {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8'}
]

HUMAN_TO_COMPUTER_TRANSLATOR = [
        {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7},
        {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
]


def coordinates_to_human(to_translate):
    if isinstance(to_translate, str):
        return to_translate

    return (COMPUTER_TO_HUMAN_TRANSLATOR[0][to_translate[0]]
            + COMPUTER_TO_HUMAN_TRANSLATOR[1][to_translate[1]])


def coordinates_to_computer(to_translate):
    if isinstance(to_translate, tuple):
        return to_translate

    return ((HUMAN_TO_COMPUTER_TRANSLATOR[0][to_translate[0]],
             HUMAN_TO_COMPUTER_TRANSLATOR[1][to_translate[1]]))


class Figure():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.possible_moves = []


class King(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 0
        if color == 'w':
            self.label = 'K'
        elif color == 'b':
            self.label = 'k'

    def get_possible_moves(self, board):
        possible_moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if (-1 < self.x + i < 8
                            and -1 < self.y + j < 8
                            and (board[self.x + i][self.y + j] == ' '
                                 or board[self.x + i][self.y + j].isupper()
                                 != self.label.isupper())):
                        possible_moves.append(
                            coordinates_to_human((self.x + i, self.y + j)))

        return possible_moves

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Queen(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 8
        if color == 'w':
            self.label = 'Q'
        elif color == 'b':
            self.label = 'q'

    def possible_moves_horisontal(self, board):
        possible_moves = []

        for i in range(1, 8 - self.x):
            if board[self.x + i][self.y] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y)))
            elif board[self.x + i][self.y].isupper() != self.label.isupper():
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y)))
                break
            else:
                break

        for i in range(1, self.x + 1):
            if board[self.x - i][self.y] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y)))
            elif board[self.x - i][self.y].isupper() != self.label.isupper():
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y)))
                break
            else:
                break

        return possible_moves

    def possible_moves_vertical(self, board):
        possible_moves = []

        for i in range(1, 8 - self.y):
            if board[self.x][self.y + i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x, self.y + i)))
            elif board[self.x][self.y + i].isupper() != self.label.isupper():
                possible_moves.append(
                        coordinates_to_human((self.x, self.y + i)))
                break
            else:
                break

        for i in range(1, self.y + 1):
            if board[self.x][self.y - i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x, self.y - i)))
            elif board[self.x][self.y - i].isupper() != self.label.isupper():
                possible_moves.append(
                        coordinates_to_human((self.x, self.y - i)))
                break
            else:
                break

        return possible_moves

    def possible_moves_1_3(self, board):
        possible_moves = []

        for i in range(1, min(7 - self.x, 7 - self.y) + 1):
            if board[self.x + i][self.y + i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y + i)))
            elif (board[self.x + i][self.y + i].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y + i)))
                break
            else:
                break

        for i in range(1, min(self.x, self.y) + 1):
            if board[self.x - i][self.y - i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y - i)))
            elif (board[self.x - i][self.y - i].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y - i)))
                break
            else:
                break

        return possible_moves

    def possible_moves_2_4(self, board):
        possible_moves = []

        for i in range(1, min(self.x, 7 - self.y) + 1):
            if board[self.x - i][self.y + i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y + i)))
            elif (board[self.x - i][self.y + i].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y + i)))
                break
            else:
                break

        for i in range(1, min(7 - self.x, self.y) + 1):
            if board[self.x + i][self.y - i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y - i)))
            elif (board[self.x + i][self.y - i].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y - i)))
                break
            else:
                break

        return possible_moves

    def get_possible_moves(self, board):
        return (self.possible_moves_horisontal(board)
                + self.possible_moves_vertical(board)
                + self.possible_moves_1_3(board)
                + self.possible_moves_2_4(board))

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Rook(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 5
        if color == 'w':
            self.label = 'R'
        elif color == 'b':
            self.label = 'r'

    def possible_moves_horisontal(self, board):
        possible_moves = []

        for i in range(1, 8 - self.x):
            if board[self.x + i][self.y] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y)))
            elif board[self.x + i][self.y].isupper() != self.label.isupper():
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y)))
                break
            else:
                break

        for i in range(1, self.x + 1):
            if board[self.x - i][self.y] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y)))
            elif board[self.x - i][self.y].isupper() != self.label.isupper():
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y)))
                break
            else:
                break

        return possible_moves

    def possible_moves_vertical(self, board):
        possible_moves = []

        for i in range(1, 8 - self.y):
            if board[self.x][self.y + i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x, self.y + i)))
            elif board[self.x][self.y + i].isupper() != self.label.isupper():
                possible_moves.append(
                        coordinates_to_human((self.x, self.y + i)))
                break
            else:
                break

        for i in range(1, self.y + 1):
            if board[self.x][self.y - i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x, self.y - i)))
            elif board[self.x][self.y - i].isupper() != self.label.isupper():
                possible_moves.append(
                        coordinates_to_human((self.x, self.y - i)))
                break
            else:
                break

        return possible_moves

    def get_possible_moves(self, board):
        return (self.possible_moves_horisontal(board)
                + self.possible_moves_vertical(board))

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Knight(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 3
        if color == 'w':
            self.label = 'KN'
        elif color == 'b':
            self.label = 'kn'

    def get_possible_moves(self, board):
        possible_moves = []

        for i in [-2, 2]:
            for j in [-1, 1]:
                if (-1 < self.x + i < 8
                        and -1 < self.y + j < 8
                        and (board[self.x + i][self.y + j] == ' ' or
                             board[self.x + i][self.y + j].isupper()
                             != self.label.isupper())):
                    possible_moves.append(
                            coordinates_to_human((self.x + i, self.y + j)))
                if (-1 < self.x + j < 8
                        and -1 < self.y + i < 8
                        and (board[self.x + j][self.y + i] == ' '
                             or board[self.x + j][self.y + i].isupper()
                             != self.label.isupper())):
                    possible_moves.append(
                            coordinates_to_human((self.x + j, self.y + i)))

        return possible_moves

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Bishop(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 3
        if color == 'w':
            self.label = 'B'
        elif color == 'b':
            self.label = 'b'

    def possible_moves_1_3(self, board):
        possible_moves = []

        for i in range(1, min(7 - self.x, 7 - self.y) + 1):
            if board[self.x + i][self.y + i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y + i)))
            elif (board[self.x + i][self.y + i].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y + i)))
                break
            else:
                break

        for i in range(1, min(self.x, self.y) + 1):
            if board[self.x - i][self.y - i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y - i)))
            elif (board[self.x - i][self.y - i].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y - i)))
                break
            else:
                break

        return possible_moves

    def possible_moves_2_4(self, board):
        possible_moves = []

        for i in range(1, min(self.x, 7 - self.y) + 1):
            if board[self.x - i][self.y + i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y + i)))
            elif (board[self.x - i][self.y + i].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x - i, self.y + i)))
                break
            else:
                break

        for i in range(1, min(7 - self.x, self.y) + 1):
            if board[self.x + i][self.y - i] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y - i)))
            elif (board[self.x + i][self.y - i].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x + i, self.y - i)))
                break
            else:
                break

        return possible_moves

    def get_possible_moves(self, board):
        return (self.possible_moves_1_3(board)
                + self.possible_moves_2_4(board))

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Pawn(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 1
        if color == 'w':
            self.label = 'P'
        elif color == 'b':
            self.label = 'p'

    def possible_moves_white_pawn(self, board):
        possible_moves = []

        if self.y + 1 < 8:
            if (self.x - 1 > -1
                    and board[self.x - 1][self.y + 1] != ' '
                    and board[self.x - 1][self.y + 1].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x - 1, self.y + 1)))

            if (self.x + 1 < 8
                    and board[self.x + 1][self.y + 1] != ' '
                    and board[self.x + 1][self.y + 1].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x + 1, self.y + 1)))

            if board[self.x][self.y + 1] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x, self.y + 1)))
                if self.y == 1 and board[self.x][self.y + 2] == ' ':
                    possible_moves.append(
                            coordinates_to_human((self.x, self.y + 2)))

        return possible_moves

    def possible_moves_black_pawn(self, board):
        possible_moves = []

        if self.y - 1 > -1:
            if (self.x - 1 > -1
                    and board[self.x - 1][self.y - 1] != ' '
                    and board[self.x - 1][self.y - 1].isupper()
                    != self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x - 1, self.y - 1)))

            if (self.x + 1 < 8
                    and board[self.x + 1][self.y - 1] != ' '
                    and board[self.x + 1][self.y - 1].isupper() !=
                    self.label.isupper()):
                possible_moves.append(
                        coordinates_to_human((self.x + 1, self.y - 1)))

            if board[self.x][self.y - 1] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x, self.y - 1)))
                if self.y == 6 and board[self.x][self.y - 2] == ' ':
                    possible_moves.append(
                            coordinates_to_human((self.x, self.y - 2)))

        return possible_moves

    def get_possible_moves(self, board):
        if self.label.isupper():
            return self.possible_moves_white_pawn(board)
        else:
            return self.possible_moves_black_pawn(board)

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


WHITE_START_FIGURES = ([King(4, 0, 'w'), Queen(3, 0, 'w')]
                       + [Rook(0, 0, 'w'), Rook(7, 0, 'w')]
                       + [Knight(1, 0, 'w'), Knight(6, 0, 'w')]
                       + [Bishop(2, 0, 'w'), Bishop(5, 0, 'w')]
                       + [Pawn(i, 1, 'w') for i in range(8)])
BLACK_START_FIGURES = ([King(4, 7, 'b'), Queen(3, 7, 'b')]
                       + [Rook(0, 7, 'b'), Rook(7, 7, 'b')]
                       + [Knight(1, 7, 'b'), Knight(6, 7, 'b')]
                       + [Bishop(2, 7, 'b'), Bishop(5, 7, 'b')]
                       + [Pawn(i, 6, 'b') for i in range(8)])

EMPTY_BOARD = [[' ' for i in range(8)] for j in range(8)]

BOARD_TEMPLATE = """
   0   1   2   3   4   5   6   7\n
 ┌───┬───┬───┬───┬───┬───┬───┬───┐\n
8│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│7\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
7│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│6\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
6│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│5\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
5│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│4\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
4│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│3\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
3│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│2\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
2│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│1\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
1│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│0\n
 └───┴───┴───┴───┴───┴───┴───┴───┘\n
   a   b   c   d   e   f   g   h\n
"""


class Game():
    def __init__(self):
        self.white_figures = WHITE_START_FIGURES
        self.black_figures = BLACK_START_FIGURES

        self.score = 0

        self.update_board()
        self.update_possible_moves()

        self.moves_history = []

        self.current_player = 'w'

        self.print_board()

    def get_possible_moves(self, side=''):
        possible_moves = {}

        if self.current_player == 'w' or side == 'all':
            for fig in self.white_figures:
                possible_moves[coordinates_to_human((fig.x, fig.y))] = (
                        fig.get_possible_moves(self.board))
        if self.current_player == 'b' or side == 'all':
            for fig in self.black_figures:
                possible_moves[coordinates_to_human((fig.x, fig.y))] = (
                        fig.get_possible_moves(self.board))

        return possible_moves

    def update_possible_moves(self):
        for fig in self.white_figures + self.black_figures:
            fig.update_possible_moves(self.board)

    def update_board(self):
        self.board = [line[:] for line in EMPTY_BOARD]
        for fig in self.white_figures + self.black_figures:
            self.board[fig.x][fig.y] = fig.label

    def print_board(self):
        print(BOARD_TEMPLATE.format(*[self.board[i][j]
              for j in range(7, -1, -1) for i in range(8)]))

    def handle_move(self, x1, y1, x2, y2, moving_figures, fixed_figures):
        score = 0

        for fig in moving_figures:
            if fig.x == x1 and fig.y == y1:
                if (x2, y2) in fig.possible_moves:
                    if self.board[x2][y2] != ' ':
                        for i in range(len(fixed_figures)):
                            if (fixed_figures[i].x == x2
                                    and fixed_figures[i].y == y2):
                                score = fixed_figures[i].value
                                fixed_figures.pop(i)
                                break
                    fig.x = x2
                    fig.y = y2
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = ' '

                    return score

        raise Exception('IMPOSSIBLE MOVE')

    def move(self, coordinate_1, coordinate_2):
        x1, y1 = coordinates_to_computer(coordinate_1)
        x2, y2 = coordinates_to_computer(coordinate_2)

        if self.current_player == 'w':
            self.score += self.handle_move(
                    x1, y1, x2, y2, self.white_figures, self.black_figures)
            self.current_player = 'b'
        else:
            self.score -= self.handle_move(
                    x1, y1, x2, y2, self.black_figures, self.white_figures)
            self.current_player = 'w'

        self.moves_history.append((coordinate_1, coordinate_2))
        self.update_possible_moves()
        self.print_board()
        return
