# Market Making and Multi-Agent Simulation

Simulation of market making strategies in financial markets, focusing on quantitative trading algorithms.

## Key Objects

- Develop a realistic **Limit Order Book (LOB) simulator** capable of limit and market orders.
- Implement classical **market making** strategies such as **Avellaneda-Stoikov** with proper inventory and risk managment.
  > "Market making is fundamentally about providing liquidity while controlling inventory risk."  
  > — *Avellaneda & Stoikov, 2008*

- Enable **multi-agents simulations** to observe interactions between different strategies and studie their impact on market dynamics
- Provide a fundation for incorporating **Machine Learnign agents** to act as autonomus market participants that adapt and learn from market conditions
  > "Reinforcement learning and adaptive agents are becoming increasingly relevant in algorithmic trading."  
  > — *Cartea, Jaimungal & Penalva, 2015*

## Features 

- **Flexible LOB** it supports market and limit orders incluing timestamps and unique ID's
- **Avellaneda-Stoikov** classical risk-averse market making
- **Multi-Agent** Having different agents that operate over the same market concluding in the evaluation of diferent startegies
- **Future ML Integration**: design a self-learning agent capable of operating in the market autonomously 

## Real World integration (Planned Modifications)

Making the simulator applicable for real-world trading

- **Market API's** incorporation and **Live Market Feeds** using Web-Socket for a lower latency
- Training ML agents with real-world data (**backtesting**) 
- Incorporating **risk management tools**: position limits, stop-loss, take-profit, capital allocation, slippage, and transaction costs
- Optimizing for **ultra-low latencie** to replicate HFT 
- Advanced Order Execution
- Monitoring and Loggin

## Future Work
- Expand the simulator with additional **quantitative strategies**
- Integrate **deep reinforcement learning agents** to act as adaptive market participants.
- Conduct **stress tests** and **scenario analysis** to evaluate strategy robustness
