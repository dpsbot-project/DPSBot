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
    
    def temprun(self, text: str, src:str, dest:str):
        return self.translator.translate(text, src=src, dest=dest).text   

trans = Trans()