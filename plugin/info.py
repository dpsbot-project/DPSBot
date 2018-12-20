import asyncio
import psycopg2
from variables import owner, mod, instructions, gamename, prefix
from discord.ext import commands
import discord
import os
import sys
from datetime import date, datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
class infoclass():
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command
    async def 사용자정보(self, message):
        person = message.mentions[0].id
        person = await self.bot.get_user_info(person)
        name = person.name
        discriminator = person.discriminator
        avatar = person.avatar_url
        id = person.id
        embed = discord.Embed(title="%s#%s" % (
            name, discriminator), description="id:%s" % (id), color=0xE0FFFF)
        embed.set_thumbnail(url=avatar)
        await self.bot.send_message(message.channel, embed=embed)


    @commands.command(pass_context=True)
    async def 정보(self, ctx):
        ownername = await self.bot.get_user_info(owner)
        ownername = ownername.name
        modstring = ""
        for a_mod in mod:
            modname = await self.bot.get_user_info(a_mod)
            modname = modname.name
            if not a_mod == mod[-1]:
                modstring += modname + ", "
            else:
                modstring += modname
        users = 0
        for s in self.bot.servers:
            users += len(s.members)
        now = datetime.now().date()
        dday = date(2018, 8, 6)
        result = now - dday
        embed=discord.Embed(title="%s 정보" % self.bot.user.name, description=instructions.get(), color=0x1ef7fa)
        embed.set_image(url=self.bot.user   .avatar_url)
        embed.add_field(name="봇 운영자", value=ownername, inline=True)
        embed.add_field(name="봇 부운영자", value=modstring, inline=True)
        embed.add_field(name="서버 수", value=len(self.bot.servers), inline=True)
        embed.add_field(name="사용자 수", value=users, inline=True)
        embed.add_field(name="접두사", value=prefix.get(), inline=True)
        embed.add_field(name="지금 플레이 중", value="%s 플레이 중\n" % gamename.get(), inline=True)
        embed.add_field(name="DPSBot의 나이", value="최초 공개로부터 " + str(result.days) + "일 지났습니다.", inline=True)
        embed.set_footer(text="Powered by Team ttakkku")
        await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(infoclass(bot))