from translate import trans
import gettext

class Opentrans():
    def __init__(self):
        self.lang = gettext.translation('./', localedir='./locales', languages=[trans.get()], fallback=True)
        self.lang.install()
    def refresh(self):
        self.lang = gettext.translation('./', localedir='./locales', languages=[trans.get()], fallback=True)
        self.lang.install()

opentrans = Opentrans()