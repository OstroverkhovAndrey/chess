
"""Module that provides functions for internationalization."""

import gettext
import locale
import os


LOCALES = {
    ("ru_RU", "UTF-8"): gettext.translation(
        "msg", os.path.dirname(__file__)+"/po", ["ru"], fallback=True),
    ("en_US", "UTF-8"): gettext.NullTranslations(),
}


def _(text: str) -> str:
    """
    Text translation function according to the current locale.

    Parameters
    ----------
    text : str
        Text for translation

    Returns
    -------
    str
        Translated text
    """
    return LOCALES[locale.getlocale()].gettext(text)
