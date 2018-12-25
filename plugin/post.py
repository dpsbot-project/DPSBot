import asyncio
import psycopg2
import discord
from variables import DATABASE_URL, owner, mod, prefix
from discord.ext import commands
from embed import Embed
class postclass():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="write", alias=["써줘"], pass_context=True)
    async def write(self, ctx, *heads):
        conn = psycopg2.connect(DATABASE_URL)
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
            await self.bot.send_message(ctx.message.channel, _("제목이 없습니다."))
            pass
        else:
            await self.bot.send_message(ctx.message.channel, _("내용을 말해주세요!"))
            body = await self.bot.wait_for_message(timeout=600, author=ctx.message.author)
            body = body.content
            author = ctx.message.author.name
            embed = Embed(title="%s" % head, description="\nby %s\n%s" % (
                author, body), color=0xE0FFFF)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            await self.postinsert("post", num, author, head, body)


    @commands.command(name="show", aliases=["보여줘"], pass_context=True)
    async def show(self, ctx):
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('select * from post')
        rows = cur.fetchall()
        for row in rows:
            num = row[0]
            author = row[1]
            head = row[2]
            await self.bot.send_message(ctx.message.channel, "%s. %s - by %s\n" % (num, head, author))
        conn.close()
        await self.bot.send_message(ctx.message.channel, _("%s글 (번호)를 입력하시면 글을 보실수 있어요!") % prefix.get())


    @commands.command(name="post", aliases=["글"], pass_context=True)
    async def post(self, ctx, select: int):
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('select * from post where num = {0}'.format(select))
        row = cur.fetchone()
        num = row[0]
        author = row[1]
        head = row[2]
        body = row[3]
        conn.close()
        embed = Embed(title="%s. %s" % (
            num, head), description="\nby %s\n%s" % (author, body), color=0xE0FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(name="deletepost", aliases=["글삭제"], pass_context=True)
    async def deletepost(self, ctx, select: int):
        if ctx.message.author.id == owner or ctx.message.author.id in mod:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("""delete from post where num = %d""" % select)
            conn.commit()
            conn.close()
            await self.bot.send_message(ctx.message.channel, _("%d 글 삭제 완료!") % select)
        else:
            await self.bot.send_message(ctx.message.channel, _("당신은 권한이 없습니다.\n당신이 봇의 소유자거나 관리자인지 확인해 보세요."))


    async def postinsert(self, table, num, author, head, body):
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        sql = """insert into {0} ("num","author","head","body") values (%s, %s, %s, %s)""".format(
            table)
        cur.execute(sql, (int(num), str(author), str(head), str(body)))
        conn.commit()
        conn.close()

def setup(bot):
    bot.add_cog(postclass(bot))
