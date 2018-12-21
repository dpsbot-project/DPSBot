import googletrans

class Trans():
    def __init__(self):
        self.translator = googletrans.Translator()
        self.outputlang = 'kr'
    
    def setlang(self, lang: str):
        self.outputlang = lang

    def gettext(self, text: str):
        if self.outputlang == 'kr':
            return text
        return self.translator.translate(text, dest=self.outputlang).text
    
    def temprun(self, text: str, lang:str):
        if lang == 'kr':
            return text
        return self.translator.translate(text, dest=lang).text   

trans = Trans()