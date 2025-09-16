from collections import deque
from dataclasses import dataclass
import time
import heapq
from typing import Optional, Dict, Deque, List, Tuple
import numpy as np

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
        timestamp = timestamp if timestamp is not None else time.time()
        order = Order(id=self.next_order_id, side=side, qty=qty, price=price, timestamp=timestamp)
        self.next_order_id += 1
        book = self.bids if side == "buy" else self.asks
        if price not in book:
            book[price] = deque()
            self.push_price(side, price)
        book[price].append(order)
        self.order_index[order.id] = (side, price)
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

    def market_order(self, side: str, qty: float, timestamp: Optional[float] = None) -> Order:
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
                self.order_index.pop(maker.id, None)
                level.popleft()
                if not level:
                    del book[best_price]
        return order

    def cancel_order(self, order_id: int) -> bool:
            info = self.order_index.get(order_id, None)
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
            self.order_index.pop(order_id, None)
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

class MarketSim:
    def __init__(self, order_book, lam=50, seed=None, p_market=0.3):
        self.order_book = order_book
        self.lam = lam
        self.rng = np.random.default_rng(seed)
        self.p_market = p_market

    def simulate(self, T=100, mid0=100.0):
        n_orders = self.rng.poisson(self.lam * T)
        interv_arrivals = self.rng.exponential(scale=1/self.lam, size=n_orders)
        arrival_times = np.cumsum(interv_arrivals)
        for t in arrival_times:
            mid = self.order_book.mid_price() or mid0
            side = self.rng.choice(["buy", "sell"])
            qty = max(1, self.rng.exponential(scale=5))
            if self.rng.random() < self.p_market:
                if side == "buy" and self.order_book.best_ask() is not None:
                    self.order_book.market_order("buy", qty, timestamp=t)
                elif side == "sell" and self.order_book.best_bid() is not None:
                    self.order_book.market_order("sell", qty, timestamp=t)
            else:
                price = max(1, self.rng.normal(mid, 1))
                self.order_book.add_limit_order(side, qty, price, timestamp=t)
        return self.order_book

class Strategy:
    def __init__ (self, order_book):
        self.order_book = order_book
        self.cash = 0.0
        self.inventory = 0.0
        self.active_orders = []      
        self.pnl_history = []       
        self.inventory_history = []   
        self.trade_history = []

    def quote(self, t):
        return []

    def update(self, trades):
        executed_orders = set()
        for trade in trades:
            if trade.maker_order_id in self.active_orders:
                qty = trade.qty
                price = trade.price
                if trade.taker_side == "buy":  
                    self.inventory -= qty
                    self.cash += qty * price
                else:  
                    self.inventory += qty
                    self.cash -= qty * price
                self.trade_history.append(trade)
                executed_orders.add(trade.maker_order_id)
            elif trade.taker_order_id in self.active_orders:
                qty = trade.qty
                price = trade.price
                if trade.taker_side == "buy":
                    self.inventory += qty
                    self.cash -= qty * price
                else:
                    self.inventory -= qty
                    self.cash += qty * price
                self.trade_history.append(trade)
                executed_orders.add(trade.taker_order_id)
        self.active_orders = [oid for oid in self.active_orders if oid not in executed_orders]

    def record_metrics(self, mid_price):
        PnL = self.cash + self.inventory * mid_price
        self.pnl_history.append(PnL)
        self.inventory_history.append(self.inventory)

class AvellanedaStoikovStrategy(Strategy):
    def __init__(self, order_book, sigma, gamma, k, order_size):
        super().__init__(order_book)
        self.sigma = sigma
        self.gamma = gamma
        self.k = k
        self.order_size = order_size
        self.last_quotes = (None, None)

    def compute_quotes(self, mid_price):
        delta_inventory = self.gamma * self.sigma**2 * self.inventory
        spread = (1/self.gamma) * np.log(1 + self.gamma/self.k)
        bid = mid_price - delta_inventory - spread/2
        ask = mid_price - delta_inventory + spread/2
        return bid, ask

    def quote(self, t=None):
        mid_price = self.order_book.mid_price()
        if mid_price is None:
            return
        bid, ask = self.compute_quotes(mid_price)
        if self.last_quotes[0] is None or abs(bid - self.last_quotes[0]) > 0.01:
            for oid in [oid for oid in self.active_orders if oid in self.order_book.order_index]:
                self.order_book.cancel_order(oid)
            self.active_orders = []
            if bid > 0:
                order_buy = self.order_book.add_limit_order("buy", self.order_size, bid)
                self.active_orders.append(order_buy.id)
        if self.last_quotes[1] is None or abs(ask - self.last_quotes[1]) > 0.01:
            if ask > 0:
                order_sell = self.order_book.add_limit_order("sell", self.order_size, ask)
                self.active_orders.append(order_sell.id)
        self.last_quotes = (bid, ask)
