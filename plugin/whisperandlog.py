import asyncio
import psycopg2
import discord
from variables import DATABASE_URL, owner, mod
from discord.ext import commands
from cryptography.fernet import Fernet
import random

class whisperclass():
    def __init__(self, bot):
        self.bot = bot
        self.privatekey = Fernet.generate_key()
        self.cipher_suite = Fernet(self.privatekey)


    @commands.command(pass_context=True)
    async def 전해줘(self, ctx, mention, message):
        try:
            userid = ctx.message.mentions[0].id
            user = await self.bot.get_user_info(userid)
            await self.ping(ctx.message, user, message)
        except Exception as e:
            raise
            await self.bot.say("멘션과 메시지를 입력해주세요.")


    @commands.command(pass_context=True)
    async def 익명(self, ctx, userid):
        towhisperperson = userid
        towhisperperson = await self.bot.get_user_info(towhisperperson)
        B_looks_A = self.cipher_suite.encrypt(
            ctx.message.author.id.encode("utf-8")).decode()
        B_looks_A = B_looks_A.replace("d'", "")
        B_looks_A = B_looks_A.replace("'", "")
        await self.bot.send_message(ctx.message.author, towhisperperson)
        await self.bot.send_message(towhisperperson, "누군가가 익명으로 대화를 시작합니다!\n 답장하시려면 디피 답장과 암호를 한번에 쳐주세요. 암호:\n")
        await self.bot.send_message(towhisperperson, "%s" % B_looks_A)
        await self.anonping(ctx.message, ctx.message.author, towhisperperson)

    @commands.command(pass_context=True)
    async def 답장(self, ctx, text):
        Author_decrypt = await self.bot.get_user_info(self.cipher_suite.decrypt(text.encode("utf-8")).decode())
        await self.bot.send_message(ctx.message.author, "암호가 확인되었습니다.")
        await self.anonping(ctx, ctx.message.author, Author_decrypt)


    async def ping(self, message, user, body):
        A = message.author
        B = user
        Aname = A.name
        Bname = B.name
        await self.bot_log("채팅을 시도합니다.\n")
        await self.bot_log(Aname + "\n")
        await self.bot_log(Bname + "\n")
        await self.bot.send_message(message.channel, Bname)
        await self.bot_log("%s님이 %s님에게 %s라 말합니다." % (Aname, Bname, message))
        if message.content.startswith('종료'):
            await self.bot.send_message(A, '종료되었습니다.')
        else:
            await self.bot.send_message(B,
                                '%s 씨가 ' % Aname + body + ' (이)라고 전해달라고 말하던데요?')
            await self.bot.send_message(message.channel, '메시지가 전해졌습니다.')
            await self.pong(message, A, B)



    async def anonping(self, message, Author, towhisperperson):
        await self.bot_log("익명 채팅을 시도합니다.\n")
        await self.bot_log("%s" % Author + "\n")
        await self.bot_log("%s" % towhisperperson + "\n")
        body = await self.bot.wait_for_message(timeout=60.0, author=Author)
        B = towhisperperson
        A = Author
        if body is None:
            await self.bot.send_message(message.channel, '응답이 없어서 종료되었습니다.')
            return
        else:
            if body.content.startswith('종료'):
                await self.bot.send_message(A, '종료되었습니다.')
            else:
                await self.bot_log("%s가 %s에게 %s라 말합니다.(익명)\n" % (Author, towhisperperson, body.content))
                await self.bot.send_message(B,
                                    '익명으로 메시지가 왔어요! ' + body.content + ' (이)라고 전해달라고 말하던데요?')
                await self.bot.send_message(A, '메시지가 전해졌습니다.')
                await self.anonpong(message, A, B)


    async def anonpong(self, message, A, B):
        body = await self.bot.wait_for_message(timeout=60.0, author=A)
        if body is None:
            await self.bot.send_message(message.message.channel, '응답이 없어서 종료되었습니다.')
            return
        else:
            if body.content.startswith('종료'):
                await self.bot.send_message(A, '종료되었습니다.')
            else:
                await self.bot_log("%s가 %s에게 %s라 말합니다.(익명)\n" % (A, B, body.content))
                await self.bot.send_message(B, '익명으로 메시지가 왔어요! ' + body.content + ' (이)라고 전해달라고 말하던데요?')
                await self.bot.send_message(A, '메시지가 전해졌습니다.')
                await self.anonpong(message, A, B)


    async def pong(self, message, A, B):
        body = await self.bot.wait_for_message(timeout=60.0, author=A)
        if body is None:
            await self.bot.send_message(message.channel, '응답이 없어서 종료되었습니다.')
        else:
            if body.content.startswith('종료'):
                await self.bot.send_message(A, '종료되었습니다.')
            else:
                await self.bot_log("%s가 %s에게 %s라 말합니다.\n" % (A, B, body.content))
                await self.bot.send_message(B, '%s 씨가 ' % (A) + body.content + ' (이)라고 전해달라고 말하던데요?')
                await self.bot.send_message(A, '메시지가 전해졌습니다.')
                await self.pong(message, A, B)


    async def log(self, message, channel, key):
        listener = message.author
        try:
            body = await self.bot.wait_for_message(channel=channel)
            if body is None:
                await self.bot.send_message(listener, '응답이 없어서 종료되었습니다.')
                pass
            else:
                if str(body.content) == str(key) and body.author.name != 'DPSBot':
                    await self.bot.send_message(listener, '비밀번호 입력으로 인해 종료되었습니다.')
                elif body.server == None:
                    pass
                else:
                    await self.bot_log('\n서버:%s\n채널:%s\n작성자:%s\n%s\n' % (body.server, body.channel, body.author, body.content))
                    embed = discord.Embed(title="log", description='\n서버:%s\n\n채널:%s\n\n작성자:%s\n\n%s' % (
                        body.server, body.channel, body.author, body.content), color=0xE0FFFF)
                    await self.bot.send_message(message.author, embed=embed)
                    await self.log(message, channel, key)
        except Exception as e:
            print(e)


    async def bot_log(self, message):
        print(message)
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        sql = """insert into log (body) values (%s)"""
        cur.execute(sql, (message, ))
        conn.commit()
        conn.close()

    @commands.command(pass_context=True)
    async def 로그켜(self, ctx, channelid):
        channel = self.bot.get_channel(channelid)
        key = random.randint(1, 1000000000000000)
        await self.bot.send_message(ctx.message.author, '종료 코드를 봇이 있는 채널이나 DM에 입력하면 꺼집니다. 종료 코드:')
        await self.bot.send_message(ctx.message.author, key)
        await self.bot_log("\nlistener is: %s\n" % ctx.message.author)
        try:
            await self.log(ctx.message, channel, key)
        except AttributeError:
            return


def setup(bot):
    bot.add_cog(whisperclass(bot))
