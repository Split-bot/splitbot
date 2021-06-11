import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uptime(self, ctx):
        await ctx.send(self.bot.uptime)

    @commands.command()
    async def about(self, ctx):
        await ctx.send(f"SplitBot v{self.bot.version}")


def setup(bot):
    bot.add_cog(Utility(bot))
