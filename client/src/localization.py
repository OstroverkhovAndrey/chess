
import gettext


translation = gettext.translation("msg", "po", fallback=True)
_, ngettext = translation.gettext, translation.ngettext
