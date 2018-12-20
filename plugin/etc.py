from discord.ext import commands
import asyncio
import discord
import random
from variables import doinglist, owner, doinglist, channel

class etcclass():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def 안녕(self, ctx):
        await self.bot.say("안녕하세요!")


    @commands.command(pass_context=True)
    async def 블라인드(self, ctx):
        await self.bot.say("---------------블라인드 중입니다---------------")
        await self.bot.say(".\n" * 20)
        await self.bot.say("---------------블라인드가 끝났습니다---------------")

    @commands.command(pass_context=True)
    async def 귓속말(self, ctx):
        await self.bot.send_message(ctx.message.channel, "DM을 봐주세요!")
        await self.bot.send_message(ctx.message.author, "저를 부르셨나요...?")
        await self.bot.send_message(ctx.message.author, "이제 눈치보지 마시고 마음껏 얘기해 주세요!")


    @commands.command(pass_context=True)
    async def 도움(self, ctx):
        await self.bot.say("DM을 봐주세요!")
        await self.bot.send_message(ctx.message.author,
                            "설명입니다.\n\n디피 안녕\nDPS봇이 인사합니다.\n\n디피 귓속말\nDPS봇이 DM을 합니다. 명령어를 사용하실 수 있습니다.\n\n"
                            "디피 로그켜\n봇이 로깅을 시작합나다.\n\n디피 전해줘 (멘션) (내용)\n특정 사용자에게 DM을 대신 보내줍니다.\n\n디피 익명 (16자리 ID)\n익명으로 DM을 대신 보내줍니다.\n\n디피 답장 (암호)\n익명으로 온 DM에 답장합니다."
                            "\n\n디피 아카이브 (url)\nDPS봇이 아카이브를 떠줘요! 사진과 url로 저장된답니다!\n주의:아카이브의 모든 책임은 본인에게 있답니다."
                            "\n\n디피 maketag (제목) (내용)\n태그를 만듭니다. 디피 t제목을 입력하면 실행됩니다. 디피스크립트 가이드: https://gist.github.com/DPS0340/fa7d1e1333e6c5bcabcc0c5cd03003f5"
                            "\n\n종료\nDM을 종료합니다."
                            )

    @commands.command(pass_context=True)
    async def 죽어(self, ctx):
        await self.bot.send_message(ctx.message.channel, '싫어요!')


    @commands.command(pass_context=True)
    async def 닥쳐(self, ctx):
        await self.bot.send_message(ctx.message.channel, '싫어요!')


    @commands.command(pass_context=True)
    async def 헬로월드(self, ctx):
        await self.bot.send_message(ctx.message.channel, '안녕하세요....DPS봇입니다!')


    @commands.command(pass_context=True)
    async def 뭐해(self, ctx):
        random.shuffle(doinglist)
        await self.bot.send_message(ctx.message.channel, doinglist[0])


    @commands.command(pass_context=True)
    async def 찍어(self, ctx):
        await self.bot.send_message(ctx.message.channel, '마피아 게임인가요...?!\n머리를 굴려서 특정 사용자를 찍을게요!\n')
        list = []
        members = ctx.message.server.members
        for x in members:
            list.append(x.name)
        random.shuffle(list)
        member = list[0]
        mention = member
        await self.bot.send_message(ctx.message.channel, mention + '\n님을 찍겠습니다☆')


    
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
    async def 내성위키(self, ctx):
        embed = discord.Embed(
            title="내성위키", description="https://naesung.tk", color=0xE0FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def 내가누구(self, ctx):
        embed = discord.Embed(title="당신은 혹시...", description="\n%s\n\n이신가요?!?!" %
                            ctx.message.author, color=0xE0FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    @commands.command(pass_context=True)
    async def 건의(self, ctx, msg):
        me = await self.bot.get_user_info(owner)
        channel = self.bot.get_channel(channel)
        mention = ctx.message.author.name
        await self.bot.send_message(channel, '%s 님이 ' % (mention) + msg + ' (이)라고 건의했습니다.')
        await self.bot.send_message(me, '존경하는 주인님♡\n소식이 있어요!\n %s 님이 ' % (mention) + msg + ' (이)라고 건의했습니다.')


def setup(bot):
    bot.add_cog(etcclass(bot))
