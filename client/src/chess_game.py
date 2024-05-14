"""Client-side chess game library."""

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
    Converts coordinates to human-like format.

    Parameters
    ----------
    to_translate : tuple
        tuple of x and y - coordinates (both 0 to 7)

    Returns
    -------
    str
        human-like coordinate
    """
    if isinstance(to_translate, str):
        return to_translate

    return (COMPUTER_TO_HUMAN_TRANSLATOR[0][to_translate[0]]
            + COMPUTER_TO_HUMAN_TRANSLATOR[1][to_translate[1]])


def coordinates_to_computer(to_translate):
    """
    Converts coordinates to machine-like format.

    Parameters
    ----------
    to_translate : str
        human-like coordinates

    Returns
    -------
    str
        machine-like coordinate
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
        Init of Figure class.

        Parameters
        ----------
        x : int
            first coordinate of figure (0 to 7)
        y : int
            second coordinate of figure (0 to 7)
        color : str
            present side which figure is on ('w' -white or 'b' - black)
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
        present side which figure is on ('w' - white or 'b' - black)
    label : str
        name of the figure as it have to be printed on the board ('Kw' or 'Kb')
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
        return list of human-like possible positions to move on the board (only roques)
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on get_possible_roques and get_possible_moves returning lists
    """

    def __init__(self, x, y, color):
        """
        Init of King class.

        Parameters
        ----------
        x : int
            first coordinate of figure (0 to 7)
        y : int
            second coordinate of figure (0 to 7)
        color : str
            present side which figure is on ('w' -white or 'b' - black)
        """
        super().__init__(x, y, color)
        self.value = 0
        if color == 'w':
            self.label = 'Kw'
        elif color == 'b':
            self.label = 'Kb'
        self.has_moved = False
        self.is_under_attack = False

    def get_possible_roques(self, board):
        """
        Returns list of ceils where figure can move (roques only).

        Parameters
        ----------
        board : list of lists
            a board the figure staying at

        Returns
        -------
        list
            list of ceils where figure can move (roques only)
        """
        possible_moves = []

        if not self.has_moved:
            for dx in [-3, -2, -1]:
                x = self.x + dx
                y = self.y
                if board[x][y] != ' ':
                    break
            else:
                if self.label == 'Kw' and board[0][0] == 'Rw':
                    possible_moves.append(coordinates_to_human((2, 0)))
                elif self.label == 'Kb' and board[0][7] == 'Rb':
                    possible_moves.append(coordinates_to_human((2, 7)))

            for dx in [1, 2]:
                x = self.x + dx
                y = self.y
                if board[x][y] != ' ':
                    break
            else:
                if self.label == 'Kw' and board[7][0] == 'Rw':
                    possible_moves.append(coordinates_to_human((6, 0)))
                elif self.label == 'Kb' and board[7][7] == 'Rb':
                    possible_moves.append(coordinates_to_human((6, 7)))

        return possible_moves

    def get_possible_moves(self, board):
        """
        Returns list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure stay at

        Returns
        -------
        list
            list of ceils where figure can move
        """
        if (self.x != 4 or self.label == 'Kw' and self.y != 0
                or self.label == 'Kb' and self.y != 7):
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
        """
        Updates the possible_moves class attribute - list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure stay at
        """
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Queen(Figure):
    """
    A class used to present Queen chess figure.

    Attributes
    ----------
    x : int
        first coordinate of figure (0 to 7)
    y : int
        second coordinate of figure (0 to 7)
    color : str
        present side which figure is on ('w' - white or 'b' - black)
    label : str
        name of the figure as it have to be printed on the board ('Qw' or 'Qb')
    possible_moves : list
        list of figure possible moves
    value : int
        value of a figure (default 8)

    Methods
    -------
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on get_possible_moves returning lists
    """

    def __init__(self, x, y, color):
        """
        Init of Queen class.

        Parameters
        ----------
        x : int
            first coordinate of figure (0 to 7)
        y : int
            second coordinate of figure (0 to 7)
        color : str
            present side which figure is on ('w' -white or 'b' - black)
        """
        super().__init__(x, y, color)
        self.value = 8
        if color == 'w':
            self.label = 'Qw'
        elif color == 'b':
            self.label = 'Qb'

    def get_possible_moves(self, board):
        """
        Returns list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure staying at

        Returns
        -------
        list
            list of ceils where figure can move
        """
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
        """
        Updates the possible_moves class attribute - list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure stay at
        """
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Rook(Figure):
    """
    A class used to present Rook chess figure.

    Attributes
    ----------
    x : int
        first coordinate of figure (0 to 7)
    y : int
        second coordinate of figure (0 to 7)
    color : str
        present side which figure is on ('w' - white or 'b' - black)
    label : str
        name of the figure as it have to be printed on the board ('Rw' or 'Rb')
    possible_moves : list
        list of figure possible moves
    value : int
        value of a figure (default 5)

    Methods
    -------
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on get_possible_moves returning lists
    """

    def __init__(self, x, y, color):
        """
        Init of Rook class.

        Parameters
        ----------
        x : int
            first coordinate of figure (0 to 7)
        y : int
            second coordinate of figure (0 to 7)
        color : str
            present side which figure is on ('w' -white or 'b' - black)
        """
        super().__init__(x, y, color)
        self.value = 5
        if color == 'w':
            self.label = 'Rw'
        elif color == 'b':
            self.label = 'Rb'
        self.has_moved = False

    def get_possible_moves(self, board):
        """
        Returns list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure staying at

        Returns
        -------
        list
            list of ceils where figure can move
        """
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
        """
        Updates the possible_moves class attribute - list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure stay at
        """
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Knight(Figure):
    """
    A class used to present Knight chess figure.

    Attributes
    ----------
    x : int
        first coordinate of figure (0 to 7)
    y : int
        second coordinate of figure (0 to 7)
    color : str
        present side which figure is on ('w' - white or 'b' - black)
    label : str
        name of the figure as it have to be printed on the board ('Knw' or 'Knb')
    possible_moves : list
        list of figure possible moves
    value : int
        value of a figure (default 3)

    Methods
    -------
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on get_possible_moves returning lists
    """

    def __init__(self, x, y, color):
        """
        Init of Knight class.

        Parameters
        ----------
        x : int
            first coordinate of figure (0 to 7)
        y : int
            second coordinate of figure (0 to 7)
        color : str
            present side which figure is on ('w' -white or 'b' - black)
        """
        super().__init__(x, y, color)
        self.value = 3
        if color == 'w':
            self.label = 'KNw'
        elif color == 'b':
            self.label = 'KNb'

    def get_possible_moves(self, board):
        """
        Returns list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure staying at

        Returns
        -------
        list
            list of ceils where figure can move
        """
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
        """
        Updates the possible_moves class attribute - list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure stay at
        """
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Bishop(Figure):
    """
    A class used to present Rook chess figure.

    Attributes
    ----------
    x : int
        first coordinate of figure (0 to 7)
    y : int
        second coordinate of figure (0 to 7)
    color : str
        present side which figure is on ('w' - white or 'b' - black)
    label : str
        name of the figure as it have to be printed on the board ('Bw' or 'Bb')
    possible_moves : list
        list of figure possible moves
    value : int
        value of a figure (default 3)

    Methods
    -------
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on get_possible_moves returning lists
    """

    def __init__(self, x, y, color):
        """
        Init of Bishop class.

        Parameters
        ----------
        x : int
            first coordinate of figure (0 to 7)
        y : int
            second coordinate of figure (0 to 7)
        color : str
            present side which figure is on ('w' -white or 'b' - black)
        """
        super().__init__(x, y, color)
        self.value = 3
        if color == 'w':
            self.label = 'Bw'
        elif color == 'b':
            self.label = 'Bb'

    def get_possible_moves(self, board):
        """
        Returns list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure staying at

        Returns
        -------
        list
            list of ceils where figure can move
        """
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
        """
        Updates the possible_moves class attribute - list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure stay at
        """
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]


class Pawn(Figure):
    """
    A class used to present Rook chess figure.

    Attributes
    ----------
    x : int
        first coordinate of figure (0 to 7)
    y : int
        second coordinate of figure (0 to 7)
    color : str
        present side which figure is on ('w' - white or 'b' - black)
    label : str
        name of the figure as it have to be printed on the board ('Pw' or 'Pb')
    possible_moves : list
        list of figure possible moves
    value : int
        value of a figure (default 1)
    has_moved_two : bool
        indicator of moving for 2 cells since begginning of the game (used for en passant)

    Methods
    -------
    get_possible_moves_white_pawn(board)
        return list of human-like possible positions to move on the board for white pawn
    get_possible_moves_black_pawn(board)
        return list of human-like possible positions to move on the board for black pawn
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on get_possible_moves returning lists
    """

    def __init__(self, x, y, color):
        """
        Init of Pawn class.

        Parameters
        ----------
        x : int
            first coordinate of figure (0 to 7)
        y : int
            second coordinate of figure (0 to 7)
        color : str
            present side which figure is on ('w' -white or 'b' - black)
        """
        super().__init__(x, y, color)
        self.value = 1
        if color == 'w':
            self.label = 'Pw'
        elif color == 'b':
            self.label = 'Pb'
        self.has_moved_two = False

    def possible_moves_white_pawn(self, board):
        """
        Returns list of ceils where white figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure staying at

        Returns
        -------
        list
            list of ceils where white figure can move
        """
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
        """
        Returns list of ceils where black figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure staying at

        Returns
        -------
        list
            list of ceils where black figure can move
        """
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
        """
        Returns list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure staying at

        Returns
        -------
        list
            list of ceils where figure can move
        """
        if self.label[-1] == 'w':
            return self.possible_moves_white_pawn(board)
        else:
            return self.possible_moves_black_pawn(board)

    def update_possible_moves(self, board):
        """
        Updates the possible_moves class attribute - list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure stay at
        """
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
1│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │1
 ├────┼────┼────┼────┼────┼────┼────┼────┤
2│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │2
 ├────┼────┼────┼────┼────┼────┼────┼────┤
3│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │3
 ├────┼────┼────┼────┼────┼────┼────┼────┤
4│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │4
 ├────┼────┼────┼────┼────┼────┼────┼────┤
5│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │5
 ├────┼────┼────┼────┼────┼────┼────┼────┤
6│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │6
 ├────┼────┼────┼────┼────┼────┼────┼────┤
7│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │7
 ├────┼────┼────┼────┼────┼────┼────┼────┤
8│{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │{:>3} │8
 └────┴────┴────┴────┴────┴────┴────┴────┘
   h    g    f    e    d    c    b    a
"""


