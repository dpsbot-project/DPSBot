import asyncio
import psycopg2
from variables import owner, mod, instructions, gamename, prefix
from discord.ext import commands
import discord
import os
import sys
from datetime import date, datetime
from embed import Embed
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
class infoclass():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="userinfo", pass_context=True, aliases=['사용자정보'])
    async def userinfo(self, ctx):
        person = ctx.message.mentions[0].id
        person = await self.bot.get_user_info(person)
        name = person.name
        discriminator = person.discriminator
        avatar = person.avatar_url
        id = person.id
        embed = Embed(title="%s#%s" % (
            name, discriminator), description="id:%s" % (id), color=0xE0FFFF)
        embed.set_thumbnail(url=avatar)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    @commands.command(name="info", pass_context=True, aliases=['정보'])
    async def info(self, ctx):
        ownername = await self.bot.get_user_info(owner)
        ownername = ownername.name
        modstring = ""
        for a_mod in mod:
            modname = await self.bot.get_user_info(a_mod)
            modname = modname.name
            modstring += modname + " "
        users = 0
        for s in self.bot.servers:
            users += len(s.members)
        now = datetime.now().date()
        dday = date(2018, 8, 6)
        result = now - dday
        embed=Embed(title=_("%s 정보") % self.bot.user.name, description=instructions.get(), color=0x1ef7fa)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name=_("봇 운영자"), value=ownername, inline=True)
        embed.add_field(name=_("봇 부운영자"), value=modstring, inline=True)
        embed.add_field(name=_("서버 수"), value=len(self.bot.servers), inline=True)
        embed.add_field(name=_("사용자 수"), value=users, inline=True)
        embed.add_field(name=_("접두사"), value=prefix.get(), inline=True)
        embed.add_field(name=_("DPSBot의 나이"), value=_("최초 공개로부터 %s일 지났습니다.") % str(result.days), inline=True)
        embed.set_footer(text=_("Powered by Team ttakkku"))
        await self.bot.send_raw_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(infoclass(bot))