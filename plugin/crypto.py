import asyncio
from discord.ext import commands
from cryptography.fernet import Fernet


class cryptoclass():
    def __init__(self, bot):
        self.bot = bot
        privatekey = Fernet.generate_key()
        self.cipher_suite = Fernet(privatekey)

    @commands.command(pass_context=True)
    async def 암호화(self, ctx, *words):
        plaintext = ''
        i = 0
        for word in words:
            i += 1
            if word == words[-1] and len(words) == i:
                plaintext += str(word)
            else:
                plaintext += str(word) + ' '
        encryptedtext = self.cipher_suite.encrypt(plaintext.encode("utf-8")).decode()
        await self.bot.send_message(ctx.message.channel, encryptedtext)


    @commands.command(pass_context=True)
    async def 복호화(self, ctx, encryptedtext):
        plaintext = self.cipher_suite.decrypt(encryptedtext.encode("utf-8")).decode()
        await self.bot.send_message(ctx.message.channel, plaintext)


def setup(bot):
    bot.add_cog(cryptoclass(bot))
