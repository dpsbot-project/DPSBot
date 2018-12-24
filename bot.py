from translate import trans
from discord.ext import commands
import asyncio
from server import serverlist
from translate import trans
class DPSBot(commands.Bot):
    @asyncio.coroutine
    def send_message(self, destination, content=None, *, tts=False, embed=None):
        channel_id, guild_id = yield from self._resolve_destination(destination)
        content = trans.gettext_remote(str(content), serverlist.list[int(guild_id)]['language']) if content is not None else None
        
        if embed is not None:
            embed = embed.to_dict()

        data = yield from self.http.send_message(channel_id, content, guild_id=guild_id, tts=tts, embed=embed)
        channel = self.get_channel(data.get('channel_id'))
        message = self.connection._create_message(channel=channel, **data)
        return message
    @asyncio.coroutine
    def raw_send_message(self, destination, content=None, *, tts=False, embed=None):
        channel_id, guild_id = yield from self._resolve_destination(destination)

        content = str(content) if content is not None else None
        
        if embed is not None:
            embed = embed.to_dict()

        data = yield from self.http.send_message(channel_id, content, guild_id=guild_id, tts=tts, embed=embed)
        channel = self.get_channel(data.get('channel_id'))
        message = self.connection._create_message(channel=channel, **data)
        return message
