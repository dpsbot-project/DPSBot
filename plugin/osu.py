from osuapi import OsuApi, ReqConnector
import asyncio
from variables import osuapikey
import discord
from discord.ext import commands


class osuclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def 오스(self, ctx, *user):
        username = ''
        i = 0
        for word in user:
            i += 1
            if word == user[-1] and len(user) == i:
                username += str(word)
            else:
                username += str(word) + ' '
        api = OsuApi(osuapikey, connector=ReqConnector())
        results = api.get_user(username)
        userid = results[0].user_id
        thumbnail = "https://s.ppy.sh/a/" + str(userid)
        embed = discord.Embed(title="%s" % (username),
                            description="id:%s" % (userid), color=0xE0FFFF)
        embed.set_thumbnail(url=thumbnail)
        await self.bot.send_message(ctx.message.channel, embed=embed)
        await self.bot.send_message(ctx.message.channel, "https://osu.ppy.sh/users/%d" % userid)


def setup(bot):
    bot.add_cog(osuclass(bot))
