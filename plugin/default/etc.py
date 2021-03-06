from discord.ext import commands
import asyncio
import discord
import random
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__)))))
from variables import doinglist, owner, doinglist
from variables import channel as ticketchannel
from embed import Embed


class etcclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello", aliases=["안녕"], pats_context=True)
    async def hello(self, ctx):
        await self.bot.say(_("안녕하세요!"))

    @commands.command(name="blind", aliases=["블라인드"], pass_context=True)
    async def blind(self, ctx):
        await self.bot.say(_("---------------블라인드 중입니다---------------"))
        await self.bot.say(_(".\n") * 50)
        await self.bot.say(_("---------------블라인드가 끝났습니다---------------"))

    @commands.command(name="whisper", aliases=["귓속말"], pass_context=True)
    async def whisper(self, ctx):
        await self.bot.send_message(ctx.message.channel, _("DM을 봐주세요!"))
        await self.bot.send_message(ctx.message.author, _("저를 부르셨나요...?"))
        await self.bot.send_message(ctx.message.author, _("이제 눈치보지 마시고 마음껏 얘기해 주세요!"))

    @commands.command(name="die", aliases=["죽어"], pass_context=True)
    async def die(self, ctx):
        await self.bot.send_message(ctx.message.channel, _('싫어요!'))

    @commands.command(name="shutup", aliases=["닥쳐"], pass_context=True)
    async def shutup(self, ctx):
        await self.bot.send_message(ctx.message.channel, _('싫어요!'))

    @commands.command(name="helloworld", aliases=["헬로월드"], pass_context=True)
    async def helloworld(self, ctx):
        await self.bot.send_message(ctx.message.channel, _('안녕하세요....DPS봇입니다!'))

    @commands.command(name="doing", aliases=["뭐해"], pass_context=True)
    async def doing(self, ctx):
        random.shuffle(doinglist)
        await self.bot.send_message(ctx.message.channel, doinglist[0])

    @commands.command(name="random", aliases=["찍어"], pass_context=True)
    async def random(self, ctx):
        await self.bot.send_message(ctx.message.channel, _('마피아 게임인가요...?!\n머리를 굴려서 특정 사용자를 찍을게요!\n'))
        list = []
        members = ctx.message.server.members
        for x in members:
            list.append(x.name)
        random.shuffle(list)
        member = list[0]
        mention = member
        await self.bot.send_message(ctx.message.channel, mention + _('\n님을 찍겠습니다☆'))

    @commands.command(name="naesungwiki", aliases=["내성위키"], pass_context=True)
    async def naesungwiki(self, ctx):
        embed = Embed(
            title=_("내성위키"), description="https://naesung.wiki", color=0xE0FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(name="whoami", aliases=["내가누구"], pass_context=True)
    async def whoami(self, ctx):
        embed = Embed(title=_("당신은 혹시..."), description=_("\n%s\n\n이신가요?!?!") %
                      ctx.message.author, color=0xE0FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(name="ticket", aliases=["건의"], pass_context=True)
    async def ticket(self, ctx, *, msg):
        me = await self.bot.get_user_info(owner)
        channel = self.bot.get_channel(ticketchannel)
        mention = ctx.message.author.name
        await self.bot.send_message(channel, _('%s 님이 %s (이)라고 건의했습니다.') % (mention, msg))
        await self.bot.send_message(me, _('소식이 있어요!\n %s 님이 %s (이)라고 건의했습니다.') % (mention, msg))


def setup(bot):
    bot.add_cog(etcclass(bot))
