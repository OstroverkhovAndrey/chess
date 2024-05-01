import copy

COMPUTER_TO_HUMAN_TRANSLATOR = [
        {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'},
        {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8'}
]

HUMAN_TO_COMPUTER_TRANSLATOR = [
        {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7},
        {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
]


def coordinates_to_human(to_translate):
    """
    Return human-like coordinates of chess figure.

    Argument:
    to_translate -- tuple of machine-like figure coordinates

    """
    if isinstance(to_translate, str):
        return to_translate

    return (COMPUTER_TO_HUMAN_TRANSLATOR[0][to_translate[0]]
            + COMPUTER_TO_HUMAN_TRANSLATOR[1][to_translate[1]])


def coordinates_to_computer(to_translate):
    """
    Return machine-like coordinates of chess figure.

    Argument:
    to_translate -- string human-like figure coordinates

    """
    if isinstance(to_translate, tuple):
        return to_translate

    return ((HUMAN_TO_COMPUTER_TRANSLATOR[0][to_translate[0]],
             HUMAN_TO_COMPUTER_TRANSLATOR[1][to_translate[1]]))


class Figure():
    """
    A class used to present any chess figure.

    Attributes
    ----------
    x : int
        first coordinate of figure (0 to 7)
    y : int
        second coordinate of figure (0 to 7)
    color : str
        present side which figure is on ('w' -white or 'b' - black)
    possible_moves : list
        list of figure possible moves

    """

    def __init__(self, x, y, color):
        """
        Parameters
        ----------
        x : int
            first coordinate of figure (0 to 7)
        y : int
            second coordinate of figure (0 to 7)
        color : str
            present side which figure is on ('w' -white or 'b' - black)
        possible_moves : list
            list of figure possible moves
        """
        self.x = x
        self.y = y
        self.color = color
        self.possible_moves = []


class King(Figure):
    """
    A class used to present King chess figure.

    Attributes
    ----------
    x : int
        first coordinate of figure (0 to 7)
    y : int
        second coordinate of figure (0 to 7)
    color : str
        present side which figure is on ('w' -white or 'b' - black)
    possible_moves : list
        list of figure possible moves
    value : int
        value of a figure (default 0)
    has_moved : bool
        indicator of moving since begginning of the game (used for roque)
    is_under_attack : bool
        indicator of attack on King (chech)

    Methods
    -------
    get_possible_roques(board)
        return list of human-like possible positions to move on the board
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on get_possible_roques and
        get_possible_moves returning lists

    """

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 0
        if color == 'w':
            self.label = 'Kw'
        elif color == 'b':
            self.label = 'Kb'
        self.has_moved = False
        self.is_under_attack = False

    def get_possible_roques(self, board):
        possible_moves = []

        if not self.has_moved:
            for dx in [-3, -2, -1]:
                x = self.x + dx
                y = self.y
                if board[x][y] != ' ':
                    break
            else:
                if self.label == 'K' and board[0][0] == 'R':
                    possible_moves.append(coordinates_to_human((2, 0)))
                elif self.label == 'k' and board[0][7] == 'r':
                    possible_moves.append(coordinates_to_human((2, 7)))

            for dx in [1, 2]:
                x = self.x + dx
                y = self.y
                if board[x][y] != ' ':
                    break
            else:
                if self.label == 'K' and board[7][0] == 'R':
                    possible_moves.append(coordinates_to_human((6, 0)))
                elif self.label == 'k' and board[7][7] == 'r':
                    possible_moves.append(coordinates_to_human((6, 7)))

        return possible_moves

    def get_possible_moves(self, board):
        if (self.x != 4 or self.label == 'K' and self.y != 0
                or self.label == 'k' and self.y != 7):
            self.has_moved = True

        possible_moves = []

        for dx, dy in ([0, 1], [1, 1], [1, 0], [1, -1],
                       [0, -1], [-1, -1], [-1, 0], [-1, 1]):
            x = self.x + dx
            y = self.y + dy
            if (-1 < x < 8 and -1 < y < 8 and (board[x][y] == ' '
               or board[x][y].isupper() != self.label.isupper())):
                possible_moves.append(coordinates_to_human((x, y)))

        possible_moves += self.get_possible_roques(board)

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Queen(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 8
        if color == 'w':
            self.label = 'Qw'
        elif color == 'b':
            self.label = 'Qb'

    def get_possible_moves(self, board):
        possible_moves = []

        for dx, dy in ([1, 0], [0, -1], [-1, 0], [0, 1],
                       [1, 1], [1, -1], [-1, -1], [-1, 1]):
            for length in range(1, 7):
                x = self.x + dx * length
                y = self.y + dy * length
                if not -1 < x < 8 or not -1 < y < 8:
                    break
                elif board[x][y] == ' ':
                    possible_moves.append(
                            coordinates_to_human((x, y)))
                elif board[x][y].isupper() != self.label.isupper():
                    possible_moves.append(coordinates_to_human((x, y)))
                    break
                else:
                    break

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Rook(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 5
        if color == 'w':
            self.label = 'Rw'
        elif color == 'b':
            self.label = 'Rb'
        self.has_moved = False

    def get_possible_moves(self, board):
        possible_moves = []

        for dx, dy in [1, 0], [0, -1], [-1, 0], [0, 1]:
            for length in range(1, 7):
                x = self.x + dx * length
                y = self.y + dy * length
                if not -1 < x < 8 or not -1 < y < 8:
                    break
                elif board[x][y] == ' ':
                    possible_moves.append(coordinates_to_human((x, y)))
                elif board[x][y].isupper() != self.label.isupper():
                    possible_moves.append(coordinates_to_human((x, y)))
                    break
                else:
                    break

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Knight(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 3
        if color == 'w':
            self.label = 'KNw'
        elif color == 'b':
            self.label = 'KNb'

    def get_possible_moves(self, board):
        possible_moves = []

        for dx, dy in ([2, 1], [2, -1], [-2, -1], [-2, 1],
                       [1, 2], [1, -2], [-1, -2], [-1, 2]):
            x = self.x + dx
            y = self.y + dy
            if (-1 < x < 8 and -1 < y < 8
                    and (board[x][y] == ' ' or board[x][y].isupper()
                         != self.label.isupper())):
                possible_moves.append(coordinates_to_human((x, y)))

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Bishop(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 3
        if color == 'w':
            self.label = 'Bw'
        elif color == 'b':
            self.label = 'Bb'

    def get_possible_moves(self, board):
        possible_moves = []

        for dx, dy in [1, 1], [1, -1], [-1, -1], [-1, 1]:
            for length in range(1, 7):
                x = self.x + dx * length
                y = self.y + dy * length
                if not -1 < x < 8 or not -1 < y < 8:
                    break
                elif board[x][y] == ' ':
                    possible_moves.append(coordinates_to_human((x, y)))
                elif board[x][y].isupper() != self.label.isupper():
                    possible_moves.append(coordinates_to_human((x, y)))
                    break
                else:
                    break

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Pawn(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 1
        if color == 'w':
            self.label = 'Pw'
        elif color == 'b':
            self.label = 'Pb'
        self.has_moved_two = False

    def possible_moves_white_pawn(self, board):
        possible_moves = []

        if self.y + 1 < 8:
            if (self.x - 1 > -1
                    and board[self.x - 1][self.y + 1] != ' '
                    and board[self.x - 1][self.y + 1][-1]
                    != self.label[-1]):
                possible_moves.append(
                        coordinates_to_human((self.x - 1, self.y + 1)))

            if (self.x + 1 < 8
                    and board[self.x + 1][self.y + 1] != ' '
                    and board[self.x + 1][self.y + 1][-1]
                    != self.label[-1]):
                possible_moves.append(
                        coordinates_to_human((self.x + 1, self.y + 1)))

            if board[self.x][self.y + 1] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x, self.y + 1)))
                if self.y == 1 and board[self.x][self.y + 2] == ' ':
                    possible_moves.append(
                            coordinates_to_human((self.x, self.y + 2)))

            if self.y == 4:
                if self.x - 1 > 0 and board[self.x - 1][self.y] == 'Pb':
                    possible_moves.append(
                        coordinates_to_human((self.x - 1, self.y + 1)))
                if self.x + 1 < 8 and board[self.x + 1][self.y] == 'Pb':
                    possible_moves.append(
                        coordinates_to_human((self.x + 1, self.y + 1)))

        return sorted(possible_moves)

    def possible_moves_black_pawn(self, board):
        possible_moves = []

        if self.y - 1 > -1:
            if (self.x - 1 > -1
                    and board[self.x - 1][self.y - 1] != ' '
                    and board[self.x - 1][self.y - 1][-1]
                    != self.label[-1]):
                possible_moves.append(
                        coordinates_to_human((self.x - 1, self.y - 1)))

            if (self.x + 1 < 8
                    and board[self.x + 1][self.y - 1] != ' '
                    and board[self.x + 1][self.y - 1][-1] !=
                    self.label[-1]):
                possible_moves.append(
                        coordinates_to_human((self.x + 1, self.y - 1)))

            if board[self.x][self.y - 1] == ' ':
                possible_moves.append(
                        coordinates_to_human((self.x, self.y - 1)))
                if self.y == 6 and board[self.x][self.y - 2] == ' ':
                    possible_moves.append(
                            coordinates_to_human((self.x, self.y - 2)))

            if self.y == 3:
                if self.x - 1 > 0 and board[self.x - 1][self.y] == 'Pw':
                    possible_moves.append(
                        coordinates_to_human((self.x - 1, self.y - 1)))
                if self.x + 1 < 8 and board[self.x + 1][self.y] == 'Pw':
                    possible_moves.append(
                        coordinates_to_human((self.x + 1, self.y - 1)))

        return sorted(possible_moves)

    def get_possible_moves(self, board):
        if self.label[-1] == 'w':
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

BOARD_TEMPLATE_WHITE = """
   a    b    c    d    e    f    g    h
 ┌────┬────┬────┬────┬────┬────┬────┬────┐
8│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │8
 ├────┼────┼────┼────┼────┼────┼────┼────┤
7│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │7
 ├────┼────┼────┼────┼────┼────┼────┼────┤
6│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │6
 ├────┼────┼────┼────┼────┼────┼────┼────┤
5│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │5
 ├────┼────┼────┼────┼────┼────┼────┼────┤
4│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │4
 ├────┼────┼────┼────┼────┼────┼────┼────┤
3│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │3
 ├────┼────┼────┼────┼────┼────┼────┼────┤
2│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │2
 ├────┼────┼────┼────┼────┼────┼────┼────┤
1│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │1
 └────┴────┴────┴────┴────┴────┴────┴────┘
   a    b    c    d    e    f    g    h
"""
BOARD_TEMPLATE_BLACK = """
   h    g    f    e    d    c    b    a
 ┌────┬────┬────┬────┬────┬────┬────┬────┐
8│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │8
 ├────┼────┼────┼────┼────┼────┼────┼────┤
7│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │7
 ├────┼────┼────┼────┼────┼────┼────┼────┤
6│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │6
 ├────┼────┼────┼────┼────┼────┼────┼────┤
5│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │5
 ├────┼────┼────┼────┼────┼────┼────┼────┤
4│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │4
 ├────┼────┼────┼────┼────┼────┼────┼────┤
3│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │3
 ├────┼────┼────┼────┼────┼────┼────┼────┤
2│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │2
 ├────┼────┼────┼────┼────┼────┼────┼────┤
1│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │1
 └────┴────┴────┴────┴────┴────┴────┴────┘
   h    g    f    e    d    c    b    a
"""


class Game():
    def __init__(self, player):
        self.white_figures = [copy.deepcopy(WHITE_START_FIGURES[i])
                              for i in range(len(WHITE_START_FIGURES))]
        self.black_figures = [copy.deepcopy(BLACK_START_FIGURES[i])
                              for i in range(len(BLACK_START_FIGURES))]

        self.score = 0

        self.update_board()
        self.update_possible_moves()

        self.moves_history = []

        self.current_player = 'w'
        self.player = player

    def get_possible_moves(self):
        possible_moves = {}

        if self.current_player == 'w' and self.player == 'w':
            for fig in self.white_figures:
                possible_moves[coordinates_to_human((fig.x, fig.y))] = (
                        fig.get_possible_moves(self.board))
            return dict(sorted(possible_moves.items()))
        elif self.current_player == 'b' and self.player == 'b':
            for fig in self.white_figures:
                possible_moves[coordinates_to_human((fig.x, fig.y))] = (
                        fig.get_possible_moves(self.board))
            return dict(sorted(possible_moves.items()))
        else:
            return []

    def update_possible_moves(self):
        for fig in self.white_figures + self.black_figures:
            fig.update_possible_moves(self.board)

    def update_board(self):
        self.board = [line[:] for line in EMPTY_BOARD]
        for fig in self.white_figures + self.black_figures:
            self.board[fig.x][fig.y] = fig.label

    def get_board(self):
        self.update_board()
        if self.player == 'w':
            return BOARD_TEMPLATE_WHITE.format(*[self.board[i][j]
                                               for j in range(7, -1, -1)
                                               for i in range(8)])
        else:
            return BOARD_TEMPLATE_BLACK.format(*[self.board[7 - i][7 - j]
                                               for j in range(7, -1, -1)
                                               for i in range(8)])

    def print_board(self):
        self.update_board()
        if self.player == 'w':
            print(BOARD_TEMPLATE_WHITE.format(*[self.board[i][j]
                  for j in range(7, -1, -1) for i in range(8)]))
        else:
            print(BOARD_TEMPLATE_BLACK.format(*[self.board[7 - i][7 - j]
                  for j in range(7, -1, -1) for i in range(8)]))

    def cancel_move(self, x1, y1, x2, y2,
                    moving_figures, fixed_figures, eaten_figure):
        for fig in moving_figures:
            if fig.x == x2 and fig.y == y2:
                fig.x = x1
                fig.y = y1
        if eaten_figure is not None:
            fixed_figures.append(eaten_figure)

    def is_check_move(self, x1, x2, y1, y2,
                      moving_figures, fixed_figures, eaten_figure):
        self.update_possible_moves()
        king_x = moving_figures[0].x
        king_y = moving_figures[0].y
        for fig in fixed_figures:
            for (x, y) in fig.possible_moves:
                if x == king_x and y == king_y:
                    self.cancel_move(x1, y1, x2, y2,
                                     moving_figures, fixed_figures,
                                     eaten_figure)
                    self.update_possible_moves()
                    return "IMPOSSIBLE MOVE: YOU CAN'T MAKE MOVE TO CHECK"
        moving_figures[0].is_under_attack = False

        self.update_possible_moves()
        king_x = fixed_figures[0].x
        king_y = fixed_figures[0].y
        for fig in moving_figures:
            for (x, y) in fig.possible_moves:
                if x == king_x and y == king_y:
                    fixed_figures[0].is_under_attack = True
                    if self.is_checkmate():
                        return 'CHECKMATE!'
                    else:
                        return 'CHECK!'

    def is_checkmate(self):
        if self.current_player == 'w':
            moving_figures = self.black_figures
            fixed_figures = self.white_figures
        else:
            moving_figures = self.white_figures
            fixed_figures = self.black_figures

        king_position = (coordinates_to_human((moving_figures[0].x,
                                              moving_figures[0].y)))

        for moved_figure in moving_figures[1:]:
            for (x, y) in moved_figure.possible_moves:
                board = [line[:] for line in self.board]
                board[moved_figure.x][moved_figure.y] = ' '
                board[x][y] = moved_figure.label
                under_attack = False
                for fixed_figure in fixed_figures:
                    if (king_position in
                            fixed_figure.get_possible_moves(board)):
                        under_attack = True
                if not under_attack:
                    return False

        return True

    def handle_roque(self, x1, y1, x2, y2, moving_figures):
        if ((self.current_player == 'w' and self.board[x1][y1] == 'Kw'
                or self.current_player == 'b' and self.board[x1][y1] == 'Kb')
                and abs(x2 - x1) == 2):
            for fig in moving_figures:
                if fig.x == x1 and fig.y == y1:
                    fig.x = x2
                    fig.y = x2
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = ' '
                elif fig.y == y1 and x2 > x1 and fig.x == 7:
                    fig.x = x2
                    fig.y = 5
                    self.board[5][y2] = self.board[7][y1]
                    self.board[7][y1] = ' '
                elif fig.y == y1 and x2 < x1 and fig.x == 0:
                    fig.x = x2
                    fig.y = 3
                    self.board[3][y2] = self.board[0][y1]
                    self.board[0][y1] = ' '
            return True
        else:
            return False

    def handle_en_passant(self, x1, y1, x2, y2, moving_figures, fixed_figures):
        if ((self.current_player == 'w'
                and self.board[x1][y1] == 'Pw' and y1 == 4
                or self.current_player == 'b'
                and self.board[x1][y1] == 'Pb' and y1 == 3)
                and abs(x2 - x1) == 1 and abs(y2 - y1) == 1):
            for moving_fig in moving_figures:
                for i in range(len(fixed_figures)):
                    fixed_fig = fixed_figures[i]
                    if (moving_fig.x == x1 and moving_fig.y == y1
                            and fixed_fig.x == x2
                            and (y1 == 4 and fixed_fig.y == y2 - 1 or
                                 y1 == 3 and fixed_fig.y == y2 + 1)):
                        self.board[fixed_fig.x][fixed_fig.y] = ' '
                        fixed_figures.pop(i)
                        self.board[x1][y1] = ' '
                        self.board[x2][y2] = moving_fig.label
                        moving_fig.x = x2
                        moving_fig.y = y2
                        if y1 == 4:
                            return 1
                        else:
                            return -1
        else:
            return 0

    def handle_en_passant_roque(self, x1, y1, x2, y2,
                                moving_figures, fixed_figures):
        if self.handle_roque(x1, y1, x2, y2, moving_figures):
            return 0
        if (t := self.handle_en_passant(x1, y1, x2, y2,
                                        moving_figures, fixed_figures) != 0):
            self.score += t
            return 0
        else:
            return -1

    def handle_move(self, x1, y1, x2, y2, moving_figures, fixed_figures):
        if self.handle_en_passant_roque(x1, y1, x2, y2,
                                        moving_figures, fixed_figures) == 0:
            return 0

        score = 0
        eaten_figure = None
        for fig in moving_figures:
            if fig.x == x1 and fig.y == y1:
                if (x2, y2) in fig.possible_moves:
                    if self.board[x2][y2] != ' ':
                        for i in range(len(fixed_figures)):
                            if (fixed_figures[i].x == x2
                                    and fixed_figures[i].y == y2):
                                score = fixed_figures[i].value
                                eaten_figure = fixed_figures[i]
                                fixed_figures.pop(i)
                                break
                    fig.x = x2
                    fig.y = y2
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = ' '
                    if isinstance(fig, Pawn) and (abs(y2 - y1) == 2):
                        fig.has_moved_two = True

                    break
        else:
            return 'IMPOSSIBLE MOVE'

        ans = self.is_check_move(x1, y1, x2, y2,
                                 moving_figures, fixed_figures, eaten_figure)
        if ans is not None:
            return ans
        else:
            return score

    def move(self, coordinate_1, coordinate_2, forced=False):
        x1, y1 = coordinates_to_computer(coordinate_1)
        x2, y2 = coordinates_to_computer(coordinate_2)

        if self.current_player == 'w' and (self.player == 'w' or forced):
            ans = self.handle_move(
                    x1, y1, x2, y2, self.white_figures, self.black_figures)
            if isinstance(ans, int):
                self.score += ans
            else:
                return ans
            self.current_player = 'b'
        elif self.current_player == 'b' and (self.player == 'b' or forced):
            ans = self.handle_move(
                    x1, y1, x2, y2, self.black_figures, self.white_figures)
            if isinstance(ans, int):
                self.score -= ans
            else:
                return ans
            self.current_player = 'w'
        else:
            return "It's your opponent's turn!"

        self.moves_history.append((coordinate_1, coordinate_2))
        self.update_possible_moves()
        return coordinate_1, coordinate_2

    def move_from_server(self, coordinate_1, coordinate_2):
        x1, y1 = coordinates_to_computer(coordinate_1)
        x2, y2 = coordinates_to_computer(coordinate_2)

        if self.current_player == 'w':
            self.score += self.handle_move(
                    x1, y1, x2, y2, self.white_figures, self.black_figures)
            self.current_player = 'b'
        elif self.current_player == 'b':
            self.score -= self.handle_move(
                    x1, y1, x2, y2, self.black_figures, self.white_figures)
            self.current_player = 'w'

        self.moves_history.append((coordinate_1, coordinate_2))
        self.update_possible_moves()
        return coordinate_1, coordinate_2

    def get_score(self):
        if self.player == 'w':
            return self.score
        else:
            return -self.score
