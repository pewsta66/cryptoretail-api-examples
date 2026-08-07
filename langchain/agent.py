import os
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from x402.client import X402Client
from x402.mechanisms.evm.exact import ExactEvmClientScheme

# Ensure you have set EVM_PRIVATE_KEY and OPENAI_API_KEY in your environment
private_key = os.environ.get("EVM_PRIVATE_KEY")
if not private_key:
    raise ValueError("EVM_PRIVATE_KEY environment variable is required")

# 1. Initialize the x402 client with your wallet (Base mainnet)
client = X402Client()
client.register("eip155:8453", ExactEvmClientScheme(private_key))

# 2. Define the tool wrapper
def calculate_crypto_return(query: str) -> str:
    """
    Wrapper function that LangChain will call.
    The x402 client automatically intercepts the 402 Payment Required response,
    signs the $0.02 USDC payment authorization, and retries the request.
    """
    try:
        # Simple parsing for the example
        parts = query.split(",")
        if len(parts) != 3:
            return "Error: Input must be exactly three comma-separated values: symbol, amount, date"
            
        symbol, amount, date = [p.strip() for p in parts]
        
        print(f"\n[Tool] Calling CryptoRetail API for {symbol}...")
        response = client.get(
            "https://api.cryptoretail.store/v1/calculate",
            params={"symbol": symbol, "amount": amount, "date": date}
        )
        
        # Return the JSON string to the agent
        return response.text
        
    except Exception as e:
        return f"Error calling API: {str(e)}"

# 3. Create the LangChain tool
crypto_tool = Tool(
    name="calculate_crypto_return",
    func=calculate_crypto_return,
    description="Calculates historical crypto investment returns. Input must be a comma-separated string: symbol, amount, YYYY-MM-DD date. Example: 'BTC, 1000, 2021-07-26'"
)

# 4. Initialize and run the agent
print("Initializing LangChain agent...")
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
agent = initialize_agent(
    [crypto_tool], 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

print("\nRunning query...")
agent.run("What would $1000 invested in SOL on 2022-01-01 be worth today? Give me the ROI percentage and current value.")
