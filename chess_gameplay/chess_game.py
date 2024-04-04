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
    
    def update_possible_moves(self, board):
        self.possible_moves = []
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if -1 < self.x + i < 8 and -1 < self.y + j < 8 and (board[self.x + i][self.y + j] == ' ' or board[self.x + i][self.y + j].isupper() != self.label.isupper()):
                        self.possible_moves.append((self.x + i, self.y + j))

class Queen(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 8
        if color == 'w':
            self.label = 'Q'
        elif color == 'b':
            self.label = 'q'

    def update_possible_moves(self, board):
        self.possible_moves = []
        
        for i in range(1, min(self.x, 7 - self.y) + 1):
            if board[self.x - i][self.y + i] == ' ':
                self.possible_moves.append((self.x - i, self.y + i))
            elif board[self.x - i][self.y + i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x - i, self.y + i))
                break
            else:
                break
        
        for i in range(1, min(7 - self.x, 7 - self.y) + 1):
            if board[self.x + i][self.y + i] == ' ':
                self.possible_moves.append((self.x + i, self.y + i))
            elif board[self.x + i][self.y + i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x + i, self.y + i))
                break
            else:
                break
        
        for i in range(1, min(7 - self.x, self.y) + 1):
            if board[self.x + i][self.y - i] == ' ':
                self.possible_moves.append((self.x + i, self.y - i))
            elif board[self.x + i][self.y - i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x + i, self.y - i))
                break
            else:
                break
        
        for i in range(1, min(self.x, self.y) + 1):
            if board[self.x - i][self.y - i] == ' ':
                self.possible_moves.append((self.x - i, self.y - i))
            elif board[self.x - i][self.y - i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x - i, self.y - i))
                break
            else:
                break
        
        
        for i in range(1, 8 - self.y):
            if board[self.x][self.y + i] == ' ':
                self.possible_moves.append((self.x, self.y + i))
            elif board[self.x][self.y + i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x, self.y + i))
                break
            else:
                break
        
        for i in range(1, 8 - self.x):
            if board[self.x + i][self.y] == ' ':
                self.possible_moves.append((self.x + i, self.y))
            elif board[self.x + i][self.y].isupper() != self.label.isupper():
                self.possible_moves.append((self.x + i, self.y))
                break
            else:
                break
        
        for i in range(1, self.y + 1):
            if board[self.x][self.y - i] == ' ':
                self.possible_moves.append((self.x, self.y - i))
            elif board[self.x][self.y - i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x, self.y - i))
                break
            else:
                break
        
        for i in range(1, self.x + 1):
            if board[self.x - i][self.y] == ' ':
                self.possible_moves.append((self.x - i, self.y))
            elif board[self.x - i][self.y].isupper() != self.label.isupper():
                self.possible_moves.append((self.x - i, self.y))
                break
            else:
                break

class Rook(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 5
        if color == 'w':
            self.label = 'R'
        elif color == 'b':
            self.label = 'r'

    def update_possible_moves(self, board):
        self.possible_moves = []
        
        for i in range(1, 8 - self.y):
            if board[self.x][self.y + i] == ' ':
                self.possible_moves.append((self.x, self.y + i))
            elif board[self.x][self.y + i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x, self.y + i))
                break
            else:
                break
        
        for i in range(1, 8 - self.x):
            if board[self.x + i][self.y] == ' ':
                self.possible_moves.append((self.x + i, self.y))
            elif board[self.x + i][self.y].isupper() != self.label.isupper():
                self.possible_moves.append((self.x + i, self.y))
                break
            else:
                break
        
        for i in range(1, self.y + 1):
            if board[self.x][self.y - i] == ' ':
                self.possible_moves.append((self.x, self.y - i))
            elif board[self.x][self.y - i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x, self.y - i))
                break
            else:
                break
        
        for i in range(1, self.x + 1):
            if board[self.x - i][self.y] == ' ':
                self.possible_moves.append((self.x - i, self.y))
            elif board[self.x - i][self.y].isupper() != self.label.isupper():
                self.possible_moves.append((self.x - i, self.y))
                break
            else:
                break

