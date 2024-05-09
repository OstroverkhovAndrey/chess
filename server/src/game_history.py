
class GameHistory:

    def __init__(self):
        self.history = []

    def get_statistic_for_user(self, user_name):
        return [1, 2, 3]

    def add_game(self, player1, player2, result, story):
        self.history.append([player1, player2, result, story])
