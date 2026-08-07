# Claude Desktop Integration (MCP)

The easiest way to use the CryptoRetail API is through our remote MCP server. This allows Claude to call the API directly from your desktop app, with the $0.02 USDC payment handled automatically by the server.

### 1. Open your Claude Desktop config file
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### 2. Add the CryptoRetail MCP server
Paste this snippet into your `mcpServers` object:

```json
{
  "mcpServers": {
    "cryptoretail": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sse",
        "https://api.cryptoretail.store/mcp"
      ]
    }
  }
}
```

*(Note: While the API uses Streamable HTTP transport, Claude Desktop currently uses the SSE adapter to connect to remote HTTP endpoints).*

### 3. Restart Claude Desktop
Close Claude Desktop completely and reopen it. You will now see the `calculate_crypto_return` tool available (click the hammer icon).

### Example Prompt
Try asking Claude:
> *"Use the CryptoRetail tool to calculate what $1,000 invested in Solana on 1 January 2022 would be worth today."*
