# CryptoRetail API — Integration Examples

Ready-to-use integration snippets for the CryptoRetail x402 API. 

The API provides historical crypto investment returns for 20+ major cryptocurrencies. Given a coin symbol, investment amount in USD, and a purchase date, it returns the current value, ROI, peak value, and full weekly price series.

- **API Endpoint:** `https://api.cryptoretail.store/v1/calculate`
- **MCP Server:** `https://api.cryptoretail.store/mcp`
- **Pricing:** $0.02 USDC per query (Base or Solana mainnet)
- **Website:** [cryptoretail.store](https://cryptoretail.store)

## Integration Guides

Choose your framework to see a working example:

- [Claude Desktop (MCP) ↗](./claude-desktop/) — 4 lines of config
- [LangChain (Python) ↗](./langchain/) — 10 lines of code
- [CrewAI (Python) ↗](./crewai/) — 10 lines of code

## How the Payment Works

Payment is handled automatically via the [x402 protocol](https://x402.org). You do not need an API key. Your agent's wallet signs a payment authorization for $0.02 USDC on Base or Solana mainnet for each successful request. 

For MCP clients (like Claude Desktop and Cursor), the payment is handled transparently by the remote MCP server — you just need to configure the endpoint.
