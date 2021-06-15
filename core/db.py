import logging
import os
import sys
from typing import Union

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from pymongo.errors import ConfigurationError

from core.model import Balance

logger = logging.getLogger(__name__)


class MongoDBClient:
    def __init__(self, bot):
        self.bot = bot
        try:
            self.client = AsyncIOMotorClient(os.getenv("CONNECTION_URI"))
        except ConfigurationError as error:
            logger.critical(
                "Your MongoDB CONNECTION_URI might be copied wrong, "
                "try re-copying from the source again. "
                "Otherwise noted in the following message:"
            )
            logger.critical(error)
            sys.exit(0)

        self.engine = AIOEngine(motor_client=self.client, database="splitbot")

    async def get_balance(self, guild_id: Union[int, str]) -> list:
        return await self.engine.find(
            Balance, Balance.guild_id == str(guild_id)
        )

    async def add_balance(
        self,
        guild_id: Union[int, str],
        user_id: Union[int, str],
        added_value: float,
    ) -> None:
        balance = await self.engine.find_one(
            Balance,
            (Balance.guild_id == str(guild_id))
            & (Balance.user_id == str(user_id)),
        )
        if balance is None:
            balance = Balance(guild_id=guild_id, user_id=user_id)
        balance.value += added_value
        await self.engine.save(balance)
