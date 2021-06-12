import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class SplitCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ampz(self, ctx):
        await ctx.send("{} w0t".format(ctx.author.mention))

    @commands.command()
    async def balance(self, ctx):
        balances = await self.bot.db_client.get_balance(ctx.guild.id)
        descriptions = []
        for balance in balances:
            user_id = balance["user_id"]
            value = balance["value"]
            descriptions.append("<@{}>: {}".format(user_id, value))
        if len(descriptions) == 0:
            description = "No outstanding debts."
        else:
            description = "\n".join(descriptions)
        embed = discord.Embed(title="Balances", description=description)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SplitCog(bot))
