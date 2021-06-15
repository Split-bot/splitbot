from __future__ import annotations

import logging
import re

import discord
from discord.ext import commands
from discord.ext.commands import Context

from bot import SplitBot
from core.model import Expense, Item
from utils.math_eval import eval_expr

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
                "<@{}>: {}".format(
                    balance.user_value.user_id, balance.user_value.value
                )
            )
        if len(descriptions) == 0:
            description = "No outstanding debts."
        else:
            description = "\n".join(descriptions)
        embed = discord.Embed(title="Balances", description=description)
        await ctx.send(embed=embed)

    @staticmethod
    def _parse_item(line):
        words = line.split()
        item = Item()
        regex = re.compile(r"^<@(!)?(\d+)>$")
        has_price = False
        for word in words:
            match = regex.match(word)
            if match:
                user_id = match.group(2)
                item.user_ids.append(user_id)
                continue

            price = eval_expr(word)
            if price is not None:
                item.price = price
                has_price = True
                continue

            # otherwise ignore for now, assume item name

        if not has_price:
            raise ValueError("No price detected")
        return item

    @commands.command()
    async def expense(
        self,
        ctx: Context,
        payer: discord.Member,
        total_price: float,
        *,
        args=None,
    ):
        if not args:
            raise ValueError("No items detected")
        lines = args.splitlines()
        items = list(map(self._parse_item, lines))
        expense, status = Expense.from_items(
            str(ctx.guild.id), str(payer.id), total_price, items
        )
        descriptions = []
        for user_value in expense.user_values:
            descriptions.append(f"<@{user_value.user_id}>: {user_value.value}")
        tax = (status["scale"] - 1) * 100
        descriptions.append(f"Detected tax: {tax:.2f}%")
        embed = discord.Embed(
            title="Expense", description="\n".join(descriptions)
        )
        await ctx.send(embed=embed)
        if not 0 <= tax <= 20:
            await ctx.send(
                embed=discord.Embed(
                    title="Warning",
                    description="Abnormal tax detected!",
                    color=0xED4245,
                )
            )
        await self.bot.db_client.add_expense_and_update_balance(expense)
        await ctx.send("Expense saved successfully.")

    @expense.error
    async def expense_handler(self, ctx: Context, error):
        await ctx.send("Anjing! {}".format(error))


def setup(bot: SplitBot):
    bot.add_cog(SplitCog(bot))
