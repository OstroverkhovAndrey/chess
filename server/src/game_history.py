
class GameHistory:

    def __init__(self):
        self.history = []

    def get_statistic_for_user(self, user_name):
        win = 0
        draw = 0
        lose = 0
        for player1, player2, result, _ in self.history:
            if player1 == user_name or player2 == user_name:
                if result == user_name:
                    win += 1
                elif result == "draw":
                    draw += 1
                else:
                    lose += 1
        return [win, draw, lose]

    def add_game(self, player1, player2, result, story):
        self.history.append([player1, player2, result, story])
