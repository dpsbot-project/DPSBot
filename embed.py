from translate import trans
from discord.ext import commands
import asyncio
import discord

class Embedtrans(discord.embeds):
    def __init__(self, **kwargs):
        # swap the colour/color aliases
        try:
            colour = kwargs['colour']
        except KeyError:
            colour = kwargs.get('color', EmptyEmbed)

        self.colour = colour
        self.title = trans.gettext(kwargs.get('title', EmptyEmbed))
        self.type = kwargs.get('type', 'rich')
        self.url = kwargs.get('url', EmptyEmbed)
        self.description = trans.gettext(kwargs.get('description', EmptyEmbed))

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
            self._footer['text'] = trans.gettext(str(text))

        if icon_url is not EmptyEmbed:
            self._footer['icon_url'] = str(icon_url)

        return self

        def add_field(self, *, name, value, inline=True):
        """Adds a field to the embed object.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        name: str
            The name of the field.
        value: str
            The value of the field.
        inline: bool
            Whether the field should be displayed inline.
        """

        field = {
            'inline': inline,
            'name': trans.gettext(str(name)),
            'value': trans.gettext((str(value)))
        }

Embed = Embedtrans()