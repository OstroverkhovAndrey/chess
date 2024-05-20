"""Client-side chess game library."""

import copy
import figures


WHITE_START_FIGURES = ([figures.King(4, 0, 'w'), figures.Queen(3, 0, 'w')]
                       + [figures.Rook(0, 0, 'w'), figures.Rook(7, 0, 'w')]
                       + [figures.Knight(1, 0, 'w'), figures.Knight(6, 0, 'w')]
                       + [figures.Bishop(2, 0, 'w'), figures.Bishop(5, 0, 'w')]
                       + [figures.Pawn(i, 1, 'w') for i in range(8)])
BLACK_START_FIGURES = ([figures.King(4, 7, 'b'), figures.Queen(3, 7, 'b')]
                       + [figures.Rook(0, 7, 'b'), figures.Rook(7, 7, 'b')]
                       + [figures.Knight(1, 7, 'b'), figures.Knight(6, 7, 'b')]
                       + [figures.Bishop(2, 7, 'b'), figures.Bishop(5, 7, 'b')]
                       + [figures.Pawn(i, 6, 'b') for i in range(8)])

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
        list (len 8) of lists (len 8) where each element is string
        (' ' if there is no figure and figure label otherwise)
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
        return dictionary with keys - coordinates of figures on
        player's side and values - list of ceils where those figures can move
    update_possible_moves()
        update possible_moves attribute of each figure in
        white_figures and black_figures lists
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
    is_draw(moving_figures, fixed_figures)
        check if it is draw situation
    isDrawMove(coordinate_1, coordinate_2)
        check if suggested move will lead to draw
    isWinMove(coordinate_1, coordinate_2)
        check if suddested move will lead to checkmate
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
            color of the figures the player plays with
            ('w' - white, 'b' - black)
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
            dictionary with keys - coordinates of figures on player's
            side and values - list of ceils where those figures can move
        """
        possible_moves = {}

        if self.current_player == 'w' and self.player == 'w':
            for fig in self.white_figures:
                possible_moves[figures.coordinates_to_human((fig.x, fig.y))] = (
                        fig.get_possible_moves(self.board))
            return dict(sorted(possible_moves.items()))
        elif self.current_player == 'b' and self.player == 'b':
            for fig in self.black_figures:
                possible_moves[figures.coordinates_to_human((fig.x, fig.y))] = (
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

    def isMyMove(self):
        """Returns True if it is the player's turn, False otherwise."""
        if self.player == self.current_player:
            return True
        else:
            return False

    def isPossibleMove(self, coordinate_1, coordinate_2):
        """Returns True if suggested move is possible, False otherwise."""
        d = self.get_possible_moves()
        if coordinate_1 in list(d.keys()) and coordinate_2 in d[coordinate_1]:
            return True
        else:
            return False

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
        if ((self.board[x2][y2] == 'Kw' or self.board[x2][y2] == 'Kb') and
                abs(x2 - x1) == 2):
            for fig in moving_figures:
                if x2 == 6 and fig.x == 5 and fig.label[0] == 'R':
                    fig.x = 7
                    break
                elif x2 == 2 and fig.x == 3 and fig.label[0] == 'R':
                    fig.x = 0
                    break

        for fig in moving_figures:
            if fig.x == x2 and fig.y == y2:
                fig.x = x1
                fig.y = y1
        if eated_figure is not None:
            fixed_figures.append(eated_figure)

    def is_draw(self, moving_figures, fixed_figures):
        """
        Check if it is draw situation now.

        Parameters
        ----------
        moving_figures : list
            list of figures of active player
        fixed_figures : list
            list of figures of non-active player

        Returns
        -------
        bool
            True if it is draw
            False otherwise
        """
        king_x = moving_figures[0].x
        king_y = moving_figures[0].y

        for fig in fixed_figures:
            for (x, y) in fig.possible_moves:
                if x == king_x and y == king_y:
                    return False

        for fig in moving_figures:
            x = fig.x
            y = fig.y
            for (x2, y2) in fig.possible_moves[::-1]:
                eated_figure = None
                if self.board[x2][y2] != ' ':
                    for i in range(len(fixed_figures)):
                        if (fixed_figures[i].x == x2 and
                                fixed_figures[i].y == y2):
                            eated_figure = fixed_figures.pop(i)
                            self.board[x2][y2] = ' '
                            break
                if self.move_from_server(figures.coordinates_to_human((x, y)),
                                         figures.coordinates_to_human((x2,
                                                                       y2))):
                    self.cancel_move(x, y, x2, y2, moving_figures,
                                     fixed_figures, eated_figure)
                    self.update_board()
                    self.update_possible_moves()
                    return False
                self.cancel_move(x, y, x2, y2, moving_figures,
                                 fixed_figures, eated_figure)
                self.update_board()
                self.update_possible_moves()
        return True

    def isDrawMove(self, coordinate_1, coordinate_2):
        """
        Check if suggested move will lead to draw, doesn't make move.

        Parameters
        ----------
        coordinate_1 : str
            human-like coordinates of first cell of suggested move
        coordinate_2 : str
            human-like coordinates of first cell of suggested move

        Returns
        -------
        bool
            True if suggested move will lead to draw
            False otherwise
        """
        if self.current_player == 'w':
            moving_figures = self.white_figures
            fixed_figures = self.black_figures
        else:
            moving_figures = self.black_figures
            fixed_figures = self.white_figures

        if not self.isPossibleMove(coordinate_1, coordinate_2):
            return False

        x1, y1 = figures.coordinates_to_computer(coordinate_1)
        x2, y2 = figures.coordinates_to_computer(coordinate_2)

        white_king_has_moved = self.white_figures[0].has_moved
        black_king_has_moved = self.black_figures[0].has_moved

        eated_figure = None
        if self.board[x2][y2] != ' ':
            for i in range(len(fixed_figures)):
                if fixed_figures[i].x == x2 and fixed_figures[i].y == y2:
                    eated_figure = fixed_figures.pop(i)
                    break

        for m_fig in moving_figures:
            if m_fig.x == x1 and m_fig.y == y1:
                m_fig.x = x2
                m_fig.y = y2
                self.board[x2][y2] = self.board[x1][y1]
                self.board[x1][y1] = ' '
                break

        if self.current_player == 'w':
            self.current_player = 'b'
        else:
            self.current_player = 'w'
        ans = self.is_draw(fixed_figures, moving_figures)

        self.update_board()
        self.update_possible_moves()

        self.cancel_move(x1, y1, x2, y2, moving_figures,
                         fixed_figures, eated_figure)

        self.white_figures[0].has_moved = white_king_has_moved
        self.black_figures[0].has_moved = black_king_has_moved

        self.update_board()
        self.update_possible_moves()

        return ans

    def isWinMove(self, coordinate_1, coordinate_2):
        """
        Check if suggested move will lead to checkmate, doesn't make move.

        Parameters
        ----------
        coordinate_1 : str
            human-like coordinates of first cell of suggested move
        coordinate_2 : str
            human-like coordinates of first cell of suggested move

        Returns
        -------
        bool
            True if suggested move will lead to checkmate
            False otherwise
        """
        if self.current_player == 'w':
            moving_figures = self.white_figures
            fixed_figures = self.black_figures
        else:
            moving_figures = self.black_figures
            fixed_figures = self.white_figures

        if not self.isPossibleMove(coordinate_1, coordinate_2):
            return False

        x1, y1 = figures.coordinates_to_computer(coordinate_1)
        x2, y2 = figures.coordinates_to_computer(coordinate_2)

        white_king_has_moved = self.white_figures[0].has_moved
        black_king_has_moved = self.black_figures[0].has_moved

        eated = None
        if self.board[x2][y2] != ' ':
            for i in range(len(fixed_figures)):
                if fixed_figures[i].x == x2 and fixed_figures[i].y == y2:
                    eated = fixed_figures.pop(i)
                    break

        for m_fig in moving_figures:
            if m_fig.x == x1 and m_fig.y == y1:
                m_fig.x = x2
                m_fig.y = y2
                self.board[x2][y2] = self.board[x1][y1]
                self.board[x1][y1] = ' '
                break

        ans = self.is_checkmate()

        self.cancel_move(x1, y1, x2, y2, moving_figures, fixed_figures, eated)

        self.white_figures[0].has_moved = white_king_has_moved
        self.black_figures[0].has_moved = black_king_has_moved

        self.update_board()
        self.update_possible_moves()

        return ans

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

        king_position = (figures.coordinates_to_human((moving_figures[0].x,
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
                    self.update_board()
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
            0 if the move is roque or en passant and the move was made
            successfully
        str
            'CHECK!' or 'CHECKMATE!' if move led to check or checkmate
            respectively
        int
            score changes after successful neither roque not en passant move
        """
        if self.handle_en_passant_roque(x1, y1, x2, y2,
                                        moving_figures, fixed_figures) == 0:
            return 0

        score = 0
#        eated_figure = None
        for fig in moving_figures:
            if fig.x == x1 and fig.y == y1:
                if (x2, y2) in fig.possible_moves:
                    if self.board[x2][y2] != ' ':
                        for i in range(len(fixed_figures)):
                            if (fixed_figures[i].x == x2
                                    and fixed_figures[i].y == y2):
                                score = fixed_figures[i].value
#                                eated_figure = fixed_figures.pop(i)
                                break
                    fig.x = x2
                    fig.y = y2
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = ' '
                    if isinstance(fig, figures.Pawn) and (abs(y2 - y1) == 2):
                        fig.has_moved_two = True
                    break
        else:
            return 'IMPOSSIBLE MOVE'

        ans = score
#        ans = self.is_check_move(x1, y1, x2, y2,
#                                 moving_figures, fixed_figures, eated_figure)

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
            tuple of human-like coordinates - move-from and move-to ceils -
            if the move was made successfully
        """
        self.update_possible_moves()
        x1, y1 = figures.coordinates_to_computer(coordinate_1)
        x2, y2 = figures.coordinates_to_computer(coordinate_2)

        if self.current_player == 'w' and self.player == 'w':
            ans = self.handle_move(
                    x1, y1, x2, y2, self.white_figures, self.black_figures)
            self.current_player = 'b'
            if isinstance(ans, int):
                self.score += ans
            else:
                return False
        elif self.current_player == 'b' and self.player == 'b':
            ans = self.handle_move(
                    x1, y1, x2, y2, self.black_figures, self.white_figures)
            self.current_player = 'w'
            if isinstance(ans, int):
                self.score -= ans
            else:
                return False
        else:
            return False

        self.moves_history.append((coordinate_1, coordinate_2))
        self.update_possible_moves()
        return True

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
        x1, y1 = figures.coordinates_to_computer(coordinate_1)
        x2, y2 = figures.coordinates_to_computer(coordinate_2)

        if self.current_player == 'w':
            ans = self.handle_move(
                    x1, y1, x2, y2, self.white_figures, self.black_figures)
            self.current_player = 'b'
            if isinstance(ans, int):
                self.score += ans
            else:
                return False
        elif self.current_player == 'b':
            ans = self.handle_move(
                    x1, y1, x2, y2, self.black_figures, self.white_figures)
            self.current_player = 'w'
            if isinstance(ans, int):
                self.score -= ans
            else:
                return False
        else:
            return False

        self.moves_history.append((coordinate_1, coordinate_2))
        self.update_possible_moves()
        return True

    def get_score(self):
        """Returns score advantage of active player."""
        if self.player == 'w':
            return self.score
        else:
            return -self.score
