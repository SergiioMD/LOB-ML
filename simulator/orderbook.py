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
  buy_order_id: int
  sell_order_id: int
  price: float
  qty: float

class OrderBook:
  def __init__(self):
    self.bids = {}
    self.asks = {}
    self.trades = []

  def add_limit_order(self, Order, order):
    book = self.bids if order.side == "buy" else self.asks 
    if order.price not in book:
      book[order.price] = deque()
    book[order.price].append(order)
  
  def best_bid(self):
    return max(self.bids.keys()) if self.bids else None

  def best_ask(self):
    return min(self.asks.keys()) if self.asks else None

ob = OrderBook()
ob.add_limit_order(Order(1, "buy", 10, 100.0, time.time()))
ob.add_limit_order(Order(2, "sell", 5, 101.0, time.time()))
print("Best bid:", ob.best_bid())
print("Best ask:", ob.best_ask())



  

