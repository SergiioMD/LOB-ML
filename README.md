# Market Making and Multi-Agent Simulation

Simulation of market making strategies in financial markets, focusing on quantitative trading algorithms.

## Key Objects

- Develop a realistic **limit order book simulatior** capable of limit and market orders.
- Implement classical **market making** strategies such as **Avellaneda-Stoikov** with proper inventory and risk managment.
  > "Market making is fundamentally about providing liquidity while controlling inventory risk."  
  > — *Avellaneda & Stoikov, 2008*

- Enable **multi-agents simulations** to observe interactions between different strategies and studie their impact on market dynamics
- Provide a fundation for incorporating **Machine Learnign agents** to act as autonomus market participants that adapt and learn from market conditions
  > "Reinforcement learning and adaptive agents are becoming increasingly relevant in algorithmic trading."  
  > — *Cartea, Jaimungal & Penalva, 2015*

## Features 

- **Flexible LOB(Limit Order Book)** it supports market and limit orders incluing time and ID'2
- **Avellaneda-Stoikov** Classical risk-averse market making
- **Multi-Agent** Having different agents that operate over the same market concluding in the evaluation of diferent startegies
- **Future ML Integration**: Designing a self-learning model that operates in the market as an agent

## Real World incoroporation Modifications
Looking forward to incorporate the model when it is more advanced to the real world, therefore here are some of the ongoing modifiactions
- Market API's incorporation, Live Market Feeds using Web-Socket for a lower latency
- Training ML agents with real World Data (**backtesting**) +
- Adding new strategies such as **position limits, Stop-Loss, Take-Profit, Capital Allocation, Slipapage and Transactions**
- Looking forward to having a Lower Latencie to be able to replicate HFT strategies
- Advanced Order Execution
- Monitoring and Loggin
