import os
import psycopg2
import trans_open
DATABASE_URL = os.environ['DATABASE_URL']
doinglist = [_('주인님 드릴 드립 커피를 내리고 있어요!'), _('두둥! 밴드부 활동 중이랍니다!'), _('요리 중이에요☆'), _('놀이터에서 꼬마들이랑 노는 중이랍니다!\n동심이란...후훗'),
             _('주인님의 블로그에 들일 가구들을 고르고 있어요!'), _('공부 중이랍니다!'), _('PUBG 플레이 중! 오늘은 진짜 치킨이에요!'), _('도서관에 왔어요! 현실속의 아카이브 저장소랍니다!')]
mod = []
def setting_set(name: str):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("select body from settings where name='%s'" % name)
    result = cur.fetchone()[0]
    conn.close()
    return result

pluginfolder = "plugin."
prefixvalue = setting_set("prefix")
token = setting_set("token")
owner = setting_set("owner")
osuapikey = setting_set("osuapikey")
gamevalue = setting_set("game")
instructionsvalue = setting_set("instructions")
channel = setting_set("channel")
class Instructions():
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
class Game():
    def __init__(self):
        self.list = []

    def get(self):
        return self.list

    def append(self, splash):
        self.list.append(splash)
class Prefix():
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
instructions = Instructions(instructionsvalue)
gamename = Game()
def gamerefresh():
    global gamename
    gamaname = Game()
    gamename.append(_("DPSBot!"))
    gamename.append(_("%s도움을 쳐보세요!") % prefixvalue)
    gamename.append(_("%s정보를 쳐보세요!") % prefixvalue)
    gamename.append(_("제작자: DPS0340"))
    gamename.append(_("dpsbot.tk"))
    gamename.append(_("github.com/DPS0340/DPSbot"))
    gamename.append(_("teamttakkku.tk"))
    gamename.append(_("Proudly Powered by Team ttakkku"))

gamerefresh()
prefix = Prefix(prefixvalue)