import asyncio
import psycopg2
import random
import discord
import re
from discord.ext import commands
from embed import Embed
import os

DATABASE_URL = os.environ['DATABASE_URL']


class alohclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="alohsayd", aliases=["알로세이드"], pass_context=True)
    async def alohsayd(self, ctx, num: int):
        await self.bot.send_message(ctx.message.channel, _("알로세이드는 1172번까지 있습니다."))
        if 0 <= num <= 1172:
            await self.alohsaydCore(ctx, num)

    @commands.command(name="alohsaydrandom", aliases=["알로세이드랜덤"], pass_context=True)
    async def alohsaydrandom(self, ctx):
        num = random.randrange(0, 1173)
        await self.bot.send_message(ctx.message.channel, _("랜덤 알로세이드"))
        await self.alohsaydCore(ctx, num)

    async def alohsaydCore(self, ctx, num: int):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
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
                embed = Embed(
                    title="%s" % head, description="\n%s" % (body), color=0xE0FFFF)
                await self.bot.send_message(ctx.message.channel, embed=embed)
            except:
                await self.bot.send_message(ctx.message.channel, _("파일을 찾지 못했어요!"))
                pass


def setup(bot):
    bot.add_cog(alohclass(bot))
