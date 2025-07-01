# 🔌 How to Connect MCP Servers to Claude/Cursor
## *The Missing Manual for MCP Integration*

---

## 🧠 Understanding the Connection Flow

When you run an MCP server, here's what actually happens:

```
1. [Your MCP Server] starts on local port (e.g., http://localhost:8000)
2. [Claude/Cursor] connects to that server via MCP client
3. [AI Model] can now call your tools and access your resources
4. [You] interact with AI, which uses your tools seamlessly
```

---

## 🚀 Method 1: Direct FastMCP Connection (Recommended)

### Step 1: Run Your MCP Server

```bash
# Navigate to your MCP server directory
cd C:/path/to/your/lab/personal

# Run the Context Manager MCP server
fastmcp run context_manager.py

# You'll see output like:
# INFO:     FastMCP server 'Personal Context Manager' running on port 8000
# INFO:     MCP server available at: http://localhost:8000/mcp
```

### Step 2: Configure Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "personal-context-manager": {
      "command": "fastmcp",
      "args": ["run", "context_manager.py"],
      "cwd": "C:/full/path/to/your/lab/personal"
    }
  }
}
```

### Step 3: Restart Claude Desktop

Claude will automatically connect to your MCP server and load your tools!

---

## 🚀 Method 2: HTTP Connection (For Development)

### Prerequisites for HTTP Method
```bash
# Install required dependencies
pip install httpx
```

### Step 1: Run Server with HTTP Transport

```python
# In your MCP server file
if __name__ == "__main__":
    # Run with HTTP transport for easy connection
    mcp.run(transport="http", port=8000)
```

### Step 2: Test Connection

```bash
# Test that your server is responding
curl http://localhost:8000/mcp/tools/list

# Should return JSON with your available tools
```

### Step 3: Configure Claude with HTTP Transport

```json
{
  "mcpServers": {
    "personal-context-manager": {
      "command": "python",
      "args": ["-m", "httpx", "http://localhost:8000/mcp"],
      "transport": "http"
    }
  }
}
```

---

## 🔧 Method 3: Development Mode (VS Code/Cursor)

### Prerequisites
```bash
# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector
```

### Step 1: Run MCP Inspector

```bash
# Run inspector to test your MCP server
mcp-inspector fastmcp run context_manager.py
```

This opens a web interface where you can test your tools directly!

### Step 2: Connect to Cursor

In Cursor, you can configure MCP connections in settings:

```json
{
  "mcp.servers": {
    "personal-context": {
      "command": "fastmcp",
      "args": ["run", "context_manager.py"],
      "cwd": "C:/full/path/to/your/lab/personal"
    }
  }
}
```

---

## 🚀 Running Multiple MCP Servers

### Configure Multiple Servers in Claude

```json
{
  "mcpServers": {
    "context-manager": {
      "command": "fastmcp",
      "args": ["run", "context_manager.py"],
      "cwd": "C:/path/to/lab/personal"
    },
    "notion-dashboard": {
      "command": "fastmcp",
      "args": ["run", "notion_dashboard.py", "--port", "8001"],
      "cwd": "C:/path/to/lab/examples"
    },
    "github-tools": {
      "command": "fastmcp",
      "args": ["run", "github_tools.py", "--port", "8002"],
      "cwd": "C:/path/to/lab/integration"
    }
  }
}
```

### Important Notes for Multiple Servers:
- Each server needs a unique port (8000, 8001, 8002, etc.)
- Claude will load all servers on startup
- Tools from all servers are available in one conversation
- Name servers clearly to avoid confusion

---

## 🎯 Understanding Your Context Manager Connection

Once connected, your Context Manager provides these tools to Claude/Cursor:

### Available Tools:
1. `add_context` - Store new context information
2. `search_context` - Find relevant context by keyword
3. `get_recent_context` - Retrieve recent context entries
4. `update_context` - Modify existing context
5. `get_context_stats` - View usage analytics
6. `get_context_by_type` - Filter by context type
7. `delete_context` - Remove context entries

### Example Usage in Claude:

**You**: "Remember that we decided to use FastMCP for our personal AI toolkit because it has better server composition features than the standard MCP SDK."

**Claude** (using your Context Manager): 
```
I'll store that decision for future reference.
[Calls add_context tool with decision details]
✅ Stored decision about FastMCP choice with reasoning about server composition features
```

**Later...**

**You**: "What did we decide about MCP frameworks?"

**Claude** (using your Context Manager):
```
[Calls search_context tool with "MCP frameworks"]
Based on our previous decision: We chose FastMCP for our personal AI toolkit because it has better server composition features than the standard MCP SDK.
```

---

## 🔍 Debugging Connection Issues

### Common Problems:

**1. Port Conflicts**
```bash
# Windows: Check what's running on port 8000
netstat -an | findstr :8000

