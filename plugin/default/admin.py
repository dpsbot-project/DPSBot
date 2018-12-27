import asyncio
import psycopg2
import os
import discord
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__)))))
from pluginlist import pluginlist
from variables import owner, pluginfolder, instructions, gamename, prefix, DATABASE_URL
from embed import Embed
from discord.ext import commands

class adminclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load", hidden=True, pass_context=True)
    async def load(self, ctx, *modules):
        if ctx.message.author.id == owner:
            for module in modules:
                try:
                    if not module in pluginlist.get()["default"]:
                        pluginlist.append(module)
                        self.bot.load_extension(pluginfolder + module)
                        await self.bot.say(_('%s 모듈 로드 완료!') % module)
                    else:
                        await self.bot.say(_('이미 로드된 모듈입니다.'))
                except Exception as e:
                    await self.bot.say(_('오류 발생!\n%s') % e)
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))

    @commands.command(name="unload", hidden=True, pass_context=True)
    async def unload(self, ctx, *modules):
        if ctx.message.author.id == owner:
            for module in modules:
                if module == "admin":
                    await self.bot.say(_('어드민 모듈은 모듈을 로드하고 해제하는 기능이 있어, 해제가 불가능합니다.'))
                else:
                    try:
                        if module in pluginlist.get()["default"]:
                            self.bot.unload_extension(pluginfolder + module)
                            pluginlist.remove(module)
                            await self.bot.say(_('%s 모듈 해제 완료!') % module)
                        else:
                            await self.bot.say(_('이미 해제된 모듈입니다.'))
                    except Exception as e:
                        await self.bot.say(_('오류 발생!\n%s') % e)
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))

    @commands.command(name="reload", hidden=True, pass_context=True)
    async def reload(self, ctx, *modules):
        if ctx.message.author.id == owner:
            for module in modules:
                if module == "admin":
                    await self.bot.say(_('어드민 모듈은 모듈을 로드하고 해제하는 기능이 있어, 재로드가 불가능합니다.'))
                else:
                    try:
                        if not module in pluginlist.get()["default"]:
                            pluginlist.append(module)
                        self.bot.unload_extension(pluginfolder + module)
                        self.bot.load_extension(pluginfolder + module)
                        await self.bot.say(_('%s 모듈 재로드 완료!') % module)
                    except Exception as e:
                        await self.bot.say(_('오류 발생!\n%s') % e)
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))

    @commands.command(name="introducechange", aliases=["봇소개변경"], hidden=True, pass_context=True)
    async def introducechange(self, ctx, *, introduce=None):
        if ctx.message.author.id == owner:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            conn.autocommit = True
            cur = conn.cursor()
            sql = cur.mogrify("update settings set body = %s where name='instructions'", (introduce,))
            cur.execute(sql)
            conn.close()
            instructions.set(introduce)
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))

    @commands.command(name="addplaying", aliases=["플레이중추가"], hidden=True, pass_context=True)
    async def addplaying(self, ctx, *, playing=None):
        if ctx.message.author.id == owner:
            if playing != None:
                gamename.append(playing)
                await self.bot.say(_("%s가 추가되었습니다.") % playing)
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))

    @commands.command(name="deleteplaying", aliases=["플레이중삭제"], hidden=True, pass_context=True)
    async def addplaying(self, ctx, *, playing=None):
        if ctx.message.author.id == owner:
            if playing != None:
                gamename.list.remove(playing)
                await self.bot.say(_("%s가 삭제되었습니다.") % playing)
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))
            
    @commands.command(name="changeprefix", aliases=["접두사변경"], hidden=True, pass_context=True)
    async def changeprefix(self, ctx, *, change=None):
        if ctx.message.author.id == owner:
            conn = psycopg2.connect(DATABASE_URL)
            conn.autocommit = True
            cur = conn.cursor()
            sql = cur.mogrify("update settings set body = %s where name='prefix'", (change))
            cur.execute(sql)
            conn.close()
            prefix.set(change)
            await self.bot.say(_("%s로 접두사가 변경되었습니다.\n봇을 재시작시켜주세요.") % change)
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))

    @commands.command(name="deletecommand", aliases=["명령어삭제"], hidden=True, pass_context=True)
    async def deletecommand(self, ctx, *functions):
        if ctx.message.author.id == owner:
            embed = Embed(title=_(
                "**경고**"), description=_("현재 이 기능은 불안정하므로, 주의해서 사용하시길 바랍니다."), color=0xff0000)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            for function in functions:
                try:
                    self.bot.remove_command(function)
                    await self.bot.say(_("%s 명령어 삭제 완료.") % function)
                except Exception as e:
                    await self.bot.say(_("오류가 발생했습니다.") % function)
                    await self.bot.say(e)
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))

    @commands.command(name="restorecommand", aliases=["명령어복구"], hidden=True, pass_context=True)
    async def restorecommand(self, ctx, *functions):
        if ctx.message.author.id == owner:
            embed = Embed(title=_(
                "**경고**"), description=_("현재 이 기능은 불안정하므로, 주의해서 사용하시길 바랍니다."), color=0xff0000)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            for function in functions:
                try:
                    self.bot.add_command(function)
                    await self.bot.say(_("%s 명령어 복구 완료.") % function)
                except Exception as e:
                    await self.bot.say(_("오류가 발생했습니다.") % function)
                    await self.bot.say(e)
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))

    @commands.command(name=_("exit"), hidden=True, pass_context=True)
    async def exit(self, ctx):
        if ctx.message.author.id == owner:
            await self.bot.say(_('봇이 종료됩니다.'))
            sys.exit()
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))

    @commands.has_permissions(ban_members=True)
    async def ban(self, member: discord.Member, days: int = 1, *, reason):
        try:
            await self.bot.ban(member, days)
            await self.bot.say(_('%s 님이 %s님을 %s일간 밴하셨습니다.') % (message.author.name, member.name, days))
            await self.bot.say(_('이유:%s') % reason)
        except:
            await self.bot.say(_('밴 대상자가 없거나 봇에 밴 권한이 없습니다.'))

    @commands.command(kick_members=True)
    async def kick(self, member: discord.Member, *, reason):
        try:
            await self.bot.kick(member)
            await self.bot.say(_('%s 님이 %s님을 킥하셨습니다.') % (message.author.name, member.name))
        except:
            await self.bot.say(_('킥 대상자가 없거나 봇에 킥 권한이 없습니다.'))
    @commands.command(pass_context=True, hidden=True)
    async def serverlist(self, ctx):
        if ctx.message.author.id == owner:
            for server in self.bot.servers:
                await self.bot.say(_('서버 이름: %s 서버 id: %s 서버 인원: %s') % (server.name, server.id, len(server.members)))
        else:
            await self.bot.say(_('권한이 없습니다.\n봇 개발자만 사용 가능합니다.'))


def setup(bot):
    bot.add_cog(adminclass(bot))
