# 🚀 FastMCP Quick Reference
## *Your One-Page Cheat Sheet for MCP Development*

---

## 🎯 Decision Flowchart: Should I Build an MCP Server?

```
Is it repetitive? → NO → ❌ Don't build
      ↓ YES
Involves external data/APIs? → NO → ❌ Don't build
      ↓ YES
Would AI context help? → NO → ❌ Don't build
      ↓ YES
Takes >5 min manually? → NO → ⚠️ Maybe build
      ↓ YES
✅ BUILD IT!
```

---

## ⚡ FastMCP Essential Commands

```bash
# Install
pip install fastmcp

# Create & Run Server
fastmcp run my_server.py                    # Default port 8000
fastmcp run my_server.py --port 8001        # Custom port
fastmcp run my_server.py --debug            # Debug mode

# Test with Inspector
mcp-inspector fastmcp run my_server.py      # Visual testing UI
```

---

## 🛠️ Basic MCP Server Template

```python
from fastmcp import FastMCP
import os

# Initialize (with security!)
mcp = FastMCP("My Server Name")
API_KEY = os.environ.get("MY_API_KEY")  # NEVER hardcode!

# Tool Pattern
@mcp.tool
async def do_something(param: str, optional: str = "default") -> str:
    """Clear description of what this does"""
    # Implementation
    return f"Result: {param}"

# Resource Pattern  
@mcp.resource("data://{item_id}/info")
async def get_data(item_id: str) -> str:
    """Dynamic resource with parameter"""
    return f"Data for {item_id}"

# Run it
if __name__ == "__main__":
    mcp.run()
```

---

## 📋 Common Patterns (Copy & Paste Ready)

### API Integration Pattern
```python
import httpx
from fastmcp import FastMCP, Context

mcp = FastMCP("API Integration")
client = httpx.AsyncClient(
    base_url="https://api.example.com",
    headers={"Authorization": f"Bearer {os.environ['API_KEY']}"}
)

@mcp.tool
async def call_api(endpoint: str, ctx: Context) -> dict:
    """Call external API with error handling"""
    try:
        response = await client.get(endpoint)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        ctx.error(f"API call failed: {e}")
        return {"error": str(e)}
```

### Bulk Operations Pattern
```python
@mcp.tool
async def process_items(item_ids: List[str]) -> dict:
    """Process multiple items efficiently"""
    results = await asyncio.gather(
        *[process_single_item(id) for id in item_ids],
        return_exceptions=True
    )
    return {
        "success": [r for r in results if not isinstance(r, Exception)],
        "failed": [str(r) for r in results if isinstance(r, Exception)]
    }
```

### Caching Pattern
```python
from datetime import datetime, timedelta

cache = {}

@mcp.tool
async def get_cached_data(key: str, ttl_minutes: int = 5) -> Any:
    """Get data with simple caching"""
    if key in cache:
        cached_time, data = cache[key]
        if datetime.now() - cached_time < timedelta(minutes=ttl_minutes):
            return data
    
    # Fetch fresh data
    fresh_data = await fetch_data(key)
    cache[key] = (datetime.now(), fresh_data)
    return fresh_data
```

---

## 🔌 Claude Desktop Config

### Single Server
```json
{
  "mcpServers": {
    "my-server": {
      "command": "fastmcp",
      "args": ["run", "my_server.py"],
      "cwd": "C:/full/path/to/server"
    }
  }
}
```

### Multiple Servers
```json
{
  "mcpServers": {
    "server1": {
      "command": "fastmcp",
      "args": ["run", "server1.py"],
      "cwd": "C:/path/to/server1"
    },
    "server2": {
      "command": "fastmcp",
      "args": ["run", "server2.py", "--port", "8001"],
      "cwd": "C:/path/to/server2"
    }
  }
}
```

---

## 🚨 Common Gotchas & Fixes

| Problem | Fix |
|---------|-----|
| "Module not found" | Activate virtual environment: `mcp-env\Scripts\activate` |
| "Port already in use" | Use different port: `--port 8001` |
| "Claude can't connect" | Use absolute paths in config.json |
| "Tool not showing" | Restart Claude Desktop after config changes |
| "API key error" | Set environment variable: `set MY_API_KEY=xxx` |

---

## 🔒 Security Checklist

- [ ] API keys in environment variables
- [ ] Input validation on all parameters
- [ ] Error messages don't expose sensitive data
- [ ] Rate limiting implemented
- [ ] Logging doesn't include secrets

---

## 📊 Tool Naming Best Practices

✅ **Good Names**
- `update_project_status`
- `get_user_analytics`
- `create_dashboard_report`

❌ **Bad Names**
- `update` (too vague)
- `processDataAndCreateReportThenSendEmail` (too long)
- `do_thing` (unclear)

---

## 🎯 Testing Workflow

1. **Local Test**: `fastmcp run server.py`
2. **Inspector Test**: `mcp-inspector fastmcp run server.py`
3. **Claude Test**: Add to config → Restart Claude → Test tools
4. **Error Test**: Try edge cases, bad inputs
5. **Performance Test**: Check response times

---

## 🚀 From Zero to Working MCP

```bash
# 1. Setup
python -m venv mcp-env && mcp-env\Scripts\activate
pip install fastmcp

# 2. Create server.py (use template above)

# 3. Test locally
fastmcp run server.py

# 4. Add to Claude config

# 5. Use it!
"Hey Claude, use my new tool to..."
```

---

**🔥 Pro Tips:**
- Start with 2-3 tools max
- Test each tool in isolation first
- Use descriptive docstrings (Claude reads them!)
- Log everything during development
- Ship early, iterate often

**Need more? Check:** `methodology.md` for complete framework 