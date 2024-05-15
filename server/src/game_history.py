
"""Module for storing already played games."""


class GameHistory:
    """
    Class for storing already played games.

    Methods
    -------
    get_statistic_for_user(self, user_name: str) -> list
        get statistic for user
    add_game(self, player1: str, player2: str, result: str, story: list) -> None
        add a played game to the history
    """

    def __init__(self) -> None:
        """
        Init GameHistory.

        Set empty history list
        """
        self.history = []

    def get_statistic_for_user(self, user_name: str) -> list:
        """
        Get statistic for user.

        Parameters
        ----------
        user_name : str
            The name of the user whose statistics you need to find out

        Returns
        -------
        List
            Count [win, draw, lose] for user_name
        """
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

    def add_game(
            self, player1: str, player2: str, result: str, story: list) -> None:
        """
        Add a played game to the history.

        Parameters
        ----------
        player1 : str
            User who play
        player2 : str
            User who play
        result : str
            Draw or name win user
        story : list
            List with move in this game
        """
        self.history.append([player1, player2, result, story])
