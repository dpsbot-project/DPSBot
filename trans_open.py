from translate import trans
import gettext
_ = gettext.translation('data', localedir='locale', languages=[trans.outputlang])
def refresh():
    global _
    _ = gettext.translation('data', localedir='locale', languages=[trans.outputlang])