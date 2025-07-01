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
cd lab/personal

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
      "cwd": "/path/to/your/lab/personal"
    }
  }
}
```

### Step 3: Restart Claude Desktop

Claude will automatically connect to your MCP server and load your tools!

---

## 🚀 Method 2: HTTP Connection (For Development)

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

### Step 1: Install MCP Inspector

```bash
# Install the MCP development tools
npm install -g @modelcontextprotocol/inspector
```

### Step 2: Run MCP Inspector

```bash
# Run inspector to test your MCP server
mcp-inspector fastmcp run context_manager.py
```

This opens a web interface where you can test your tools directly!

### Step 3: Connect to Cursor

In Cursor, you can configure MCP connections in settings:

```json
{
  "mcp.servers": {
    "personal-context": {
      "command": "fastmcp",
      "args": ["run", "context_manager.py"],
      "cwd": "./lab/personal"
    }
  }
}
```

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
# Check what's running on port 8000
netstat -an | grep 8000

# Use a different port
fastmcp run context_manager.py --port 8001
```

**2. Path Issues**
```bash
# Make sure Claude can find your MCP server
which fastmcp
# Should return path to fastmcp executable
```

**3. Permission Issues**
```bash
# Make sure your MCP server file is executable
chmod +x context_manager.py
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
- Look for MCP connection errors in Claude Desktop logs
- Check that all required dependencies are installed

**3. Use MCP Inspector**
```bash
# Best debugging tool - visual interface
mcp-inspector fastmcp run context_manager.py
```

---

## 🎯 Real-World Example: Context Manager in Action

### Scenario: Managing a Project

**Step 1: Store Project Context**
```
You: "Store context about our new MCP project - we're building a personal AI toolkit starting with a context manager, targeting executive productivity tools eventually."

Claude: [Calls add_context]
✅ Project context stored with details about MCP toolkit development and executive productivity goals.
```

**Step 2: Track Decisions**
```
You: "We decided to use FastMCP instead of the standard SDK because of better server composition."

Claude: [Calls add_context with type="decision"]
✅ Decision recorded with reasoning about FastMCP advantages.
```

**Step 3: Retrieve Context Later**
```
You: "What was our reasoning for choosing FastMCP?"

Claude: [Calls search_context("FastMCP")]
Retrieved context: You chose FastMCP for server composition advantages over the standard MCP SDK, particularly for building scalable personal AI toolkit servers.
```

**Step 4: Project Status Check**
```
You: "What's the status of our MCP project?"

Claude: [Calls get_context_by_type("project")]
Current project status:
- ✅ Personal AI Toolkit concept defined
- ✅ Context Manager MCP server built
- ✅ FastMCP framework selected and implemented
- 🎯 Next: Building additional personal productivity tools
```

---

## 🚀 Next Steps After Connection

Once your MCP server is connected:

1. **Test Each Tool** - Verify all functions work as expected
2. **Build Workflows** - Create tool chains for common tasks
3. **Add More Servers** - Build additional MCP servers for different domains
4. **Scale Up** - Move from personal to team/executive tools

---

**The magic happens when Claude/Cursor can seamlessly use your custom tools as if they were built-in capabilities!** 