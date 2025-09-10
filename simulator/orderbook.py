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
    taker_order_id: Optional[int]
    maker_order_id: Optional[int]
    price: float
    qty: float
    taker_side: str
    
class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.trades = []
        self.next_order_id = 1

    def add_limit_order(self, order: Order):
       
        order = Order(
            id = self.next_order_id,
            side = side,
            qty = qty,
            price = price,
            timestamp = timestamp
        )
        self.next_order_id += 1
        
        book = self.bids if order.side == "buy" else self.asks 
        if price not in book:
            book[price] = deque()
        book[price].append(order)
  
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
  
    def market_order(self, side: str, qty: float, timestamp: float):
    
        order = Order(
            id = self.next_order_id,
            side = side,
            qty = qty,
            price = None,  # market order no tiene precio
            timestamp = timestamp
        )
        self.next_order_id += 1
    
        book = self.asks if side == "buy" else self.bids
    
        while order.qty > 0 and book:
            best_price = min(book.keys()) if side == "buy" else max(book.keys())
            level = book[best_price]
            best_order = level[0]  # maker
    
            trading_qty = min(order.qty, best_order.qty)
    
            order.qty -= trading_qty
            best_order.qty -= trading_qty
    
            self.trades.append(
                Trade(
                    time = timestamp,
                    price = best_price,
                    qty = trading_qty,
                    taker_order_id = order.id,
                    maker_order_id = best_order.id,
                    taker_side = side
                )
            )
    
            if best_order.qty == 0:
                level.popleft()
                if not level:
                    del book[best_price]

    def cancel_order(self,order_id: int) -> bool:
        for book in [self.bids, self.asks]:
            for price, level in list(book.items()):
                for order in list(level):
                    if order.id == order_id:
                        level.remove(order)
                        if not level:
                            del book[price]
                        return True
        return False

    def depth(self, n:int):
        result = { "bids":[] , "asks":[]}

        for price in sorted(self.bids.keys(), reverse= True)[:n]:
            qty_total1 = sum(order.qty for order in self.bids[price])
            result["bids"].append((price, qty_total1))
        for price in sorted(self.asks.keys())[:n]:
            qty_total2 = sum(order.qty for order in self.asks[price])
            result["asks"].append((price, qty_total2))
        print(result)
        


  