class Knight(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 3
        if color == 'w':
            self.label = 'KN'
        elif color == 'b':
            self.label = 'kn'

    def update_possible_moves(self, board):
        self.possible_moves = []
        
        for i in [-2, 2]:
            for j in [-1, 1]:
                if -1 < self.x + i < 8 and -1 < self.y + j < 8 and (board[self.x + i][self.y + j] == ' ' or board[self.x + i][self.y + j].isupper() != self.label.isupper()):
                    self.possible_moves.append((self.x + i, self.y + j))
                if -1 < self.x + j < 8 and -1 < self.y + i < 8 and (board[self.x + j][self.y + i] == ' ' or board[self.x + j][self.y + i].isupper() != self.label.isupper()):
                    self.possible_moves.append((self.x + j, self.y + i))

class Bishop(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 3
        if color == 'w':
            self.label = 'B'
        elif color == 'b':
            self.label = 'b'
    
    def update_possible_moves(self, board):
        self.possible_moves = []
        
        for i in range(1, min(self.x, 7 - self.y) + 1):
            if board[self.x - i][self.y + i] == ' ':
                self.possible_moves.append((self.x - i, self.y + i))
            elif board[self.x - i][self.y + i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x - i, self.y + i))
                break
            else:
                break
        
        for i in range(1, min(7 - self.x, 7 - self.y) + 1):
            if board[self.x + i][self.y + i] == ' ':
                self.possible_moves.append((self.x + i, self.y + i))
            elif board[self.x + i][self.y + i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x + i, self.y + i))
                break
            else:
                break
        
        for i in range(1, min(7 - self.x, self.y) + 1):
            if board[self.x + i][self.y - i] == ' ':
                self.possible_moves.append((self.x + i, self.y - i))
            elif board[self.x + i][self.y - i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x + i, self.y - i))
                break
            else:
                break
        
        for i in range(1, min(self.x, self.y) + 1):
            if board[self.x - i][self.y - i] == ' ':
                self.possible_moves.append((self.x - i, self.y - i))
            elif board[self.x - i][self.y - i].isupper() != self.label.isupper():
                self.possible_moves.append((self.x - i, self.y - i))
                break
            else:
                break

class Pawn(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 1
        if color == 'w':
            self.label = 'P'
        elif color == 'b':
            self.label = 'p'
    
    def update_possible_moves(self, board):
        self.possible_moves = []
        
        if self.label.isupper():
            if self.y + 1 < 8:
                if self.x - 1 > -1 and board[self.x - 1][self.y + 1]!= ' ' and board[self.x - 1][self.y + 1].isupper() != self.label.isupper():
                    self.possible_moves.append((self.x - 1, self.y + 1))
                if self.x + 1 < 8 and board[self.x + 1][self.y + 1]!= ' ' and board[self.x + 1][self.y + 1].isupper() != self.label.isupper():
                    self.possible_moves.append((self.x + 1, self.y + 1))
                if board[self.x][self.y + 1] == ' ':
                    self.possible_moves.append((self.x, self.y + 1))
                    if self.y == 1 and board[self.x][self.y + 2] == ' ':
                        self.possible_moves.append((self.x, self.y + 2))
        else:
            if self.y - 1 > -1:
                if self.x - 1 > -1 and board[self.x - 1][self.y - 1]!= ' ' and board[self.x - 1][self.y - 1].isupper() != self.label.isupper():
                    self.possible_moves.append((self.x - 1, self.y - 1))
                if self.x + 1 < 8 and board[self.x + 1][self.y - 1]!= ' ' and board[self.x + 1][self.y - 1].isupper() != self.label.isupper():
                    self.possible_moves.append((self.x + 1, self.y - 1))
                if board[self.x][self.y - 1] == ' ':
                    self.possible_moves.append((self.x, self.y - 1))
                    if self.y == 6 and board[self.x][self.y - 2] == ' ':
                        self.possible_moves.append((self.x, self.y - 2))

WHITE_START_FIGURES = [King(4, 0, 'w'), Queen(3, 0, 'w')] + [Rook(0, 0, 'w'), Rook(7, 0, 'w')] + [Knight(1, 0, 'w'), Knight(6, 0, 'w')] + [Bishop(2, 0, 'w'), Bishop(5, 0, 'w')] + [Pawn(i, 1, 'w') for i in range(8)]
BLACK_START_FIGURES = [King(4, 7, 'b'), Queen(3, 7, 'b')] + [Rook(0, 7, 'b'), Rook(7, 7, 'b')] + [Knight(1, 7, 'b'), Knight(6, 7, 'b')] + [Bishop(2, 7, 'b'), Bishop(5, 7, 'b')] + [Pawn(i, 6, 'b') for i in range(8)]

EMPTY_BOARD = [[' ' for i in range(8)] for j in range(8)]

BOARD_TEMPLATE = """
   0   1   2   3   4   5   6   7\n
 ┌───┬───┬───┬───┬───┬───┬───┬───┐\n
7│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│7\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
6│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│6\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
5│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│5\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
4│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│4\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
3│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│3\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
2│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│2\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
1│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│1\n
 ├───┼───┼───┼───┼───┼───┼───┼───┤\n
0│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│ {:<2}│0\n
 └───┴───┴───┴───┴───┴───┴───┴───┘\n
   0   1   2   3   4   5   6   7\n
"""

class Game():
    def __init__(self):
        self.white_figures = WHITE_START_FIGURES
        self.black_figures = BLACK_START_FIGURES

        self.score = 0
        
        self.update_board()
        self.update_possible_moves()

        self.moves_history = []

        self.curr_player = 'w'

        self.print_board()

    def update_possible_moves(self):
        for fig in self.white_figures + self.black_figures:
            fig.update_possible_moves(self.board)
    
    def update_board(self):
        self.board = EMPTY_BOARD
        for fig in self.white_figures + self.black_figures:
            self.board[fig.x][fig.y] = fig.label

    def print_board(self):
        print(BOARD_TEMPLATE.format(*[self.board[i][j] for j in range(7, -1, -1) for i in range(8)]))


