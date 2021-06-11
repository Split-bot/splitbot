import os

import discord
from discord.ext import commands


class SplitBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix=None, intents=intents)  # implemented in `get_prefix`

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))
        if message.author == self.user:
            return
        await message.channel.send(message.content)


def main():
    client = SplitBot()
    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
