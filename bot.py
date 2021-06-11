import logging
import os

import discord
from discord.ext import commands

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SplitBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.add_commands()

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        if message.author.bot:
            return

        print("Message from {0.author}: {0.content}".format(message))
        await message.channel.send(message.content)

        await self.process_commands(message)

    def add_commands(self):
        @self.command()
        async def ampz(ctx):
            print("ampz")
            await ctx.send("w0t")


def main():
    client = SplitBot()
    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
