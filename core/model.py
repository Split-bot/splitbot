from typing import List
from types import SimpleNamespace


class DictConvertable(SimpleNamespace):
    @classmethod
    def from_dict(cls, obj):
        return super(obj)

class Balance(DictConvertable):
    def init(self, guild_id: int, user_id: int, balance: float):
        self.guild_id = guild_id
        self.user_id = user_id
        self.balance = balance

class Item(DictConvertable):
    def init(self, price: float, user_ids: List[int]):
        self.price = price
        self.user_ids = user_ids
        
    
class Expense(DictConvertable):
    def init(self, guild_id: int, items: List[Item]):
        user_expense = {}
        for item in items:
            price_per_user = item.price / len(item.user_ids)
            for user_id in item.user_ids:
                if user_id not in user_expense:
                    user_expense[user_id] = 0.
                user_expense[user_id] += price_per_user
        
        self.balances = [Balance(guild_id, user_id, balance) for user_id, balance in user_expense.items()]
        
a = Balance()
a.__dir__
            
# Format: 
# item_price @user1 @user2 ... 
