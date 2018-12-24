import asyncio
from discord.ext import commands
from translate import trans
from trans_open import opentrans
from pluginlist import lst
from variables import pluginfolder, gamerefresh
import server
class transconfig():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=_("번역"), pass_context=True)
    async def translate(self, ctx, src, dest):
        await self.bot.say(_('번역할 내용을 말해주세요.'))
        plaintext = await self.bot.wait_for_message(author=ctx.message.author)
        if plaintext:
            try:
                await self.bot.raw_send_message(ctx.message.channel, trans.temprun(plaintext.content, src, dest))
            except:
                await self.bot.say(_('잘못된 언어코드입니다.'))
        else:
            await self.bot.say(_('내용이 없습니다.'))

    @commands.command(name="changelang", pass_context=True, aliases=[_('언어변경')])
    async def changelang(self, ctx, lang):
        if lang == 'ko' or lang == 'ko_KR:
            trans.setlang('ko_KR')
            opentrans.refresh()
            gamerefresh()
        elif lang == 'en' lang == 'en_US':
            trans.setlang('en_US')
            opentrans.refresh()
            gamerefresh()
        else:
            trans.setlang(lang)
            opentrans.set('en_US')
            gamerefresh()
        for extension in lst:
            try:
                self.bot.unload_extension(pluginfolder + extension)
                self.bot.load_extension(pluginfolder + extension)
                print(_("%s 확장 기능을 불러왔습니다.") % extension)
            except Exception as e:
                print(_('%s 확장 기능을 불러오는데 실패했습니다.') % extension)
                print(e)
                pass
        await self.bot.say(_('%s로 변경되었습니다.') % lang)


def setup(bot):
    bot.add_cog(transconfig(bot))

