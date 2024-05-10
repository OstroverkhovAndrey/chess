
from localization import _

server_answer = {
    #  for registre
    "registre_ok": "Success registre",
    "registre_not": "Not success registre, such a user is already registered",
    #  for login
    "already_login": "You already login",
    "login_dont_registre": "This user_name dont registre",
    "login_already_online": "This user_name already online",
    "success_login": "Success login",
    #  for logout
    "success_logout": "Success logout",
    "logout_not": "Not success logout, you dont login",
    "opponent_give_up": "Opponent give up",
    "success_logout_give_up": "You success give up",
    #  for play
    "you_dont_register": "You dont registre",
    "opponent_dont_registre": "Opponent dont registre",
    "opponent_dont_online": "Opponent dont online",
    "cant_play_with_yourself": "Cant play with yourself",
    "now_opponent_play": "Now opponent play",
    "now_you_play": "Now you play",
    "start_game": "Start game, color: {}",
    "send_game_request": "Send game request",
    "send_you_game_request": "{} send you game request",
}


def mock_for_i18n():
    #  for registre
    _("Success registre")
    _("Not success registre, such a user is already registered")
    #  for login
    _("You already login")
    _("This user_name dont registre")
    _("This user_name already online")
    _("Success login")
    #  for logout
    _("Success logout")
    _("Not success logout, you dont login")
    _("Opponent give up")
    _("You success give up")
