import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class SplitCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ampz(self, ctx):
        await ctx.send("w0t")


def setup(bot):
    bot.add_cog(SplitCog(bot))
