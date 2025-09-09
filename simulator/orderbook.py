from collections import deque  
from dataclasses import dataclass  
import time
from typing import Optional 

@dataclass
class Order:
    id : int
    side: str
    qty : float
    price: Optional[float]
    timestamp: float

@dataclass
class Trade:
    time : float
    buy_order_id: Optional[int]
    sell_order_id: Optional[int]
    price: float
    qty: float

class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.trades = []

    def add_limit_order(self, order: Order):
        book = self.bids if order.side == "buy" else self.asks 
        if order.price not in book:
            book[order.price] = deque()
        book[order.price].append(order)
  
    def best_bid(self):
        return max(self.bids.keys()) if self.bids else None

    def best_ask(self):
        return min(self.asks.keys()) if self.asks else None

    def mid_price(self):
        if self.best_bid() is not None and self.best_ask() is not None:
            return (self.best_bid() + self.best_ask()) / 2
        return None
 
    def spread(self):
        if self.best_bid() is not None and self.best_ask() is not None:
            return self.best_ask() - self.best_bid()
        return None
  
    def market_order(self, side: str , qty: float , timestamp: float):
        book = self.asks if side == "buy" else self.bids
        while qty > 0 and book:
            best_price = min(book.keys()) if side == "buy" else max(book.keys())
            level = book[best_price]
            best_order = level[0]

            trading_qty = min(qty, best_order.qty)
            qty -= trading_qty
            best_order.qty -= trading_qty

            self.trades.append(
                Trade(
                    time=timestamp,
                    buy_order_id=best_order.id if side == "sell" else None,
                    sell_order_id=best_order.id if side == "buy" else None,
                    price=best_price,
                    qty=trading_qty
                )
            )

            if best_order.qty == 0:
                level.popleft()
                if not level:
                    del book[best_price]

    
  
  



    



  

