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











