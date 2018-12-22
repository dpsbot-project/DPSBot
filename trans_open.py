from translate import trans
import gettext

class Opentrans():
    def __init__(self):
        self._ = gettext.translation('./', localedir='./locales', languages=[trans.outputlang], fallback=True)
        self._ = self._.gettext
    def refresh(self):
        self._ = gettext.translation('./', localedir='./locales', languages=[trans.outputlang], fallback=True)
        self._ = self._.gettext

opentrans = Opentrans()