# Mac/Linux:
lsof -i :8000

# Use a different port
fastmcp run context_manager.py --port 8001
```

**2. Path Issues**
```bash
# Make sure FastMCP is in your PATH
where fastmcp  # Windows
which fastmcp  # Mac/Linux

# Should return path to fastmcp executable
```

**3. Permission Issues**
```bash
# Windows: Run as administrator if needed
# Mac/Linux: Make sure your MCP server file is executable
chmod +x context_manager.py
```

**4. Virtual Environment Issues**
```bash
# Make sure Claude can find your virtual environment
# Update config to use full Python path:
{
  "mcpServers": {
    "context-manager": {
      "command": "C:/path/to/mcp-env/Scripts/python",
      "args": ["-m", "fastmcp", "run", "context_manager.py"],
      "cwd": "C:/path/to/lab/personal"
    }
  }
}
```

### Verification Steps:

**1. Test Server Directly**
```bash
# Run server and test manually
fastmcp run context_manager.py

# In another terminal, test tools:
curl -X POST http://localhost:8000/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "add_context", "params": {"context_type": "test", "content": "Hello World"}}'
```

**2. Check Claude Logs**
```
# Windows logs location:
%APPDATA%\Claude\logs\

# Look for MCP connection errors
# Common errors:
- "Failed to start MCP server" - Path issues
- "Connection refused" - Server not running
- "Tool not found" - Server connected but tools not registered
```

**3. Use MCP Inspector**
```bash
# Best debugging tool - visual interface
mcp-inspector fastmcp run context_manager.py

# Opens browser at http://localhost:5173
# Test each tool individually
# See real-time request/response data
```

---

## 🎯 Real-World Example: Notion Dashboard + Context Manager

### Scenario: Managing Multiple Projects with Context

**Step 1: Configure Both Servers**
```json
{
  "mcpServers": {
    "context-manager": {
      "command": "fastmcp",
      "args": ["run", "context_manager.py"],
      "cwd": "C:/lab/personal"
    },
    "notion-dashboard": {
      "command": "fastmcp",
      "args": ["run", "notion_dashboard.py", "--port", "8001"],
      "cwd": "C:/lab/examples"
    }
  }
}
```

**Step 2: Use Both Together**
```
You: "Update my Notion dashboard for the MCP Lab project and remember the current status"

Claude: 
[Calls notion_dashboard.update_project_status("MCP Lab", "Phase 2: Building Examples")]
✅ Updated Notion dashboard

[Calls context_manager.add_context("project_status", "MCP Lab moved to Phase 2")]
✅ Context stored for future reference
```

**Step 3: Leverage Combined Power**
```
You: "What's the status of all my projects?"

Claude:
[Calls context_manager.search_context("project_status")]
[Calls notion_dashboard.get_all_projects()]

Here's your project overview:
- MCP Lab: Phase 2 (Building Examples) ✅
- AI Toolkit: Planning phase 📋
- Executive Dashboard: In development 🔨
```

---

## 🚀 Advanced Configuration Tips

### Environment Variables for API Keys
```json
{
  "mcpServers": {
    "notion-dashboard": {
      "command": "fastmcp",
      "args": ["run", "notion_dashboard.py"],
      "cwd": "C:/lab/examples",
      "env": {
        "NOTION_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Custom Python Path
```json
{
  "mcpServers": {
    "my-server": {
      "command": "C:/path/to/specific/python.exe",
      "args": ["-m", "fastmcp", "run", "server.py"],
      "cwd": "C:/lab/examples"
    }
  }
}
```

### Debugging Mode
```json
{
  "mcpServers": {
    "my-server": {
      "command": "fastmcp",
      "args": ["run", "server.py", "--debug"],
      "cwd": "C:/lab/examples",
      "env": {
        "FASTMCP_DEBUG": "true"
      }
    }
  }
}
```

---

## 🚀 Next Steps After Connection

Once your MCP servers are connected:

1. **Test Each Tool** - Verify all functions work as expected
2. **Build Workflows** - Create tool chains for common tasks
3. **Monitor Performance** - Check response times and optimize
4. **Add More Servers** - Build additional MCP servers for different domains
5. **Document Patterns** - Record successful tool combinations

---

**The magic happens when Claude/Cursor can seamlessly use your custom tools as if they were built-in capabilities! Start with one server, then scale to an entire suite of productivity tools. 🔥** 