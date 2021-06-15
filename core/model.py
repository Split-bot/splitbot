from dataclasses import dataclass
from typing import List

from odmantic import Field, Model


class Balance(Model):
    guild_id: str
    user_id: str
    value: float = Field(default=0.0)


@dataclass
class Item:
    price: float
    user_ids: List[int]


class Expense(Model):
    guild_id: str
    balances: List[Balance]

    @classmethod
    def from_items(cls, guild_id: int, items: List[Item]):
        user_expense = {}
        for item in items:
            if not item.user_ids:
                raise ValueError("An item has an empty user list")
            price_per_user = item.price / len(item.user_ids)
            for user_id in item.user_ids:
                if user_id not in user_expense:
                    user_expense[user_id] = 0.0
                user_expense[user_id] += price_per_user

        balances = [
            Balance(guild_id=guild_id, user_id=user_id, balance=balance)
            for user_id, balance in user_expense.items()
        ]
        return cls(guild_id=guild_id, balances=balances)
