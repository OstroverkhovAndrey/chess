
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
