import discord
import asyncio
from variables import token, pluginfolder, gamename, prefix, owner
from pluginlist import lst as initial_extensions
from bot import DPSBot
bot = DPSBot(command_prefix=prefix.get())
@bot.event
async def on_ready():
    print('로그인 되었습니다.')
    print('------')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.loop.create_task(splash_rotate())

async def splash_rotate():
    splashes = gamename.get()
    while True:
        for splash in splashes:
            await bot.change_presence(game=discord.Game(name=splash))
            await asyncio.sleep(2)


if __name__ == '__main__':
    print("------")
    for extension in initial_extensions:
        try:
            bot.load_extension(pluginfolder + extension)
            print("%s 확장 기능을 불러왔습니다." % extension)
        except Exception as e:
            print('%s 확장 기능을 불러오는데 실패했습니다.' % extension)
            print(e)
            pass
    print("------")
    bot.run(token)
