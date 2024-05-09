
class Game:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.game_story = []
        self.draw_request = None

    def move(self, user, move):
        self.game_story.append([user, move])

    def get_opponent(self, me_name):
        if me_name == self.user1:
            return self.user2
        elif me_name == self.user2:
            return self.user1
        else:
            return None

    def get_game_story(self):
        return self.game_story

    def get_draw_request(self):
        return self.draw_request

    def set_draw_request(self, user_name):
        self.draw_request = user_name

    def remove_draw_request(self):
        self.draw_request = None


class GamesDict:
    def __init__(self):
        self.user1_to_user2 = {}
        self.user2_to_user1 = {}
        self.game_dict = {}

    def add_game(self, user1, user2):
        self.user1_to_user2[user1] = user2
        self.user2_to_user1[user2] = user1
        self.game_dict[user1+" "+user2] = Game(user1, user2)

    def stop_game(self, user1, user2):
        if user1 in self.user1_to_user2:
            del self.user1_to_user2[user1]
        if user2 in self.user1_to_user2:
            del self.user1_to_user2[user2]
        if user1 in self.user2_to_user1:
            del self.user2_to_user1[user1]
        if user2 in self.user2_to_user1:
            del self.user2_to_user1[user2]
        if user1+" "+user2 in self.game_dict:
            del self.game_dict[user1+" "+user2]
        if user2+" "+user1 in self.game_dict:
            del self.game_dict[user2+" "+user1]

    def __getitem__(self, user):
        if user in self.user1_to_user2:
            user1, user2 = user, self.user1_to_user2[user]
        else:
            user2, user1 = user, self.user2_to_user1[user]
        return self.game_dict[user1+" "+user2]
