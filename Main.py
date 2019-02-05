import discord
import asyncio
from tag import *
from variables import token, pluginfolder, gamename, prefix, owner
from pluginlist import pluginlist
from bot import DPSBot
import argparse
import sys
from server import serverlist, server_init
bot = DPSBot(command_prefix=prefix.get())


@bot.command(pass_context=True, name="maketag")
async def maketag(ctx, *, line):
    name = line.split()[0]
    try:
        await taginsert("tag", name, line.replace(name, "", 1))
        await bot.send_message(ctx.message.channel, _("태그 생성 완료!"))
        print("t!%s" % name)
        @bot.command(name="t%s" % name, pass_context=True)
        async def tag(ctx, *, inputline=""):
            await bot.send_message(ctx.message.channel, line.replace(name, "", 1))
            result = run(name, line.replace(name, "", 1), inputline)
            await bot.send_message(ctx.message.channel, result)
            print(name)
            print(result)
    except Exception as e:
        print(e)
        await bot.send_message(ctx.message.channel, _("이미 있는 태그입니다."))


@bot.command(pass_context=True, name="tag", aliases=["태그"])
async def tag(ctx):
    await bot.say("english guide:https://gist.github.com/DPS0340/8eb28271b75e4956717c7038ad57f528\nkorean guide:https://gist.github.com/DPS0340/fa7d1e1333e6c5bcabcc0c5cd03003f5")


def taginit(name, line):
    @bot.command(name="t%s" % name, pass_context=True)
    async def tag(ctx, *, inputline=""):
        await bot.send_message(ctx.message.channel, line)
        result = run(name, line, inputline)
        await bot.send_message(ctx.message.channel, result)
        print(name)
        print(result)


def tagload():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('select * from tag')
    rows = cur.fetchall()
    print(_('태그 로드중...'))
    print(_('------'))
    for row in rows:
        try:
            name = row[0]
            line = row[1]
            taginit(name, line)
            print(line)
        except Exception as e:
            print(_('태그 로드 실패!'))
            print(e)
            pass
    conn.close()
    print(_('------'))
    print(_('태그 로드 완료!'))

@bot.event
async def on_ready():
    tagload()
    print(_('로그인 되었습니다.'))
    print(_('------'))
    print(bot.user.name)
    print(bot.user.id)
    print(_('------'))
    server_init(bot)
    serverlist.reload()
    if args.test == True:
        sys.exit()
    bot.loop.create_task(splash_rotate())


@bot.event
async def on_guild_join(guild):
    serverlist.reload()


async def splash_rotate():
    while True:
        splashes = gamename.get()
        for splash in splashes:
            await bot.change_presence(game=discord.Game(name=splash))
            await asyncio.sleep(2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-test', help='exit after ready', action='store_true')
    parser.set_defaults(test=False)
    global args
    args = parser.parse_args()
    print(_("------"))
    print(pluginlist.get()['default'])
    for extension in pluginlist.get()['default']:
        try:
            bot.load_extension(pluginfolder + extension)
            print(_("%s 확장 기능을 불러왔습니다.") % extension)
        except Exception as e:
            print(_('%s 확장 기능을 불러오는데 실패했습니다.') % extension)
            print(e)
            raise
    print(_("------"))
    bot.run(token)
