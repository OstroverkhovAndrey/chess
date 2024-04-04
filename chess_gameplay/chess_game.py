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

