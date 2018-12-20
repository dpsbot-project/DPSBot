from discord.ext import commands
import asyncio
import discord
from pluginlist import lst, alllst

class pluginclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def 모듈(self, ctx):
        i = 0
        body = ""
        for plugin in alllst:
            i += 1
            body += plugin + " "
            if i % 5 == 0:
                body += '\n'
        embed = discord.Embed(title="사용 가능한 모듈 리스트", description=body, color=0x00FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)
        i = 0
        body = ""
        for plugin in lst:
            i += 1
            body += plugin + " "
            if i % 5 == 0:
                body += '\n'
        embed = discord.Embed(title="현재 작동중인 모듈 리스트",
                              description=body, color=0xE0FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(pluginclass(bot))
