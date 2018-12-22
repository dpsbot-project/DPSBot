from translate import trans
from discord.ext import commands
import asyncio

class DPSBot(commands.Bot):
    def __init__(self):
        self.raw_send_message = self.send_message

    @asyncio.coroutine
    def send_message(self, destination, content=None, *, tts=False, embed=None):
        channel_id, guild_id = yield from self._resolve_destination(destination)

        content = trans.gettext(str(content)) if content is not None else None
        
        if embed is not None:
            embed = embed.to_dict()

        data = yield from self.http.send_message(channel_id, content, guild_id=guild_id, tts=tts, embed=embed)
        channel = self.get_channel(data.get('channel_id'))
        message = self.connection._create_message(channel=channel, **data)
        return message