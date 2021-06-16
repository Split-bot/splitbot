from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Tuple

from odmantic import Field, Model
from odmantic.model import EmbeddedModel


class UserValue(EmbeddedModel):
    user_id: str
    value: float = Field(default=0.0)


class Balance(Model):
    guild_id: str
    user_value: UserValue


@dataclass
class Item:
    price: float = 0.0
    user_ids: List[str] = field(default_factory=list)


class Expense(Model):
    guild_id: str
    user_values: List[UserValue]

    @classmethod
    def from_items(
        cls,
        guild_id: str,
        payer_id: str,
        total_price: float,
        items: List[Item],
    ) -> Tuple[Expense, dict]:
        user_expense = defaultdict(float)
        subtotal_price = 0.0
        for item in items:
            if not item.user_ids:
                raise ValueError("An item has an empty user list")
            price_per_user = item.price / len(item.user_ids)
            for user_id in item.user_ids:
                user_expense[user_id] -= price_per_user
            subtotal_price += item.price

        user_expense[payer_id] += subtotal_price

        if math.isclose(subtotal_price, 0):
            raise ValueError("Zero subtotal")

        scale = total_price / subtotal_price

        user_values = [
            UserValue(user_id=user_id, value=value * scale)
            for user_id, value in user_expense.items()
        ]
        return cls(guild_id=guild_id, user_values=user_values), {
            "scale": scale
        }
