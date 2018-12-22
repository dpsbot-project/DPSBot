import hashlib
import asyncio
from discord.ext import commands

class gravatarclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=_("그라바타"), pass_context=True)
    async def gravatar(self, ctx, plaintext):
        h = hashlib.md5()
        h.update(plaintext.encode("utf-8").lower())
        encryptedtext = h.hexdigest()
        await self.bot.send_message(ctx.message.channel, encryptedtext)
        await self.bot.send_message(ctx.message.channel, "http://www.gravatar.com/avatar/" + encryptedtext)


def setup(bot):
    bot.add_cog(gravatarclass(bot))