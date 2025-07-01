# 🚀 EVE-MCP-LAB: Getting Started
## *Quick Start Guide for Personal AI Toolkit Development*

---

## 📋 Prerequisites

Before diving in, make sure you have:

- **Python 3.8+** installed
- **FastMCP** framework (`pip install fastmcp`)
- **Claude Desktop** or **Cursor** for MCP integration
- **Basic understanding** of APIs and Python

---

## 🎯 Quick Start: Your First 5 Minutes

### 1. Test the Context Manager
```bash
# Navigate to lab
cd lab/personal

# Run our first MCP server
fastmcp run context_manager.py

# Should see: "FastMCP server 'Personal Context Manager' running on port 8000"
```

### 2. Connect to Claude Desktop
Add to your Claude config (`%APPDATA%\Claude\claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "personal-context-manager": {
      "command": "fastmcp",
      "args": ["run", "context_manager.py"],
      "cwd": "C:/path/to/your/lab/personal"
    }
  }
}
```

### 3. Test It Works
In Claude Desktop:
- **You**: "Remember that we're building a personal AI toolkit with MCP servers"
- **Claude**: *[Uses add_context tool]* ✅ Context stored!

---

## 📚 Lab Resources

### Core Documentation
- **[Methodology Guide](methodology.md)** - Complete framework for building MCP servers
- **[Connection Guide](connection-guide.md)** - How to connect MCP servers to Claude/Cursor
- **[Lab Overview](../README.md)** - Mission, phases, and current status

### Current Experiments
- **[Personal Context Manager](../personal/context_manager.py)** - Intelligent context management across conversations

### Lab Structure
```
lab/
├── README.md                 # Lab overview and mission
├── docs/                     # All documentation
│   ├── methodology.md        # Development framework
│   ├── connection-guide.md   # Integration instructions
│   └── getting-started.md    # This file
├── personal/                 # Personal productivity tools
│   └── context_manager.py    # Context management MCP server
├── executive/                # Executive team tools (future)
├── integration/              # System integration tools (future)
└── research/                 # Research and experiments (future)
```

---

## 🛠️ Development Workflow

### Building Your Next MCP Server

1. **Identify Pain Point** (use methodology.md)
   - What repetitive task is eating your time?
   - What information do you frequently need?

2. **Research APIs** 
   - What services have APIs you could leverage?
   - Check for OpenAPI specs (auto-generation possible!)

3. **Design Tools**
   - What actions would the AI need to perform?
   - What information would it need to access?

4. **Build with FastMCP**
   ```python
   from fastmcp import FastMCP
   
   mcp = FastMCP("Your MCP Server Name")
   
   @mcp.tool
   def your_tool(param: str) -> str:
       """Your tool description"""
       # Implementation
       return result
   ```

5. **Test and Connect**
   - Test locally with `fastmcp run your_server.py`
   - Add to Claude Desktop config
   - Verify tools work as expected

---

## 🎯 Suggested Learning Path

### Week 1: Master the Basics
- [ ] Get Context Manager working with Claude
- [ ] Read through methodology.md completely
- [ ] Experiment with Context Manager tools
- [ ] Identify your first custom pain point

### Week 2: Build Your First Tool
- [ ] Apply methodology to your pain point
- [ ] Research relevant APIs
- [ ] Build simple MCP server with 2-3 tools
- [ ] Test and iterate

### Week 3: Scale and Integrate
- [ ] Add more sophisticated tools
- [ ] Experiment with server composition
- [ ] Start planning executive-level tools
- [ ] Document your learnings

---

## 🚨 Common Issues & Solutions

### "fastmcp: command not found"
```bash
# Install FastMCP
pip install fastmcp

# Or if using virtual environment
pip install -e .
```

### "Port already in use"
```bash
# Use different port
fastmcp run context_manager.py --port 8001
```

### "Claude can't connect to MCP server"
- Check file paths in claude_desktop_config.json
- Ensure server is running before starting Claude
- Verify no firewall blocking localhost connections

---

## 🎭 The EVE Approach

Remember the core philosophy:
- **Test on yourself first** - Build tools YOU need daily
- **Filter the BS** - Focus on meaningful time savings
- **Scale elegantly** - Design for personal, architect for teams
- **Executive-ready** - Include proper error handling from day one

---

## 🚀 Next Steps

1. **Get Context Manager working** - Your foundation for everything else
2. **Study methodology.md** - Your systematic development framework  
3. **Identify your next tool** - What pain point will you solve next?
4. **Join the conversation** - Share your experiments and learnings

---

*Remember: Every executive productivity suite starts with solving personal pain points. Build tools that make YOUR work better, then scale them up!*

**Ready to build something amazing? Let's get started! 🔥** 