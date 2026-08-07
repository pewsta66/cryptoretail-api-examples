# CrewAI Integration (Python)

This example shows how to create a custom CrewAI tool that queries the CryptoRetail API using the x402 protocol.

### Prerequisites

```bash
pip install crewai langchain-openai x402-client
```

You will need a wallet private key funded with USDC on Base or Solana mainnet to pay the $0.02 per-query fee.

### Example Code

See `crew.py` for the complete working example.

```python
import os
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from x402.client import X402Client
from x402.mechanisms.evm.exact import ExactEvmClientScheme

# 1. Define the tool input schema
class CryptoReturnInput(BaseModel):
    symbol: str = Field(..., description="Cryptocurrency ticker symbol (e.g., BTC, ETH, SOL)")
    amount: float = Field(..., description="Investment amount in USD")
    date: str = Field(..., description="Purchase date in YYYY-MM-DD format")

# 2. Create the custom CrewAI tool
class CryptoRetailTool(BaseTool):
    name: str = "calculate_crypto_return"
    description: str = "Calculates historical crypto investment returns. Returns current value, ROI, and peak value."
    args_schema: type[BaseModel] = CryptoReturnInput
    
    def _run(self, symbol: str, amount: float, date: str) -> str:
        # Initialize x402 client inside the tool execution
        client = X402Client()
        client.register("eip155:8453", ExactEvmClientScheme(os.environ["EVM_PRIVATE_KEY"]))
        
        # The client automatically handles the $0.02 USDC payment
        response = client.get(
            "https://api.cryptoretail.store/v1/calculate",
            params={"symbol": symbol, "amount": amount, "date": date}
        )
        return response.text

# 3. Create the agent and task
analyst = Agent(
    role="Crypto Investment Analyst",
    goal="Analyze historical crypto returns and provide insights",
    backstory="You are an expert crypto analyst who uses historical data to evaluate investment decisions.",
    tools=[CryptoRetailTool()],
    verbose=True
)

task = Task(
    description="Calculate what a $500 investment in Ethereum on 2021-01-01 would be worth today. Extract the current value and the ROI.",
    expected_output="A short summary stating the current value and ROI percentage.",
    agent=analyst
)

# 4. Run the crew
crew = Crew(agents=[analyst], tasks=[task])
result = crew.kickoff()
```
