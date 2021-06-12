import logging
import os
import sys
from typing import Union

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConfigurationError

logger = logging.getLogger(__name__)


class MongoDBClient:
    def __init__(self, bot):
        try:
            self.db = AsyncIOMotorClient(os.getenv("CONNECTION_URI")).splitbot
        except ConfigurationError as e:
            logger.critical(
                "Your MongoDB CONNECTION_URI might be copied wrong, "
                "try re-copying from the source again. "
                "Otherwise noted in the following message:"
            )
            logger.critical(e)
            sys.exit(0)

    async def get_balance(self, guild_id: Union[int, str]) -> list:
        return await self.db.balance.find({"guild_id": str(guild_id)}).to_list(
            None
        )
