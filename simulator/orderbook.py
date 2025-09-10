from collections import deque
from dataclasses import dataclass
import time
import heapq
from typing import Optional, Dict, Deque, List, Tuple

@dataclass
class Order:
    id: int
    side: str                
    qty: float
    price: Optional[float]   
    timestamp: float

@dataclass
class Trade:
    time: float
    taker_order_id: Optional[int]
    maker_order_id: Optional[int]
    price: float
    qty: float
    taker_side: str

class OrderBook:
    def __init__(self):
        
        self.bids: Dict[float, Deque[Order]] = {}
        self.asks: Dict[float, Deque[Order]] = {}

        
        self.trades: List[Trade] = []

        
        self.next_order_id: int = 1

        
        self.bid_heap: List[float] = []
        self.ask_heap: List[float] = []

        
        self.order_index: Dict[int, Tuple[str, Optional[float]]] = {}

    # ---------------- helper heap ----------------
    def push_price(self, side: str, price: float) -> None:
        if side == "buy":  
            heapq.heappush(self.bid_heap, -price)
        else:
            heapq.heappush(self.ask_heap, price)

    def clean_top_price(self, side: str) -> None:
        if side == "buy":
            while self.bid_heap:
                price = -self.bid_heap[0]         
                if price in self.bids and self.bids[price]:
                    break
                heapq.heappop(self.bid_heap)
        else:
            while self.ask_heap:
                price = self.ask_heap[0]
                if price in self.asks and self.asks[price]:
                    break
                heapq.heappop(self.ask_heap)

    def best_price_heap(self, side: str) -> Optional[float]:
        self.clean_top_price(side)
        if side == "buy":
            return -self.bid_heap[0] if self.bid_heap else None
        else:
            return self.ask_heap[0] if self.ask_heap else None

    def add_limit_order(self, side: str, qty: float, price: float, timestamp: Optional[float] = None) -> Order:
        assert side in ("buy", "sell")
        timestamp = timestamp if timestamp is not None else time.time()

        order = Order(id=self.next_order_id, side=side, qty=qty, price=price, timestamp=timestamp)
        self.next_order_id += 1

        book = self.bids if side == "buy" else self.asks
        is_new_level = price not in book
        if is_new_level:
            book[price] = deque()
        book[price].append(order)

        self.order_index[order.id] = (side, price)

        if is_new_level:
            self.push_price(side, price)

        return order

    def best_bid(self) -> Optional[float]:
        return self.best_price_heap("buy")

    def best_ask(self) -> Optional[float]:
        return self.best_price_heap("sell")

    def mid_price(self) -> Optional[float]:
        b = self.best_bid()
        a = self.best_ask()
        if b is None or a is None:
            return None
        return (a + b) / 2.0

    def spread(self) -> Optional[float]:
        b = self.best_bid()
        a = self.best_ask()
        if b is None or a is None:
            return None
        return a - b

    def market_order(self, side: str, qty: float, timestamp: Optional[float] = None) -> Order:
        assert side in ("buy", "sell")
        timestamp = timestamp if timestamp is not None else time.time()

        order = Order(id=self.next_order_id, side=side, qty=qty, price=None, timestamp=timestamp)
        self.next_order_id += 1

        book = self.asks if side == "buy" else self.bids

        while order.qty > 0 and book:
            best_price = self.best_ask() if side == "buy" else self.best_bid()
            if best_price is None:
                break
            level = book[best_price]
            maker = level[0]
            trade_qty = min(order.qty, maker.qty)

            order.qty -= trade_qty
            maker.qty -= trade_qty

            self.trades.append(Trade(
                time=timestamp,
                taker_order_id=order.id,
                maker_order_id=maker.id,
                price=best_price,
                qty=trade_qty,
                taker_side=side
            ))

            if maker.qty == 0:
                level.popleft()
                if not level:
                    del book[best_price]

        return order

    def cancel_order(self, order_id: int) -> bool:
        info = self.order_index.pop(order_id, None)
        if not info:
            return False
        side, price = info
        book = self.bids if side == "buy" else self.asks
        if price not in book:
            return False
        level = book[price]
        for o in list(level):
            if o.id == order_id:
                level.remove(o)
                break
        else:
            return False
        if not level:
            del book[price]

        return True

    def depth(self, n: int = 5):
        result = {"bids": [], "asks": []}
        for price in sorted(self.bids.keys(), reverse=True)[:n]:
            qty_total = sum(o.qty for o in self.bids[price])
            result["bids"].append((price, qty_total))
        for price in sorted(self.asks.keys())[:n]:
            qty_total = sum(o.qty for o in self.asks[price])
            result["asks"].append((price, qty_total))
        return result
        


  

