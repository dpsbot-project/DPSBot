# -*- coding:utf-8 -*-
from discord.ext import commands
import discord
import asyncio
import random
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# IMPORTANT! #
# if you want to use proxy server when you use archiveis. edit this library. #
# or others can view your ip address. #
import archiveis
from osuapi import OsuApi, ReqConnector
import requests
import types
import pickle
import pickle_mixin
import os
import copy
import re
import sqlite3


# put some server on proxystring #
proxyString = "127.0.0.1:8080"
desired_capability = webdriver.DesiredCapabilities.FIREFOX
desired_capability['proxy'] = {
            "proxyType": "manual",
            "httpProxy": proxyString,
            "ftpProxy": proxyString,
            "sslProxy": proxyString
        }
options = Options()
options.add_argument('--headless')
options.add_argument('--log-level=3')
options.add_argument('--mute-audio')
profile = webdriver.FirefoxProfile()
profile.set_preference("media.volume_scale", "0.0")
profile.set_preference("intl.accept_languages", "ko")
driver = webdriver.Firefox(profile, firefox_options=options)
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
bot = commands.Bot(command_prefix="디피 ")
global privatekey, cipher_suite, funckey
privatekey = Fernet.generate_key()
cipher_suite = Fernet(privatekey)
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await 태그로드()
    await bot.change_presence(game=discord.Game(name="디피 도움"))

@bot.event
async def 태그로드():
    conn = sqlite3.connect("data\\data.db")
    cur = conn.cursor()
    cur.execute("select * from tag")
    rows = cur.fetchall()
    for row in rows:
        name = row[0]
        message = row[1]
        await taginit(name, message)

@bot.event
async def alohinsert(table, num, head, body):
    conn = sqlite3.connect("data\\data.db")
    cur = conn.cursor()
    sql = "insert into {0} (num,head,body) values (?, ?, ?)".format(table)
    cur.execute(sql, (int(num), str(head), str(body)))
    conn.commit()
    conn.close()

@bot.event
async def postinsert(table, num, author, head, body):
    conn = sqlite3.connect("data\\data.db")
    cur = conn.cursor()
    sql = "insert into {0} (num,author,head,body) values (?, ?, ?, ?)".format(table)
    cur.execute(sql, (int(num), str(author), str(head), str(body)))
    conn.commit()
    conn.close()

@bot.event
async def taginsert(table, name, body):
    conn = sqlite3.connect("data\\data.db")
    cur = conn.cursor()
    sql = "insert into {0} (name,body) values (?, ?)".format(table)
    cur.execute(sql, (str(name), str(body)))
    conn.commit()
    conn.close()

@bot.event
async def taginit(name, message):
    nameclone = copy.deepcopy(name)
    messageclone = copy.deepcopy(message)
    # making some functions
    @bot.command(name = "t" + name, pass_context=True)
    async def tag(ctx):
        await bot.send_message(ctx.message.channel, messageclone)
        print(nameclone)
        print(messageclone)

doinglist = ['주인님 드릴 드립 커피를 내리고 있어요!', '두둥! 밴드부 활동 중이랍니다!', '요리 중이에요☆', '놀이터에서 꼬마들이랑 노는 중이랍니다!\n동심이란...후훗',
             '주인님의 블로그에 들일 가구들을 고르고 있어요!', '공부 중이랍니다!', 'PUBG 플레이 중! 오늘은 진짜 치킨이에요!', '도서관에 왔어요! 현실속의 아카이브 저장소랍니다!']
#write this.
self = 'your_bot_id'

@bot.command(pass_context=True)
async def 안녕(ctx):
    await bot.say("안녕하세요!")

@bot.command(pass_context=True)
async def 블라인드(ctx):
    await bot.say("---------------블라인드 중입니다---------------")
    await bot.say(".\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.")
    await bot.say("---------------블라인드가 끝났습니다---------------")

@bot.command(pass_context=True)
async def 암호화(ctx, *words):
    plaintext = ''
    i = 0
    for word in words:
        i += 1
        if word == words[-1] and len(words) == i:
            plaintext += str(word)
        else:
            plaintext += str(word) + ' '
    encryptedtext = cipher_suite.encrypt(plaintext.encode("utf-8")).decode()
    await bot.send_message(ctx.message.channel, encryptedtext)

@bot.command(pass_context=True)
async def 복호화(ctx, encryptedtext):
    plaintext = cipher_suite.decrypt(encryptedtext.encode("utf-8")).decode()
    await bot.send_message(ctx.message.channel, plaintext)

