import discord
import asyncio
from variables import token, pluginfolder, gamename, prefix, owner
from pluginlist import pluginlist
from bot import DPSBot
import argparse
import sys
from server import serverlist, server_init
bot = DPSBot(command_prefix=prefix.get())
@bot.event  
async def on_ready():
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
    for key in pluginlist.get().keys():
        try:
            for extension in pluginlist.get().get(key):
                bot.load_extension(pluginfolder + key + "/" + extension)
                print(_("%s 확장 기능을 불러왔습니다.") % extension)
        except Exception as e:
            print(_('%s 확장 기능을 불러오는데 실패했습니다.') % extension)
            print(e)
            raise
    print(_("------"))
    bot.run(token)
