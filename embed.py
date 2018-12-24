from translate import trans
from discord.ext import commands
import asyncio
import discord
from discord.embeds import EmptyEmbed
class Embed(discord.embeds.Embed):
    def __init__(self, **kwargs):
        # swap the colour/color aliases
        try:
            colour = kwargs['colour']
        except KeyError:
            colour = kwargs.get('color', EmptyEmbed)

        self.colour = colour
        self.title = trans.gettext_remote(kwargs.get('title', EmptyEmbed), serverlist.list[int(guild_id)]['language'])
        self.type = kwargs.get('type', 'rich')
        self.url = kwargs.get('url', EmptyEmbed)
        self.description = trans.gettext_remote(kwargs.get('description', EmptyEmbed), serverlist.list[int(guild_id)]['language'])

        try:
            timestamp = kwargs['timestamp']
        except KeyError:
            pass
        else:
            self.timestamp = timestamp

    def set_footer(self, *, text=EmptyEmbed, icon_url=EmptyEmbed):
        """Sets the footer for the embed content.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        text: str
            The footer text.
        icon_url: str
            The URL of the footer icon. Only HTTP(S) is supported.
        """

        self._footer = {}
        if text is not EmptyEmbed:
            self._footer['text'] = trans.gettext_remote((str(text)), serverlist.list[int(guild_id)]['language'])

        if icon_url is not EmptyEmbed:
            self._footer['icon_url'] = str(icon_url)

        return self

    def add_field(self, *, name, value, inline=True):
        field = {
            'inline': inline,
            'name': trans.gettext_remote(((str(name))), serverlist.list[int(guild_id)]['language']),
            'value': trans.gettext_remote(((str(value))), serverlist.list[int(guild_id)]['language'])
        }

        try:
            self._fields.append(field)
        except AttributeError:
            self._fields = [field]

        return self