@bot.command(pass_context=True)
async def 그라바타(ctx, plaintext):
    h = hashlib.md5()
    h.update(plaintext.encode("utf-8").lower())
    encryptedtext = h.hexdigest()
    await bot.send_message(ctx.message.channel, encryptedtext)
    await bot.send_message(ctx.message.channel, "http://www.gravatar.com/avatar/" + encryptedtext)


@bot.command(pass_context=True)
async def 오스(ctx, *user):
    username = ''
    i = 0
    for word in user:
        i += 1
        if word == user[-1] and len(user) == i:
            username += str(word)
        else:
            username += str(word) + ' '
    # put some api keu
    api = OsuApi("your_api_key", connector=ReqConnector())
    results = api.get_user(username)
    userid = results[0].user_id
    thumbnail = "https://s.ppy.sh/a/" + str(userid)
    embed = discord.Embed(title="%s" % (username), description="id:%s" % (userid), color=0xE0FFFF)
    embed.set_thumbnail(url=thumbnail)
    await bot.send_message(ctx.message.channel, embed=embed)
    await bot.send_message(ctx.message.channel, "https://osu.ppy.sh/users/%d" % userid)

@bot.command(pass_context=True, name="태그")
async def 태그(ctx, *names):
    name = ''
    i = 0
    for word in names:
        i += 1
        if word == names[-1] and len(names) == i:
            name += str(word)
        else:
            name += str(word) + ' '
    await bot.send_message(ctx.message.channel, "제목: %s\n내용을 입력해 주세요." % name)
    await bot.send_message(ctx.message.channel, "주의! 제목에는 띄어쓰기가 불가능합니다.")
    body = await bot.wait_for_message(timeout=100.0, author=ctx.message.author)
    if not body == '':
        # making some functions
        @bot.command(name="t" + name, pass_context=True)
        async def tag(ctx):
            await bot.send_message(ctx.message.channel, body.content)
            print(name)
            print(body.content)
        await taginsert("tag", name, body.content)
        await bot.send_message(ctx.message.channel, "등록되었습니다.")
    else:
        await bot.send_message(ctx.message.channel, "공백은 안돼요!")
@bot.command(pass_context=True)
async def 사진(ctx):
    await bot.send_message(ctx.message.channel, "https://sge17th.xyz/upload/")

@bot.command(pass_context=True)
async def 아카이브(ctx, url):
    await bot_log("%s가 %s를(을) 아카이브 했습니다.\n" % (ctx.message.author, url))
    try:
        if not "http" in url:
            url = "http://" + url
        # you can use porked library and put proxystring for now
        # https://github.com/DPS0340/archiveis
        archive_url = archiveis.capture(url)
        await bot.send_message(ctx.message.channel, "아카이브 중입니다...\n"
                                                       "조금만 기다려 주세요!")
        driver.get(url)
        driver.maximize_window()
        driver.find_element_by_tag_name('html').screenshot('screenshot.png')
        await bot.send_file(ctx.message.channel, 'screenshot.png')
        await bot.send_message(ctx.message.channel, archive_url)
        await bot_log("아카이브 주소:%s\n" % (url))
    except:
        await bot.send_message(ctx.message.channel, "오류가 발생했어요!")
    finally:
        driver.close()

@bot.event
async def Aloh(ctx):
    with open("data/Alohbackup.txt", "r", encoding="utf-8") as a:
        body = ''
        while True:
            sayd = a.readline()
            if sayd == "0.5배라는 건가요" or sayd == "Speed 0.5는":
                body += sayd + '\n'
            else:
                if sayd:
                    sayd = sayd.replace('\n', '')
                    checker = bool(re.match('[0-9]+[.]', sayd))
                    if checker is True:
                        if body == '':
                            body += sayd + '\n'
                        num = re.match('[0-9]+[.]', sayd).group().replace('.', '')
                        await alohinsert("alohsayd", int(num) - 1, "Alohsayd " + str(int(num) - 1), body)
                        body = sayd + '\n'
                        print(num)
                        print(sayd)
                    else:
                        body += sayd + '\n'
                else:
                    body += '\n' + sayd + '\n'
                    await alohinsert("alohsayd", int(1172), "Alohsayd " + str(1172), body)
                    body = ''
                    print(num)
                    print(sayd)
                    break

@bot.command(pass_context=True)
async def 귓속말(ctx):
    await bot.send_message(ctx.message.channel, "DM을 봐주세요!")
    await bot.send_message(ctx.message.author, "저를 부르셨나요...?")
    await bot.send_message(ctx.message.author, "이제 눈치보지 마시고 마음껏 얘기해 주세요!")