class Game():
    """
    A class used to present chess game.

    Attributes
    ----------
    board : list
        list (len 8) of lists (len 8) where each element is string (' ' if there is no figure and figure label otherwise)
    white_figures : list
        list of white figures on the board
    black_figures : list
        list of white figures on the board
    player : str
        color of the figures the player plays with ('w' - white, 'b' - black)
    current_player : str
        color of the figures which turn now ('w' - white, 'b' - black)
    score : int
        score advantage if game (score > 0 for white and score < 0 for black)
    moves_history : list
        list of tuples of tuples - start and end coordinates of moves in game

    Methods
    -------
    get_possible_moves()
        return dictionary with keys - coordinates of figures on player's side and values - list of ceils where those figures can move
    update_possible_moves()
        update possible_moves attribute of each figure in white_figures and black_figures lists
    get_board()
        return board as string in "pretty" format
    update_board()
        updates board attribute
    print_board()
        print board in "pretty" format
    cancel_move(x1, y1, x2, y2, moving_figures, fixed_figures, eated_figure)
        cancel move from (x1, y1) to (x2, y2)
    is_check_move(x1, x2, y1, y2, moving_figures, fixed_figures, eated_figure)
        check if move from (x1, y1) to (x2, y2) led to check
    is_checkmate()
        check if any King is checkmated
    handle_roque(x1, y1, x2, y2, moving_figures)
        handle roque from (x1, y1) to (x2, y2)
    handle_en_passant(x1, y1, x2, y2, moving_figures, fixed_figures)
        handle en passant from (x1, y1) to (x2, y2)
    handle_en_passant_roque(x1, y1, x2, y2, moving_figures, fixed_figures)
        handle roque or en passant from (x1, y1) to (x2, y2)
    handle_move(x1, y1, x2, y2, moving_figures, fixed_figures)
        handle move from (x1, y1) to (x2, y2)
    move(coordinate_1, coordinate_2)
        handle move from (x1, y1) to (x2, y2)
    move_from_server(coordinate_1, coordinate_2)
        handle forced move from (x1, y1) to (x2, y2)
    get_score()
        return your score advantage
    """

    def __init__(self, player):
        """
        Init of Pawn class.

        Parameters
        ----------
        player : str
            color of the figures the player plays with ('w' - white, 'b' - black)
        """
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
        """
        Merges all figures in game possible_moves attributes into dictionaty.

        Returns
        -------
        dictionary
            dictionary with keys - coordinates of figures on player's side and values - list of ceils where those figures can move
        """
        possible_moves = {}

        if self.current_player == 'w' and self.player == 'w':
            for fig in self.white_figures:
                possible_moves[coordinates_to_human((fig.x, fig.y))] = (
                        fig.get_possible_moves(self.board))
            return dict(sorted(possible_moves.items()))
        elif self.current_player == 'b' and self.player == 'b':
            for fig in self.black_figures:
                possible_moves[coordinates_to_human((fig.x, fig.y))] = (
                        fig.get_possible_moves(self.board))
            return dict(sorted(possible_moves.items()))
        else:
            return []

    def update_possible_moves(self):
        """Updates all figures in game possible_moves attributes."""
        for fig in self.white_figures + self.black_figures:
            fig.update_possible_moves(self.board)

    def update_board(self):
        """Updates board attribute based on each figure in game coordinate."""
        self.board = [line[:] for line in EMPTY_BOARD]
        for fig in self.white_figures + self.black_figures:
            self.board[fig.x][fig.y] = fig.label

    def get_board(self):
        """Returns board as string in "pretty" format."""
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
        """Prints board in "pretty" format."""
        self.update_board()
        if self.player == 'w':
            print(BOARD_TEMPLATE_WHITE.format(*[self.board[i][j]
                  for j in range(7, -1, -1) for i in range(8)]))
        else:
            print(BOARD_TEMPLATE_BLACK.format(*[self.board[7 - i][7 - j]
                  for j in range(7, -1, -1) for i in range(8)]))

    def cancel_move(self, x1, y1, x2, y2,
                    moving_figures, fixed_figures, eated_figure=None):
        """
        Moves the figure back and recovers eated figure.

        Parameters
        ----------
        x1 : int
            first coordinate of ceil where figure was moved from
        y1 : int
            second coordinate of ceil where figure was moved from
        x2 : int
            first coordinate of ceil where figure was moved to
        y2 : int
            second coordinate of ceil where figure was moved to
        moving_figures : list
            list of figures of player whose turn was it
        fixed_figures : list
            list of figures of the opposite player
        eated_figure
            Figure which was eated in this turn (None if any figure was eated)
        """
        for fig in moving_figures:
            if fig.x == x2 and fig.y == y2:
                fig.x = x1
                fig.y = y1
        if eated_figure is not None:
            fixed_figures.append(eated_figure)

    def is_check_move(self, x1, x2, y1, y2,
                      moving_figures, fixed_figures, eated_figure=None):
        """
        Check if made move led to check and calls cancel_move method if player's King is checked or checkmated after move.

        Parameters
        ----------
        x1 : int
            first coordinate of ceil where figure was moved from
        y1 : int
            second coordinate of ceil where figure was moved from
        x2 : int
            first coordinate of ceil where figure was moved to
        y2 : int
            second coordinate of ceil where figure was moved to
        moving_figures : list
            list of figures of player whose turn was it
        fixed_figures : list
            list of figures of the opposite player
        eated_figure
            Figure which was eated in this turn (None if any figure was eated)

        Returns
        -------
        str
            'IMPOSSIBLE MOVE: YOU CAN'T MAKE MOVE TO CHECK' if move led to player's King to be checked or checkmated
            'CHECKMATE!' if move led to opposite King to be checkmated
            'CHECK!' if move led to opposite King to be checked
        """
        self.update_possible_moves()
        king_x = moving_figures[0].x
        king_y = moving_figures[0].y
        for fig in fixed_figures:
            for (x, y) in fig.possible_moves:
                if x == king_x and y == king_y:
                    self.cancel_move(x1, y1, x2, y2,
                                     moving_figures, fixed_figures,
                                     eated_figure)
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
        """
        Check if King is under checkmate.

        Returns
        -------
        bool
            True if King is under checkmate
            False if King is not under checkmate
        """
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
        """
        Moves corresoponding figures to handle the roque.

        Parameters
        ----------
        x1 : int
            first coordinate of ceil where figure whould be moved from
        y1 : int
            second coordinate of ceil where figure should be moved from
        x2 : int
            first coordinate of ceil where figure should be moved to
        y2 : int
            second coordinate of ceil where figure should be moved to
        moving_figures : list
            list of figures of active player

        Returns
        -------
        int
            -1 if the move is not roque
        None
            if the roque was made succesfully
        """
        if ((self.current_player == 'w' and self.board[x1][y1] == 'Kw'
                or self.current_player == 'b' and self.board[x1][y1] == 'Kb')
                and abs(x2 - x1) == 2 and (x2, y2)
                in moving_figures[0].possible_moves):
            for fig in moving_figures:
                if ((self.current_player == 'w' and fig.label == 'Rw' or
                    self.current_player == 'b' and fig.label == 'Rb') and
                   (x2 == 2 and fig.x == 0 or x2 == 6 and fig.x == 7)):
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = ' '
                    self.board[0 if x2 == 2 else 7][y1] = ' '
                    moving_figures[0].x = x2
                    fig.x = 3 if x2 == 2 else 5
                    moving_figures[0].update_possible_moves(self.board)
                    break
        else:
            return -1

    def handle_en_passant(self, x1, y1, x2, y2, moving_figures, fixed_figures):
        """
        Moves and removes corresoponding figures to handle the en passant.

        Parameters
        ----------
        x1 : int
            first coordinate of ceil where figure whould be moved from
        y1 : int
            second coordinate of ceil where figure should be moved from
        x2 : int
            first coordinate of ceil where figure should be moved to
        y2 : int
            second coordinate of ceil where figure should be moved to
        moving_figures : list
            list of figures of active player
        fixed_figures : list
            list of figures of the opposite player

        Returns
        -------
        int
            1 if black figure was eated during en passant
        int
            -1 if white figure was eated during en passant
        int
            0 if the move is not en passant
        """
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
        """
        Moves and removes corresoponding figures to handle roque or en passant.

        Parameters
        ----------
        x1 : int
            first coordinate of ceil where figure whould be moved from
        y1 : int
            second coordinate of ceil where figure should be moved from
        x2 : int
            first coordinate of ceil where figure should be moved to
        y2 : int
            second coordinate of ceil where figure should be moved to
        moving_figures : list
            list of figures of active player
        fixed_figures : list
            list of figures of the opposite player

        Returns
        -------
        int
            0 if roque or en passant was made successfully
        int
            -1 if the move is neither roque not en passant
        """
        if not self.handle_roque(x1, y1, x2, y2, moving_figures):
            return 0
        if (t := self.handle_en_passant(x1, y1, x2, y2,
                                        moving_figures, fixed_figures) != 0):
            self.score += t
            return 0
        else:
            return -1

    def handle_move(self, x1, y1, x2, y2, moving_figures, fixed_figures):
        """
        Handles move from (x1, y1) to (x2, y2) if it is possible move.

        Parameters
        ----------
        x1 : int
            first coordinate of ceil where figure whould be moved from
        y1 : int
            second coordinate of ceil where figure should be moved from
        x2 : int
            first coordinate of ceil where figure should be moved to
        y2 : int
            second coordinate of ceil where figure should be moved to
        moving_figures : list
            list of figures of active player
        fixed_figures : list
            list of figures of the opposite player

        Returns
        -------
        str
            'IMPOSSIBLE MOVE' if proposed move is impossible
        int
            0 if the move is roque or en passant and the move was made successfully
        str
            'CHECK!' or 'CHECKMATE!' if move led to check or checkmate respectively
        int
            score changes after successful neither roque not en passant move
        """
        if self.handle_en_passant_roque(x1, y1, x2, y2,
                                        moving_figures, fixed_figures) == 0:
            return 0

        score = 0
        eated_figure = None
        for fig in moving_figures:
            if fig.x == x1 and fig.y == y1:
                if (x2, y2) in fig.possible_moves:
                    if self.board[x2][y2] != ' ':
                        for i in range(len(fixed_figures)):
                            if (fixed_figures[i].x == x2
                                    and fixed_figures[i].y == y2):
                                score = fixed_figures[i].value
                                eated_figure = fixed_figures[i]
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
                                 moving_figures, fixed_figures, eated_figure)
        if ans is not None:
            return ans
        else:
            return score

    def move(self, coordinate_1, coordinate_2):
        """
        Calls handle_move method if it is players turn now.

        Parameters
        ----------
        coordinate_1 : str
            human-like coordinate of the ceil figure should be moved from
        coordinate_2 : str
            human-like coordinate of the ceil figure should be moved to

        Returns
        -------
        str
            'IMPOSSIBLE MOVE' if proposed move is impossible
        str
            'It's your opponent's turn!' if now it is opponent's move
        tuple
            tuple of human-like coordinates - move-from and move-to ceils - if the move was made successfully
        """
        self.update_possible_moves()
        x1, y1 = coordinates_to_computer(coordinate_1)
        x2, y2 = coordinates_to_computer(coordinate_2)

        if self.current_player == 'w' and self.player == 'w':
            ans = self.handle_move(
                    x1, y1, x2, y2, self.white_figures, self.black_figures)
            if isinstance(ans, int):
                self.score += ans
            else:
                return ans
            self.current_player = 'b'
        elif self.current_player == 'b' and self.player == 'b':
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
        """
        Calls handle_move forcedly.

        Parameters
        ----------
        coordinate_1 : str
            human-like coordinate of the ceil figure should be moved from
        coordinate_2 : str
            human-like coordinate of the ceil figure should be moved to

        Returns
        -------
        tuple
            tuple of human-like coordinates - move-from and move-to ceils
        """
        self.update_possible_moves()
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
        """Returns score advantage of active player."""
        if self.player == 'w':
            return self.score
        else:
            return -self.score
