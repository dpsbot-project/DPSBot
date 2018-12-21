import asyncio
from discord.ext import commands
from translate import trans

class transconfig():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def 번역(self, ctx, src, dest):
        await self.bot.say('번역할 내용을 말해주세요.')
        plaintext = await self.bot.wait_for_message(author=ctx.message.author)
        if plaintext:
            try:
                await self.bot.say(trans.temprun(plaintext.content, src, dest))
            except:
                await self.bot.say('잘못된 언어코드입니다.')
        else:
            await self.bot.say('내용이 없습니다.')

    @commands.command(pass_context=True)
    async def 언어변경(self, ctx, lang):
        trans.setlang(lang)
        await self.bot.raw_send_message(ctx.message.author, '%s로 변경되었습니다.' % lang)


def setup(bot):
    bot.add_cog(transconfig(bot))

