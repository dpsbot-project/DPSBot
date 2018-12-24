from translate import trans
import gettext

class Opentrans():
    def __init__(self):
        self.lang = gettext.translation('data', localedir='./locales', languages=[trans.get()], fallback=True)
        self.lang.install()
    def refresh(self):
        self.lang = gettext.translation('data', localedir='./locales', languages=[trans.get()], fallback=True)
        self.lang.install()
    def set(self, lang):
        self.lang = gettext.translation('data', localedir='./locales', languages=[lang], fallback=True)
        self.lang.install()

opentrans = Opentrans()