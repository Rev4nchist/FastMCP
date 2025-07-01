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

## 🔧 Environment Setup

### Create Virtual Environment (Recommended)
```bash
# Create a virtual environment for MCP development
python -m venv mcp-env

# Activate it:
# Windows
mcp-env\Scripts\activate
# Mac/Linux
source mcp-env/bin/activate

# Install FastMCP
pip install fastmcp

# Verify installation
fastmcp --version
```

---

## 🎯 Quick Start: Your First 5 Minutes

### 1. Test the Context Manager
```bash
# Navigate to lab
cd C:/path/to/your/lab/personal

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
      "cwd": "C:/full/path/to/your/lab/personal"
    }
  }
}
```

### 3. Test It Works
In Claude Desktop:
- **You**: "Remember that we're building a personal AI toolkit with MCP servers"
- **Claude**: *[Uses add_context tool]* ✅ Context stored!

---

## 🎯 Real Example: Notion Project Dashboard

Here's what we'll build as our first real MCP server:

**Problem**: Manually updating Notion project dashboards with scattered information
**Solution**: MCP server that organizes docs, updates status, and generates project views

**What it will do:**
- Scan your Notion pages for project-related content
- Organize scattered links and documents
- Generate clean project dashboards
- Update project status automatically

---

## 📚 Lab Resources

### Core Documentation
- **[Methodology Guide](methodology.md)** - Complete framework for building MCP servers
- **[Connection Guide](connection-guide.md)** - How to connect MCP servers to Claude/Cursor
- **[Quick Reference](quick-reference.md)** - One-page cheat sheet for rapid development
- **[Security Best Practices](security-best-practices.md)** - Keep your MCP servers secure
- **[Notion Example Walkthrough](notion-example-walkthrough.md)** - Complete example from pain point to deployment

### Current Experiments
- **[Personal Context Manager](../personal/context_manager.py)** - Intelligent context management across conversations

### Lab Structure
```
lab/
├── README.md                 # Lab overview and mission
├── docs/                     # All documentation
│   ├── methodology.md        # Development framework
│   ├── connection-guide.md   # Integration instructions
│   ├── getting-started.md    # This file
│   ├── quick-reference.md    # Quick commands and patterns
│   ├── security-best-practices.md  # Security guidelines
│   └── notion-example-walkthrough.md  # Complete Notion example
├── personal/                 # Personal productivity tools
│   └── context_manager.py    # Context management MCP server
├── examples/                 # Example MCP servers
│   └── notion_dashboard.py   # Notion dashboard updater
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
   - Example: "I spend 30 minutes daily updating my Notion project dashboard"

2. **Research APIs** 
   - What services have APIs you could leverage?
   - Check for OpenAPI specs (auto-generation possible!)
   - Example: Notion API has great documentation and Python SDK

3. **Design Tools**
   - What actions would the AI need to perform?
   - What information would it need to access?
   - Example: `update_project_status`, `organize_documents`, `generate_dashboard`

4. **Build with FastMCP**
   ```python
   from fastmcp import FastMCP
   
   mcp = FastMCP("Notion Dashboard Updater")
   
   @mcp.tool
   def update_project_status(project_id: str, status: str) -> str:
       """Update project status in Notion"""
       # Implementation
       return f"Updated project {project_id} to {status}"
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
- [ ] Set up development environment properly
- [ ] Review the Notion example walkthrough
- [ ] Identify your first custom pain point

### Week 2: Build Your First Tool
- [ ] Apply methodology to your pain point
- [ ] Research relevant APIs (start with Notion API)
- [ ] Build simple MCP server with 2-3 tools
- [ ] Test with MCP Inspector
- [ ] Connect to Claude and iterate

### Week 3: Scale and Integrate
- [ ] Add more sophisticated tools
- [ ] Implement proper error handling
- [ ] Add security measures (API key management)
- [ ] Experiment with server composition
- [ ] Share with team for feedback

---

## 🚨 Common Issues & Solutions

### "fastmcp: command not found"
```bash
# Make sure you activated your virtual environment
# Windows
mcp-env\Scripts\activate
# Mac/Linux
source mcp-env/bin/activate

# Then install FastMCP
pip install fastmcp
```

### "Port already in use"
```bash
# Check what's using the port
netstat -an | grep 8000

# Use different port
fastmcp run context_manager.py --port 8001
```

### "Claude can't connect to MCP server"
- Check file paths in claude_desktop_config.json (use absolute paths!)
- Ensure server is running before starting Claude
- Verify no firewall blocking localhost connections
- Check Claude logs: `%APPDATA%\Claude\logs`

### "Module not found" errors
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt

# Or install specific missing module
pip install notion-client  # for Notion example
```

---

## 🎭 The EVE Approach

Remember the core philosophy:
- **Test on yourself first** - Build tools YOU need daily
- **Filter the BS** - Focus on meaningful time savings
- **Scale elegantly** - Design for personal, architect for teams
- **Executive-ready** - Include proper error handling from day one
- **Security-first** - Never hardcode API keys, always use environment variables

---

## 🚀 Next Steps

1. **Get Context Manager working** - Your foundation for everything else
2. **Review the Notion example** - See a complete implementation
3. **Study methodology.md** - Your systematic development framework  
4. **Identify your next tool** - What pain point will you solve after Notion?
5. **Join the conversation** - Share your experiments and learnings

---

*Remember: Every executive productivity suite starts with solving personal pain points. Build tools that make YOUR work better, then scale them up!*

**Ready to build something amazing? Let's get started! 🔥** 