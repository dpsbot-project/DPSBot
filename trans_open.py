from translate import trans
import gettext
_ = gettext.translation('./', localedir='./locales', languages=[trans.outputlang], fallback=True)
_ = _.gettext
def refresh():
    global _
    _ = gettext.translation('./', localedir='./locales', languages=[trans.outputlang], fallback=True)
    _ = _.gettext