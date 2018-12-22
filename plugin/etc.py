from discord.ext import commands
import asyncio
import discord
import random
from variables import doinglist, owner, doinglist, channel
from embed import Embed
import gettext
_ = gettext.gettext
class etcclass():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def 안녕(self, ctx):
        await self.bot.say(_("안녕하세요!"))


    @commands.command(pass_context=True)
    async def 블라인드(self, ctx):
        await self.bot.say(_("---------------블라인드 중입니다---------------"))
        await self.bot.say(_(".\n" * 50))
        await self.bot.say(_("---------------블라인드가 끝났습니다---------------"))

    @commands.command(pass_context=True)
    async def 귓속말(self, ctx):
        await self.bot.send_message(ctx.message.channel, _("DM을 봐주세요!"))
        await self.bot.send_message(ctx.message.author, _("저를 부르셨나요...?"))
        await self.bot.send_message(ctx.message.author, _("이제 눈치보지 마시고 마음껏 얘기해 주세요!"))


    @commands.command(pass_context=True)
    async def 죽어(self, ctx):
        await self.bot.send_message(ctx.message.channel, _('싫어요!'))


    @commands.command(pass_context=True)
    async def 닥쳐(self, ctx):
        await self.bot.send_message(ctx.message.channel, _('싫어요!'))


    @commands.command(pass_context=True)
    async def 헬로월드(self, ctx):
        await self.bot.send_message(ctx.message.channel, _('안녕하세요....DPS봇입니다!'))


    @commands.command(pass_context=True)
    async def 뭐해(self, ctx):
        random.shuffle(doinglist)
        await self.bot.send_message(ctx.message.channel, doinglist[0])


    @commands.command(pass_context=True)
    async def 찍어(self, ctx):
        await self.bot.send_message(ctx.message.channel, _('마피아 게임인가요...?!\n머리를 굴려서 특정 사용자를 찍을게요!\n'))
        list = []
        members = ctx.message.server.members
        for x in members:
            list.append(x.name)
        random.shuffle(list)
        member = list[0]
        mention = member
        await self.bot.send_message(ctx.message.channel, mention + _('\n님을 찍겠습니다☆'))


    @commands.command(pass_context=True)
    async def 내성위키(self, ctx):
        embed = Embed(
            title=_("내성위키"), description="https://naesung.tk", color=0xE0FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def 내가누구(self, ctx):
        embed = Embed(title=_("당신은 혹시..."), description=_("\n%s\n\n이신가요?!?!") %
                            ctx.message.author, color=0xE0FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    @commands.command(pass_context=True)
    async def 건의(self, ctx, msg):
        me = await self.bot.get_user_info(owner)
        channel = self.bot.get_channel(int(channel))
        mention = ctx.message.author.name
        await self.bot.send_message(channel, _('%s 님이 %s (이)라고 건의했습니다.') % mention, msg)
        await self.bot.send_message(me, _('소식이 있어요!\n %s 님이 %s (이)라고 건의했습니다.') % mention, msg)


def setup(bot):
    bot.add_cog(etcclass(bot))
