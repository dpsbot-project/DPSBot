import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__)))))
import asyncio
from discord.ext import commands
from translate import trans
from trans_open import opentrans
from pluginlist import pluginlist
from variables import pluginfolder, gamerefresh
from server import serverlist


class transconfig():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="translate", pass_context=True, aliases=['번역'])
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

    @commands.command(name="changelang", pass_context=True, aliases=['언어변경'])
    async def changelang(self, ctx, lang=None):
        await self.bot.raw_send_message(ctx.message.channel, 'open translate language support: en, ko \nothers support translator.\nplease view google language code:\nhttps://developers.google.com/admin-sdk/directory/v1/languages')
        if lang == None:
            await self.bot.raw_send_message(ctx.message.channel, "please specify a language.")
        else:
            if lang == 'ko' or lang == 'ko_KR':
                serverlist.setlang(ctx.message.server.id, 'ko_KR')
                opentrans.set('ko_KR')
            elif lang == 'en' or lang == 'en_US':
                serverlist.setlang(ctx.message.server.id, 'en_US')
                opentrans.set('en_US')
            else:
                serverlist.setlang(ctx.message.server.id, lang)
                opentrans.set('en_US')
            for extension in pluginlist.get()['default']:
                try:
                    self.bot.unload_extension("plugin.default." + extension)
                    self.bot.load_extension("plugin.default." + extension)
                    print(_("%s 확장 기능을 불러왔습니다.") % extension)
                except Exception as e:
                    print(_('%s 확장 기능을 불러오는데 실패했습니다.') % extension)
                    print(e)
                    pass
            await self.bot.say(_('%s로 변경되었습니다.') % lang)


def setup(bot):
    bot.add_cog(transconfig(bot))
