from __future__ import annotations

import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context

from bot import SplitBot
from core.model import Expense

logger = logging.getLogger(__name__)


class SplitCog(commands.Cog):
    def __init__(self, bot: SplitBot):
        self.bot = bot

    @commands.command()
    async def ampz(self, ctx):
        await ctx.send("{} w0t".format(ctx.author.mention))

    @commands.command()
    async def balance(self, ctx: Context):
        balances = await self.bot.db_client.get_balance(ctx.guild.id)
        descriptions = []
        for balance in balances:
            descriptions.append(
                "<@{}>: {}".format(balance.user_id, balance.value)
            )
        if len(descriptions) == 0:
            description = "No outstanding debts."
        else:
            description = "\n".join(descriptions)
        embed = discord.Embed(title="Balances", description=description)
        await ctx.send(embed=embed)

    @commands.command()
    async def kaya(self, ctx: Context):
        await self.bot.db_client._add_balance(
            ctx.guild.id, ctx.author.id, 1000
        )
        await ctx.send(f"{ctx.author.mention} kaya sekarang")

    @commands.command()
    async def expense(
        self,
        ctx: Context,
        payer: discord.Member,
        total_price: float,
        *,
        args=None,
    ):
        expense, status = Expense.from_items(
            str(ctx.guild.id), str(payer.id), total_price, []
        )
        await ctx.send("{}, scale: {}".format(expense, status["scale"]))

    @expense.error
    async def expense_handler(self, ctx: Context, error):
        await ctx.send("Anjing {}".format(error))


def setup(bot: SplitBot):
    bot.add_cog(SplitCog(bot))