@bot.command(pass_context=True)
async def 도움(ctx):
    await bot.say("DM을 봐주세요!")
    await bot.send_message(ctx.message.author,
                              "설명입니다.\n\n디피 안녕\nDPS봇이 인사합니다.\n\n디피 귓속말\nDPS봇이 DM을 합니다. 명령어를 사용하실 수 있습니다.\n\n"
                              "디피 로그켜\n봇이 로깅을 시작합나다.\n\n디피 전해줘 (멘션) (내용)\n특정 사용자에게 DM을 대신 보내줍니다.\n\n디피 익명 (16자리 ID)\n익명으로 DM을 대신 보내줍니다.\n\n디피 답장 (암호)\n익명으로 온 DM에 답장합니다."
                              "\n\n디피 사진\nDPS봇이 사진을 자체 서버에 올리는 링크를 전해줘요! 큰 gif 같은걸 불러올때 좋답니다!"
                              "\n\n디피 아카이브 (url)\nDPS봇이 아카이브를 떠줘요! 사진과 url로 저장된답니다!\n주의:아카이브의 모든 책임은 본인에게 있답니다."
                              "\n\n종료\nDM을 종료합니다."
                              "\n\n디피 태그 (제목) (내용)\nDPS봇이 태그를 만들어줘요!"
                              "\n\n디피 t(제목)\nDPS봇이 태그를 보여준답니다!"
                              "\n\n디피 스위트룸\nDPS봇이 개발자의 홈페이지로 가는 링크를 알려줍니다.")

@bot.command(pass_context=True)
async def 이팔(ctx):
    await dp28(ctx.message)

@bot.command(pass_context=True, name="28")
async def 이팔2(ctx):
    await dp28(ctx.message)

@bot.command(pass_context=True)
async def 죽어(ctx):
    await bot.send_message(ctx.message.channel, '싫어요!')

@bot.command(pass_context=True)
async def 닥쳐(ctx):
    await bot.send_message(ctx.message.channel, '싫어요!')

@bot.command(pass_context=True)
async def 로그켜(ctx):
    key = random.randint(10000000, 1000000000000000)
    await bot.send_message(ctx.message.author, '종료 코드를 봇이 있는 채널이나 DM에 입력하면 꺼집니다. 종료 코드:')
    await bot.send_message(ctx.message.author, key)
    await bot_log("\nlistener is: %s\n" % ctx.message.author)
    try:
        await log(ctx.message, key)
    except AttributeError:
        return

@bot.command(pass_context=True)
async def 헬로월드(ctx):
    await bot.send_message(ctx.message.channel, '안녕하세요....DPS봇입니다!')

@bot.command(pass_context=True)
async def 뭐해(ctx):
    random.shuffle(doinglist)
    await bot.send_message(ctx.message.channel, doinglist[0])

@bot.command(pass_context=True)
async def 스위트룸(ctx):
    embed = discord.Embed(title="SGE17th의 스위트룸", description="https://sge17th.xyz", color=0xE0FFFF)
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def 내성위키(ctx):
    embed = discord.Embed(title="내성위키", description="https://naesung.tk", color=0xE0FFFF)
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def 다리위키(ctx):
    embed = discord.Embed(title="다리위키", description="https://bridge.ml", color=0xE0FFFF)
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def 단어위키(ctx):
    embed = discord.Embed(title="단어위키", description="https://wordwiki.net", color=0xE0FFFF)
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def 내가누구(ctx):
    embed = discord.Embed(title="당신은 혹시...", description="\n%s\n\n이신가요?!?!" % ctx.message.author, color=0xE0FFFF)
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def 건의(ctx, msg):
    me = await bot.get_user_info('316553064087552001')
    channel = bot.get_channel('474732217340264448')
    mention = ctx.message.author.name
    await bot.send_message(channel, '%s 님이 ' % (mention) + msg + ' (이)라고 건의했습니다.')
    await bot.send_message(me, '존경하는 주인님♡\n소식이 있어요!\n %s 님이 ' % (mention) + msg + ' (이)라고 건의했습니다.')

@bot.command(pass_context=True)
async def 써줘(ctx, *heads):
    conn = sqlite3.connect("data\\data.db")
    with conn:
        try:
            cur = conn.cursor()
            num = cur.lastlowid
            num += 1
        except:
            num = 1
            pass
    i = 0
    head = ''
    for word in heads:
        i += 1
        if word == heads[-1] and len(heads) == i:
            head += word
        else:
            head += word + ' '
    if len(heads) == 0:
        await bot.send_message(ctx.message.channel, "제목이 없습니다.")
        pass
    else:
        await bot.send_message(ctx.message.channel, "내용을 말해주세요!")
        body = await bot.wait_for_message(timeout=600, author=ctx.message.author)
        body = body.content
        author = ctx.message.author.name
        embed = discord.Embed(title="%s" % head, description="\nby %s\n%s" % (author, body), color=0xE0FFFF)
        await bot.send_message(ctx.message.channel, embed=embed)
        await postinsert("post", num, author, head, body)

