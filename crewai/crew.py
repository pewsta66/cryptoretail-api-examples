import os
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from x402.client import X402Client
from x402.mechanisms.evm.exact import ExactEvmClientScheme

# Ensure you have set EVM_PRIVATE_KEY and OPENAI_API_KEY in your environment
private_key = os.environ.get("EVM_PRIVATE_KEY")
if not private_key:
    raise ValueError("EVM_PRIVATE_KEY environment variable is required")

# 1. Define the tool input schema using Pydantic
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
        print(f"\n[Tool] Executing CryptoRetail API call for {symbol}...")
        
        # Initialize x402 client
        client = X402Client()
        client.register("eip155:8453", ExactEvmClientScheme(private_key))
        
        try:
            # The client automatically handles the $0.02 USDC payment
            response = client.get(
                "https://api.cryptoretail.store/v1/calculate",
                params={"symbol": symbol, "amount": amount, "date": date}
            )
            return response.text
        except Exception as e:
            return f"Error calling API: {str(e)}"

# 3. Create the agent
analyst = Agent(
    role="Crypto Investment Analyst",
    goal="Analyze historical crypto returns and provide clear, data-driven insights",
    backstory="You are an expert crypto analyst who uses historical data to evaluate investment decisions. You always extract the most important metrics from raw JSON data.",
    tools=[CryptoRetailTool()],
    verbose=True
)

# 4. Create the task
task = Task(
    description="Calculate what a $500 investment in Ethereum on 2021-01-01 would be worth today. Extract the current value, the ROI percentage, and the peak value.",
    expected_output="A short, readable summary stating the current value, ROI percentage, and peak value.",
    agent=analyst
)

# 5. Assemble and run the crew
print("Assembling Crew...")
crew = Crew(
    agents=[analyst],
    tasks=[task],
    verbose=True
)

print("\nKicking off task...")
result = crew.kickoff()

print("\n=== FINAL RESULT ===")
print(result)
