import googletrans

class Trans():
    def __init__(self):
        self.translator = googletrans.Translator()
        self.outputlang = 'en_US'
    
    def setlang(self, lang: str):
        self.outputlang = lang

    def get(self):
        return self.outputlang

    def gettext(self, text: str):
        if self.outputlang == 'ko_KR' or self.outputlang == 'en_US':
            return text
        return self.translator.translate(text, dest=self.outputlang).text


    def gettext_remote(self, text: str, lang:str):
        if lang == 'ko_KR' or lang == 'en_US':
            return text
        return self.translator.translate(text, dest=lang).text

    def temprun(self, text: str, src:str, dest:str):
        if self.outputlang == 'ko_KR' or self.outputlang == 'en_US':
            return text
        return self.translator.translate(text, src=src, dest=dest).text   

trans = Trans()
