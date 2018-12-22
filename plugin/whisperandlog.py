import asyncio
import psycopg2
import discord
from variables import DATABASE_URL, owner, mod
from discord.ext import commands
from cryptography.fernet import Fernet
import random
from embed import Embed
import gettext
_ = gettext.gettext
class whisperclass():
    def __init__(self, bot):
        self.bot = bot
        self.privatekey = Fernet.generate_key()
        self.cipher_suite = Fernet(self.privatekey)


    @commands.command(name=_("전해줘"), pass_context=True)
    async def send(self, ctx, mention, message):
        try:
            userid = ctx.message.mentions[0].id
            user = await self.bot.get_user_info(userid)
            await self.ping(ctx.message, user, message)
        except Exception as e:
            raise
            await self.bot.say(_("멘션과 메시지를 입력해주세요."))


    @commands.command(name=_("익명"), pass_context=True)
    async def anon(self, ctx, userid):
        towhisperperson = userid
        towhisperperson = await self.bot.get_user_info(towhisperperson)
        B_looks_A = self.cipher_suite.encrypt(
            ctx.message.author.id.encode("utf-8")).decode()
        B_looks_A = B_looks_A.replace("d'", "")
        B_looks_A = B_looks_A.replace("'", "")
        await self.bot.send_message(ctx.message.author, towhisperperson)
        await self.bot.send_message(towhisperperson, _("누군가가 익명으로 대화를 시작합니다!\n 답장하시려면 %s답장과 암호를 한번에 쳐주세요. 암호:\n" % prefix.get())
        await self.bot.send_message(towhisperperson, "%s" % B_looks_A)
        await self.anonping(ctx.message, ctx.message.author, towhisperperson)

    @commands.command(name=_("암호화"), pass_context=True)
    async def reply(self, ctx, text):
        Author_decrypt = await self.bot.get_user_info(self.cipher_suite.decrypt(text.encode("utf-8")).decode())
        await self.bot.send_message(ctx.message.author, _("암호가 확인되었습니다."))
        await self.anonping(ctx, ctx.message.author, Author_decrypt)


    async def ping(self, message, user, body):
        A = message.author
        B = user
        Aname = A.name
        Bname = B.name
        await bot_log(_("채팅을 시도합니다.\n"))
        await bot_log(Aname + "\n")
        await bot_log(Bname + "\n")
        await self.bot.send_message(message.channel, Bname)
        await bot_log(_("%s님이 %s님에게 %s라 말합니다.") % (Aname, Bname, message))
        if message.content.startswith(_('종료')):
            await self.bot.send_message(A, _('종료되었습니다.'))
        else:
            await self.bot.send_message(B, _('%s 씨가 %s(이)라고 전해달라고 말하던데요?') % (name, body))
            await self.bot.send_message(message.channel, _('메시지가 전해졌습니다.'))
            await self.pong(message, A, B)



    async def anonping(self, message, Author, towhisperperson):
        await bot_log(_("익명 채팅을 시도합니다.\n"))
        await bot_log("%s" % Author + "\n")
        await bot_log("%s" % towhisperperson + "\n")
        body = await self.bot.wait_for_message(timeout=60.0, author=Author)
        B = towhisperperson
        A = Author
        if body is None:
            await self.bot.send_message(message.channel, _('응답이 없어서 종료되었습니다.'))
            return
        else:
            if body.content.startswith(_('종료')):
                await self.bot.send_message(A, _('종료되었습니다.'))
            else:
                await bot_log(_("%s가 %s에게 %s라 말합니다.(익명)\n") % (Author, towhisperperson, body.content))
                await self.bot.send_message(B,
                                    _('익명으로 메시지가 왔어요! %s(이)라고 전해달라고 말하던데요?') % body.content)
                await self.bot.send_message(A, _('메시지가 전해졌습니다.'))
                await self.anonpong(message, A, B)
    

    async def anonpong(self, message, A, B):
        body = await self.bot.wait_for_message(timeout=60.0, author=A)
        if body is None:
            await self.bot.send_message(message.message.channel, _('응답이 없어서 종료되었습니다.'))
            return
        else:
            if body.content.startswith(_('종료')):
                await self.bot.send_message(A, _('종료되었습니다.'))
            else:
                await bot_log(_("%s가 %s에게 %s라 말합니다.(익명)\n") % (A, B, body.content))
                await self.bot.send_message(B, _('익명으로 메시지가 왔어요! %s(이)라고 전해달라고 말하던데요?') % body.content)
                await self.bot.send_message(A, _('메시지가 전해졌습니다.'))
                await self.anonpong(message, A, B)


    async def pong(self, message, A, B):
        body = await self.bot.wait_for_message(timeout=60.0, author=A)
        if body is None:
            await self.bot.send_message(message.channel, _('응답이 없어서 종료되었습니다.'))
        else:
            if body.content.startswith(_('종료')):
                await self.bot.send_message(A, _('종료되었습니다.'))
            else:
                await bot_log(_("%s가 %s에게 %s라 말합니다.\n") % (A, B, body.content))
                await self.bot.send_message(B, _('%s 씨가 %s(이)라고 전해달라고 말하던데요?') % (A, body.content))
                await self.bot.send_message(A, _('메시지가 전해졌습니다.'))
                await self.pong(message, A, B)


    async def log(self, message, channel, key):
        listener = message.author
        try:
            body = await self.bot.wait_for_message(channel=channel)
            if body is None:
                await self.bot.send_message(listener, _('응답이 없어서 종료되었습니다.'))
                pass
            else:
                if str(body.content) == str(key) and body.author.name != self.bot.user.name:
                    await self.bot.send_message(listener, _('비밀번호 입력으로 인해 종료되었습니다.'))
                elif body.server == None:
                    pass
                else:
                    await bot_log(_('\n서버:%s\n채널:%s\n작성자:%s\n%s\n') % (body.server, body.channel, body.author, body.content))
                    embed = Embed(title=_("log"), description=_('\n서버:%s\n\n채널:%s\n\n작성자:%s\n\n%s') % (
                        body.server, body.channel, body.author, body.content), color=0xE0FFFF)
                    await self.bot.send_message(message.author, embed=embed)
                    await self.log(message, channel, key)
        except Exception as e:
            print(e)


    @commands.command(name=_("로그켜"), pass_context=True)
    async def log(self, ctx, channelid):
        channel = self.bot.get_channel(channelid)
        key = random.randint(1, 1000000000000000)
        await self.bot.send_message(ctx.message.author, _('종료 코드를 봇이 있는 채널이나 DM에 입력하면 꺼집니다. 종료 코드:'))
        await self.bot.send_message(ctx.message.author, key)
        await bot_log(_("\nlistener is: %s\n") % ctx.message.author)
        try:
            await self.log(ctx.message, channel, key)
        except AttributeError:
            return

async def bot_log(message):
    print(message)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    sql = """insert into log (body) values (%s)"""
    cur.execute(sql, (message, ))
    conn.commit()
    conn.close()

def setup(bot):
    bot.add_cog(whisperclass(bot))