@bot.command(pass_context=True)
async def 알로세이드(ctx, num: int):
    await bot.send_message(ctx.message.channel, "알로세이드는 1172번까지 있습니다.")
    if 0 <= num <= 1172:
        conn = sqlite3.connect("data\\data.db")
        with conn:
            try:
                cur = conn.cursor()
                cur.execute("select * from alohsayd where num={0}".format(num))
                rows = cur.fetchall()
                row = rows[0]
                print(row)
                num = row[0]
                head = row[1]
                body = row[2]
                head = head.replace("\n", "")
                embed = discord.Embed(title="%s" % head, description="\n%s" % (body), color=0xE0FFFF)
                await bot.send_message(ctx.message.channel, embed=embed)
            except:
                await bot.send_message(ctx.message.channel, "파일을 찾지 못했어요!")
                pass

@bot.command(pass_context=True)
async def 보여줘(ctx):
    conn = sqlite3.connect("data\\data.db")
    cur = conn.cursor()
    cur.execute("select * from post")
    rows = cur.fetchall()
    for row in rows:
        num = row[0]
        author = row[1]
        head = row[2]
        await bot.send_message(ctx.message.channel, "%s. %s - by %s\n" % (num, head, author))
    await bot.send_message(ctx.message.channel, "디피 글 (번호)를 입력하시면 글을 보실수 있어요!")

@bot.command(pass_context=True)
async def 글(ctx, select: int):
    conn = sqlite3.connect("data\\data.db")
    cur = conn.cursor()
    cur.execute("select * from post where num = {0}".format(select))
    row = cur.fetchone()
    num = row[0]
    author = row[1]
    head = row[2]
    body = row[3]
    embed = discord.Embed(title="%s. %s" % (num, head), description="\nby %s\n%s" % (author, body), color=0xE0FFFF)
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def 전해줘(ctx, user, *message):
    await ping(ctx.message, user, message)

@bot.command(pass_context=True)
async def 익명(ctx, user):
    towhisperperson = user
    towhisperperson = await bot.get_user_info(towhisperperson)
    B_looks_A = cipher_suite.encrypt(ctx.message.author.id.encode("utf-8")).decode()
    B_looks_A = B_looks_A.replace("d'", "")
    B_looks_A = B_looks_A.replace("'", "")
    await bot.send_message(ctx.message.author, towhisperperson)
    await bot.send_message(towhisperperson, "누군가가 익명으로 대화를 시작합니다!\n 답장하시려면 디피 답장과 암호를 한번에 쳐주세요. 암호:\n")
    await bot.send_message(towhisperperson, "%s" % B_looks_A)
    await anonping(ctx.message, ctx.message.author, towhisperperson)

@bot.command(pass_context=True)
async def 찍어(ctx):
    await bot.send_message(ctx.message.channel, '마피아 게임인가요...?!\n머리를 굴려서 특정 사용자를 찍을게요!\n')
    list = []
    members = ctx.message.server.members
    for x in members:
        list.append(x.name)
    random.shuffle(list)
    member = list[0]
    mention = member
    await bot.send_message(ctx.message.channel, mention + '\n님을 찍겠습니다☆')

@bot.command(pass_context=True)
async def 정보(ctx):
    await info(ctx.message)

@bot.command(pass_context=True)
async def 답장(ctx, text):
    Author_decrypt = await bot.get_user_info(cipher_suite.decrypt(text.encode("utf-8")).decode())
    await bot.send_message(ctx.message.author, "암호가 확인되었습니다.")
    await anonping(ctx, ctx.message.author, Author_decrypt)
