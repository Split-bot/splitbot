__version__ = "0.1.0"

import logging
import os
from datetime import datetime
from string import Formatter

import discord
from discord.ext import commands
from pkg_resources import parse_version

from core.db import MongoDBClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SplitBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # pylint: disable=assigning-non-slot
        self.prefix = "!"
        super().__init__(command_prefix=self.prefix, intents=intents)

        self._db_client = None
        self.loaded_cogs = ["cogs.splitcog", "cogs.utility"]
        self.start_time = datetime.utcnow()

        self.startup()

    @property
    def version(self):
        return parse_version(__version__)

    @property
    def uptime(self) -> str:
        now = datetime.utcnow()
        delta = now - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fmt = "{h}h {m}m {s}s"
        if days:
            fmt = "{d}d " + fmt

        return Formatter().format(fmt, d=days, h=hours, m=minutes, s=seconds)

    @property
    def db_client(self):
        if self._db_client is None:
            self._db_client = MongoDBClient(self)
        return self._db_client

    async def on_ready(self):
        logger.info("Logged on as %s!", self.user)

    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith(self.prefix):
            await self.process_commands(message)
            return

        logger.info("Message from %s: %s", message.author, message.content)
        await message.channel.send(message.content)

    def startup(self):
        logger.info("SplitBot v%s", __version__)

        for cog in self.loaded_cogs:
            logger.info("Loading %s.", cog)
            try:
                self.load_extension(cog)
                logger.info("Successfully loaded %s.", cog)
            except Exception:
                logger.exception("Failed to load %s.", cog)


def main():
    client = SplitBot()
    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
