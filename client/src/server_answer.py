
"""Module for translating server responses into messages for the user."""

from internationalization import _

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
    "opponent_give_up_logout": "Opponent give up",
    "success_logout_give_up": "You success give up",
    #  for play
    "you_dont_login": "You dont login now",
    "opponent_dont_registre": "Opponent dont registre",
    "opponent_dont_online": "Opponent dont online",
    "cant_play_with_yourself": "Cant play with yourself",
    "now_opponent_play": "Now opponent play",
    "now_you_play": "Now you play",
    "start_game": "Start game, color: {}",
    "send_game_request": "Send game request",
    "send_you_game_request": "{} send you game request",
    # for move
    "you_dont_play_now": "You dont play now",
    "move_opponent_refused_draw": "Opponent refused a draw",
    "you_get_move": "You get move",
    "opponent_get_move": "Opponent get move {}",
    #  for draw
    "send_draw_request": "Send draw request",
    "opponent_send_you_draw_request": "Opponent send you draw request",
    "opponent_dont_send_draw_request": "Opponent dont send draw request",
    "you_cant_delete_draw_request": "You cant delete draw request",
    "you_refused_draw": "You refused a draw",
    "opponent_refused_draw": "Opponent refused a draw",
    "draw": "Draw",
    #  for give up
    "you_success_give_up": "You success give up",
    "opponent_give_up": "Opponent give up\nYou win!",
    #  for get game request
    "game_request": "From me: {}\nFor me: {}",
    #  for remove game request
    "success_remove_game_request": "Success remove game request",
    "not_found_you_game_request": "Not found you game request",
    #  for statistic
    "statistic": "Statistic for {}\nwin: {}\ndraw: {}\ndefeat: {}",
}


def mock_for_i18n() -> None:
    """
    Do not call this function.

    Function exists so that the i18n can see the lines that need
    to be translated.
    """
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
    #  for play
    _("You dont login now")
    _("Opponent dont registre")
    _("Opponent dont online")
    _("Cant play with yourself")
    _("Now opponent play")
    _("Now you play")
    _("Start game, color: {}")
    _("Send game request")
    _("{} send you game request")
    # for move
    _("You dont play now")
    _("Opponent refused a draw")
    _("You get move")
    _("Opponent get move {}")
    #  for draw
    _("Send draw request")
    _("Opponent send you draw request")
    _("Opponent dont send draw request")
    _("You cant delete draw request")
    _("You refused a draw")
    _("Opponent refused a draw")
    _("Draw")
    #  for give up
    _("You success give up")
    _("Opponent give up\nYou win!")
    #  for get game request
    _("From me: {}\nFor me: {}")
    #  for remove game request
    _("Success remove game request")
    _("Not found you game request")
    #  for statistic
    _("Statistic for {}\nwin: {}\ndraw: {}\ndefeat: {}")