@bot.event
async def ping(message, user, chattuple):
    body = ''
    for word in chattuple:
        if word == chattuple[-1]:
            body += word
        else:
            body += word + ' '
    print(user)
    user = user.replace("!", "")
    user = user.replace("<@", "")
    user = user.replace(">", "")
    print(user)
    towhisperperson = await bot.get_user_info(user)
    await bot_log("채팅을 시도합니다.\n")
    await bot_log(message.author.name + "\n")
    await bot_log(towhisperperson.name + "\n")
    await bot.send_message(message.channel, towhisperperson)
    await bot_log("%s%s가 %s에게 %s라 말합니다." % (message.author.id, message.author.discriminator, towhisperperson, body))
    B = towhisperperson
    A = message.author
    if message.content.startswith('종료'):
        await bot.send_message(A, '종료되었습니다.')
    else:
        await bot.send_message(towhisperperson,
                                  '%s 씨가 ' % (message.author) + body + ' (이)라고 전해달라고 말하던데요?')
        await bot.send_message(message.channel, '메시지가 전해졌습니다.')
        await pong(message, A, B)
    pass

@bot.event
async def anonping(message, Author, towhisperperson):
    await bot_log("익명 채팅을 시도합니다.\n")
    await bot_log("%s" % Author + "\n")
    await bot_log("%s" % towhisperperson + "\n")
    body = await bot.wait_for_message(timeout=60.0, author=Author)
    B = towhisperperson
    A = Author
    if body is None:
        await bot.send_message(message.channel, '응답이 없어서 종료되었습니다.')
        return
    else:
        if body.content.startswith('종료'):
            await bot.send_message(A, '종료되었습니다.')
        else:
            await bot_log("%s가 %s에게 %s라 말합니다.(익명)\n" % (Author, towhisperperson, body.content))
            await bot.send_message(B,
                                      '익명으로 메시지가 왔어요! ' + body.content + ' (이)라고 전해달라고 말하던데요?')
            await bot.send_message(A, '메시지가 전해졌습니다.')
            await anonpong(message, A, B)
        pass

@bot.event
async def dp28(message):
    await bot.send_message(message.channel, 'DP-28! 박물관에 있는 총 아닌가요?')

@bot.event
async def info(message):
    person = message.mentions[0].id
    person = await bot.get_user_info(person)
    name = person.name
    discriminator = person.discriminator
    avatar = person.avatar_url
    id = person.id
    embed = discord.Embed(title="%s#%s" % (name, discriminator), description="id:%s" % (id), color=0xE0FFFF)
    embed.set_thumbnail(url=avatar)
    await bot.send_message(message.channel, embed=embed)


@bot.event
async def anonpong(message, A, B):
    body = await bot.wait_for_message(timeout=60.0, author=A)
    if body is None:
        await bot.send_message(message.message.channel, '응답이 없어서 종료되었습니다.')
        return
    else:
        if body.content.startswith('종료'):
            await bot.send_message(A, '종료되었습니다.')
        else:
            await bot_log("%s가 %s에게 %s라 말합니다.(익명)\n" % (A, B, body.content))
            await bot.send_message(B, '익명으로 메시지가 왔어요! ' + body.content + ' (이)라고 전해달라고 말하던데요?')
            await bot.send_message(A, '메시지가 전해졌습니다.')
            await anonpong(message, A, B)
        pass

@bot.event
async def pong(message, A, B):
    body = await bot.wait_for_message(timeout=60.0, author=A)
    if body is None:
        await bot.send_message(message.channel, '응답이 없어서 종료되었습니다.')
    else:
        if body.content.startswith('종료'):
            await bot.send_message(A, '종료되었습니다.')
        else:
            await bot_log("%s가 %s에게 %s라 말합니다.\n" % (A, B, body.content))
            await bot.send_message(B, '%s 씨가 ' % (A) + body.content + ' (이)라고 전해달라고 말하던데요?')
            await bot.send_message(A, '메시지가 전해졌습니다.')
            await pong(message, A, B)
        pass
@bot.event
async def log(message, key):
    listener = message.author
    try:
        body = await bot.wait_for_message(timeout=2000000, channel=message.channel)
        if body is None:
            await bot.send_message(listener, '응답이 없어서 종료되었습니다.')
            pass
        else:
            if str(body.content) == str(key) and body.author.name != 'DPSBot':
                await bot.send_message(listener, '비밀번호 입력으로 인해 종료되었습니다.')
            elif body.server == None:
                pass
            else:
                await bot_log('\n서버:%s\n채널:%s\n작성자:%s\n%s\n' % (body.server, body.channel, body.author, body.content))
                embed = discord.Embed(title="log", description='\n서버:%s\n\n채널:%s\n\n작성자:%s\n\n%s' % (body.server, body.channel, body.author, body.content), color=0xE0FFFF)
                await bot.send_message(message.author, embed=embed)
                await log(message, key)
            pass
    except AttributeError:
        pass

@bot.event
async def bot_log(message):
    with open("log.txt", 'a') as log:
        log.write(message)
        
bot.run("your token")
