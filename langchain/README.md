# LangChain Integration (Python)

This example shows how to give a LangChain agent access to the CryptoRetail API using the x402 protocol.

### Prerequisites

```bash
pip install langchain langchain-openai x402-client
```

You will need a wallet private key funded with USDC on Base or Solana mainnet to pay the $0.02 per-query fee.

### Example Code

See `agent.py` for the complete working example.

```python
import os
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from x402.client import X402Client
from x402.mechanisms.evm.exact import ExactEvmClientScheme
import requests

# 1. Initialize the x402 client with your wallet
client = X402Client()
client.register("eip155:8453", ExactEvmClientScheme(os.environ["EVM_PRIVATE_KEY"]))

# 2. Define the tool wrapper
def calculate_crypto_return(query: str) -> str:
    # LangChain passes a single string; in production you'd parse this into symbol/amount/date
    symbol, amount, date = query.split(",")
    
    # The client automatically handles the 402 payment challenge
    response = client.get(
        "https://api.cryptoretail.store/v1/calculate",
        params={"symbol": symbol.strip(), "amount": amount.strip(), "date": date.strip()}
    )
    return response.text

# 3. Create the LangChain tool
crypto_tool = Tool(
    name="calculate_crypto_return",
    func=calculate_crypto_return,
    description="Calculates historical crypto investment returns. Input must be a comma-separated string: symbol, amount, YYYY-MM-DD date. Example: 'BTC, 1000, 2021-07-26'"
)

# 4. Run the agent
llm = ChatOpenAI(temperature=0)
agent = initialize_agent([crypto_tool], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.run("What would $1000 invested in SOL on 2022-01-01 be worth today?")
```
