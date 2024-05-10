
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
