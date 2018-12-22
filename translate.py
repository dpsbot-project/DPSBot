import googletrans

class Trans():
    def __init__(self):
        self.translator = googletrans.Translator()
        self.outputlang = 'ko-KR'
    
    def setlang(self, lang: str):
        self.outputlang = lang

    def gettext(self, text: str):
        return self.translator.translate(text, dest=self.outputlang).text
    
    def temprun(self, text: str, src:str, dest:str):
        return self.translator.translate(text, src=src, dest=dest).text   

trans = Trans()