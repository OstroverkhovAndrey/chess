
"""A module for storing current games and accessing them."""


class Game:
    """
    Game between two players storing their moves.

    Parameters
    ----------
    user1 : str
        User who play
    user2 : str
        User who play

    Methods
    -------
    move(self, user: str, move: str) -> None
        save move in history
    get_opponent(self, me_name: str) -> str
        return opponent for me_name
    get_game_story(self) -> list
        return game history
    get_draw_request(self) -> bool
        return user who send draw request
    set_draw_request(self, user_name: str) -> None
        set user who send draw request
    remove_draw_request(self) -> None
        delete draw request
    """

    def __init__(self, user1: str, user2: str):
        """
        Init Game.

        Set users, empty game_story list and None draw_request

        Parameters
        ----------
        user1 : str
            User who play
        user2 : str
            User who play
        """
        self.user1 = user1
        self.user2 = user2
        self.game_story = []
        self.draw_request = None

    def move(self, user: str, move: str) -> None:
        """
        Make move in this game. And save move in history.

        Parameters
        ----------
        user : str
            User who play
        move : str
            User who play
        """
        self.game_story.append([user, move])

    def get_opponent(self, me_name: str) -> str:
        """
        Return name opponent me_name user.

        Parameters
        ----------
        me_name : str
            User who play

        Returns
        -------
        str
            Another user_name than me_name
        """
        if me_name == self.user1:
            return self.user2
        elif me_name == self.user2:
            return self.user1
        else:
            return None

    def get_game_story(self) -> list:
        """
        Return corrent game history list.

        Returns
        -------
        list
            Current game_story list
        """
        return self.game_story

    def get_draw_request(self) -> str:
        """
        Returns user name who send draw requests in the game.

        Returns
        -------
        str
            Active draw request
        """
        return self.draw_request

    def set_draw_request(self, user_name: str) -> None:
        """
        Set user_name who send draw_request in the game.

        Parameters
        ----------
        user_name : str
            User who send draw request
        """
        self.draw_request = user_name

    def remove_draw_request(self) -> None:
        """Delete draw request in the game."""
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
