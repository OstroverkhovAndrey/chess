
"""Module for storing information about users registered on the server."""


class UserInfo:
    """
    Information about users registered on the server.

    Parameters
    ----------
    user_name : str
        Name of user, registered on the server
    """

    def __init__(self, user_name: str) -> None:
        """
        Init UserInfo.

        Set user_name, onlain and play status to false, IP and statistic
        to empty string

        Parameters
        ----------
        user_name : str
            Name of user, registered on the server
        """
        self.user_name = user_name
        self.isOnline = False
        self.isPlay = False
        self.IP = ""
        self.statistic = ""
