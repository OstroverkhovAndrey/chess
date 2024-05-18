"""Chess figures library."""

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
        return list of human-like possible positions
        to move on the board (only roques)
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on
        get_possible_roques and get_possible_moves returning lists
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
               or board[x][y][-1] != self.label[-1])):
                possible_moves.append(coordinates_to_human((x, y)))

        possible_moves += self.get_possible_roques(board)

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        """
        Updates the possible_moves class attribute.

        Updates the possible_moves class attribute -
        list of ceils where figure can move.

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
        update possible moves attribute based on
        get_possible_moves returning lists
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
            for length in range(1, 8):
                x = self.x + dx * length
                y = self.y + dy * length
                if not -1 < x < 8 or not -1 < y < 8:
                    break
                elif board[x][y] == ' ':
                    possible_moves.append(
                            coordinates_to_human((x, y)))
                elif board[x][y][-1] != self.label[-1]:
                    possible_moves.append(coordinates_to_human((x, y)))
                    break
                else:
                    break

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        """
        Updates the possible_moves class attribute.

        Updates the possible_moves class attribute -
        list of ceils where figure can move.

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
        update possible moves attribute based on
        get_possible_moves returning lists
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
            for length in range(1, 8):
                x = self.x + dx * length
                y = self.y + dy * length
                if not -1 < x < 8 or not -1 < y < 8:
                    break
                elif board[x][y] == ' ':
                    possible_moves.append(coordinates_to_human((x, y)))
                elif board[x][y][-1] != self.label[-1]:
                    possible_moves.append(coordinates_to_human((x, y)))
                    break
                else:
                    break

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        """
        Updates the possible_moves class attribute.

        Updates the possible_moves class attribute -
        list of ceils where figure can move.

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
        name of the figure as it have to be printed on the board
        ('Knw' or 'Knb')
    possible_moves : list
        list of figure possible moves
    value : int
        value of a figure (default 3)

    Methods
    -------
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on
        get_possible_moves returning lists
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
                    and (board[x][y] == ' ' or board[x][y][-1]
                         != self.label[-1])):
                possible_moves.append(coordinates_to_human((x, y)))

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        """
        Updates the possible_moves class attribute.

        Updates the possible_moves class attribute -
        list of ceils where figure can move.

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
        update possible moves attribute based on
        get_possible_moves returning lists
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
            for length in range(1, 8):
                x = self.x + dx * length
                y = self.y + dy * length
                if not -1 < x < 8 or not -1 < y < 8:
                    break
                elif board[x][y] == ' ':
                    possible_moves.append(coordinates_to_human((x, y)))
                elif board[x][y][-1] != self.label[-1]:
                    possible_moves.append(coordinates_to_human((x, y)))
                    break
                else:
                    break

        return sorted(possible_moves)

    def update_possible_moves(self, board):
        """
        Updates the possible_moves class attribute.

        Updates the possible_moves class attribute -
        list of ceils where figure can move.

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
        indicator of moving for 2 cells since begginning of the game
        (used for en passant)

    Methods
    -------
    get_possible_moves_white_pawn(board)
        return list of human-like possible positions
        to move on the board for white pawn
    get_possible_moves_black_pawn(board)
        return list of human-like possible positions
        to move on the board for black pawn
    get_possible_moves(board)
        return list of human-like possible positions to move on the board
    update_possible_moves(board)
        update possible moves attribute based on
        get_possible_moves returning lists
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
        Updates the possible_moves class attribute.

        Updates the possible_moves class attribute
         - list of ceils where figure can move.

        Parameters
        ----------
        board : list of lists
            a board the figure stay at
        """
        self.possible_moves = [coordinates_to_computer(coordinate)
                               for coordinate in self.get_possible_moves(board)]
