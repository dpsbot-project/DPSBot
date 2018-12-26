
import asyncio
import telnetlib
import subprocess
import discord
from variables import owner
from discord.ext import commands
from embed import Embed


class execclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def print(self, ctx):
        await self.bot.say(ctx.message.content)

    @commands.command(name="exec", aliases=["실행"], pass_context=True)
    async def exec(self, ctx, *, command):
        if ctx.message.author.id == owner:
            try:
                result = subprocess.check_output(command, shell=True)
                embed = Embed(title=_("명령어 실행: %s") % (
                    plaintext), description="%s" % (result.decode('ascii')), color=0xE0FFFF)
                await self.bot.send_message(ctx.message.channel, embed=embed)
            except:
                await self.bot.send_message(ctx.message.channel, _('오류가 발생했습니다!'))
        else:
            await self.bot.send_message(ctx.message.channel, _('권한이 없습니다!\n개발자만 접근 가능합니다.'))

    @commands.command(name="telnet", aliases=["텔넷"], pass_context=True)
    async def telnet(self, ctx, host: str, port: int):
        telnet = telnetlib.Telnet(host, port)
        await self.bot.send_message(ctx.message.channel, _('%s:%s에 연결 중...') % (host, port))
        while True:
            body = await self.bot.wait_for_message(timeout=60.0, author=ctx.message.author)
            if body is None:
                await self.bot.send_message(ctx.message.channel, _('응답이 없어서 종료되었습니다.'))
                break
            else:
                if body.content.startswith(_('종료')):
                    await self.bot.send_message(ctx.message.channel, _('종료되었습니다.'))
                    break
                else:
                    try:
                        line = body.content + "\n"
                        telnet.write(line.encode('ascii'))
                        await asyncio.sleep(1)
                        response = telnet.read_very_eager()
                        embed = Embed(title="%s:%s" % (host, port), description="%s" % (
                            response.decode('ascii')), color=0xE0FFFF)
                        await self.bot.send_message(ctx.message.channel, embed=embed)
                    except:
                        await self.bot.send_message(ctx.message.channel, _('오류가 발생했습니다!'))
                        return


def setup(bot):
    bot.add_cog(execclass(bot))
