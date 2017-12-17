from discord.ext import commands
import discord
import asyncio


class AutoDelete:
    def __init__(self, bot):
        self.bot = bot
        self.delete_after = 10

    async def on_message(self, message):
        if len(message.content) < 2 or message.channel.is_private:
            return

        msg = message.content
        server = message.server
        prefix = self.get_prefix(server, msg)

        if not prefix:
            return

        asyncio.ensure_future(self.safe_delete(message))

    async def safe_delete(self, message):
        try:
            await asyncio.sleep(self.delete_after)
            await self.bot.delete_message(message)
        except discord.NotFound:
            pass

    def get_prefix(self, server, msg):
        prefixes = self.bot.settings.get_prefixes(server)
        for p in prefixes:
            if msg.startswith(p):
                return p
        return None

    @commands.command()
    async def delay(self, args):
        self.delete_after = int(args)
        await self.bot.say("New delay " + str(self.delete_after) + "sec")


def setup(bot):
    bot.add_cog(AutoDelete(bot))
