# 🎯 MCP Development Methodology: The EVE Framework
## *A Complete Guide to Building Production-Ready MCP Servers*

---

## 📋 TL;DR - MCP Development in 7 Steps

1. **Find repetitive task that annoys you** (e.g., updating Notion dashboards manually)
2. **Find API that can automate it** (e.g., Notion API has great Python SDK)
3. **Create FastMCP server with tools** (`@mcp.tool` decorator on functions)
4. **Test locally with MCP Inspector** (`mcp-inspector fastmcp run server.py`)
5. **Connect to Claude/Cursor** (add to config.json)
6. **Iterate based on real usage** (add error handling, improve UX)
7. **Share with team when polished** (document patterns, create templates)

**Example**: Turn "30 minutes updating Notion dashboards" into "Hey Claude, update my project status" ✨

---

## 🧠 Understanding MCP Architecture

### What MCP Actually Does
The **Model Context Protocol (MCP)** is the "USB-C for AI" - it creates a standardized way for AI models (Claude, GPT, etc.) to connect to external tools, data, and services. Think of it as an **API gateway specifically designed for LLM interactions**.

```
[AI Model] ←→ [MCP Client] ←→ [MCP Server] ←→ [Your Tools/Data/APIs]
     ↑              ↑              ↑              ↑
   Claude      Built into      Your Custom      External
  /Cursor      Claude/Cursor     MCP Server      Services
```

### The Three MCP Primitives

1. **Tools** (Functions the AI can call)
   - Like POST/PUT endpoints
   - Execute actions, computations, side effects
   - Return results to the AI

2. **Resources** (Data the AI can read)
   - Like GET endpoints
   - Provide information, documents, context
   - Can be static or dynamic (templates)

3. **Prompts** (Reusable interaction patterns)
   - Pre-defined conversation starters
   - Standardized ways to interact with your tools

---

## 🎯 The EVE MCP Development Framework

### Phase 1: Opportunity Identification

#### 1.1 The "Pain Point Audit"
Ask these questions:
- **What repetitive tasks** are eating your time?
- **What information** do you frequently need but can't easily access?
- **What decisions** require data from multiple sources?
- **What workflows** involve manual steps between systems?
- **What context** gets lost between conversations/sessions?

**Real Example - Notion Dashboard Pain**:
- ❌ Manually updating project status across multiple pages
- ❌ Copy-pasting links between documents
- ❌ Creating project summaries from scattered notes
- ❌ Tracking progress across different workspaces

#### 1.2 The "AI-Worthy Test"
A task is MCP-worthy if:
- ✅ **Repeatable**: You do it more than once
- ✅ **Data-Dependent**: Requires specific information
- ✅ **Context-Sensitive**: Benefits from conversation context
- ✅ **Cross-System**: Involves multiple tools/services
- ✅ **Decision-Support**: Helps make better choices faster

**Notion Dashboard scores 5/5** - Perfect MCP candidate!

#### 1.3 Opportunity Categories

**Personal Productivity**
- Task management integration
- Calendar/scheduling automation
- File organization and search
- Note-taking and knowledge management
- Personal analytics and tracking

**Team Coordination**
- Project status aggregation
- Communication summarization
- Resource allocation tracking
- Decision documentation
- Progress reporting

**Executive Intelligence**
- KPI monitoring and alerts
- Market intelligence gathering
- Competitive analysis automation
- Strategic decision support
- Performance dashboard creation

**System Integration**
- API aggregation and normalization
- Data pipeline monitoring
- Service health checking
- Automated reporting
- Cross-platform synchronization

### Phase 2: API Discovery & Analysis

#### 2.1 REST API Goldmines
Look for these API characteristics:
- **Well-documented** (OpenAPI/Swagger preferred)
- **Stable endpoints** (versioned APIs)
- **Rich data models** (detailed responses)
- **Authentication supported** (API keys, OAuth)
- **Rate limits reasonable** (won't get blocked)

**Notion API Example**:
- ✅ Excellent documentation: https://developers.notion.com
- ✅ Stable v1 API with versioning
- ✅ Rich block-based content model
- ✅ Simple bearer token auth
- ✅ Generous rate limits (3 requests/second)

#### 2.2 FastMCP's Auto-Generation Magic
FastMCP can automatically convert REST APIs to MCP servers:

```python
# Auto-generate from OpenAPI spec
mcp_server = FastMCP.from_openapi(
    openapi_spec=api_spec,
    client=httpx_client
)

# Auto-generate from FastAPI app
mcp_server = FastMCP.from_fastapi(
    app=fastapi_app,
    name="Generated MCP Server"
)

# For Notion (manual but straightforward):
from notion_client import Client
from fastmcp import FastMCP

notion = Client(auth=os.environ["NOTION_API_KEY"])
mcp = FastMCP("Notion Dashboard Manager")

@mcp.tool
def update_page_title(page_id: str, title: str) -> str:
    """Update a Notion page title"""
    notion.pages.update(page_id, properties={"title": {"title": [{"text": {"content": title}}]}})
    return f"Updated page {page_id} title to: {title}"
```

#### 2.3 High-Value API Categories

**Productivity APIs**
- Google Workspace (Docs, Sheets, Calendar)
- Microsoft 365 (Outlook, Teams, SharePoint)
- Notion, Airtable, Monday.com
- Slack, Discord, Zoom

**Data & Analytics**
- Financial APIs (Alpha Vantage, Yahoo Finance)
- Social media APIs (Twitter, LinkedIn)
- Analytics APIs (Google Analytics, Mixpanel)
- Weather, news, market data

**Developer Tools**
- GitHub, GitLab, Bitbucket
- CI/CD platforms (Jenkins, GitHub Actions)
- Monitoring (Datadog, New Relic)
- Cloud providers (AWS, Azure, GCP)

### Phase 3: MCP Tool Design

#### 3.1 Tool Categorization Strategy

**Action Tools** (Do something)
```python
@mcp.tool
def create_project_dashboard(name: str, template_id: str = None) -> str:
    """Create a new project dashboard in Notion"""
    # Implementation
```

**Query Tools** (Get information)
```python
@mcp.tool
def find_project_documents(project_name: str) -> List[dict]:
    """Find all documents related to a project"""
    # Implementation
```

**Analysis Tools** (Process data)
```python
@mcp.tool
def analyze_project_progress(project_id: str) -> dict:
    """Analyze project completion and blockers"""
    # Implementation
```

**Orchestration Tools** (Coordinate multiple actions)
```python
@mcp.tool
def organize_project_workspace(project_name: str) -> str:
    """Complete project organization workflow"""
    # 1. Find scattered documents
    # 2. Create organized structure
    # 3. Update cross-references
    # 4. Generate summary dashboard
```

#### 3.2 Tool Design Principles

**Atomic but Powerful**
- Each tool does ONE thing well
- But that one thing should be meaningfully useful
- Avoid micro-tools that require many calls

**Context-Aware**
- Accept context parameters when needed
- Use the FastMCP Context object for logging/sampling
- Store and retrieve relevant state

**Error-Resilient**
- Handle API failures gracefully
- Provide meaningful error messages
- Implement retry logic where appropriate

**Performance-Conscious**
- Cache expensive operations
- Use async/await for I/O operations
- Respect API rate limits

**🔒 Security-First**
- NEVER hardcode API keys
- Use environment variables: `os.environ["NOTION_API_KEY"]`
- Validate all inputs
- Sanitize outputs
- Log security events

#### 3.3 Resource Design Strategy

**Static Resources** (Fixed data)
```python
@mcp.resource("config://api-endpoints")
def get_api_endpoints():
    """Available API endpoints"""
    return {"endpoints": [...]}
```

**Dynamic Resources** (Template-based)
```python
@mcp.resource("project://{project_id}/status")
def get_project_status(project_id: str):
    """Get real-time project status"""
    # Implementation
```

### Phase 4: Architecture Patterns

#### 4.1 The "Hub-and-Spoke" Pattern
For executive/team tools:
```python
# Main hub server
hub_mcp = FastMCP("Executive Hub")

# Mount specialized servers
hub_mcp.mount("finance", finance_mcp)
hub_mcp.mount("projects", project_mcp)
hub_mcp.mount("hr", hr_mcp)
```

#### 4.2 The "Pipeline" Pattern
For data processing workflows:
```python
@mcp.tool
def analyze_pipeline(data_source: str) -> str:
    """Execute complete data analysis pipeline"""
    raw_data = extract_data(data_source)
    cleaned_data = clean_data(raw_data)
    insights = analyze_data(cleaned_data)
    report = generate_report(insights)
    return report
```

#### 4.3 The "State Machine" Pattern
For complex workflows:
```python
class WorkflowState(Enum):
    PLANNING = "planning"
    EXECUTING = "executing"
    REVIEWING = "reviewing"
    COMPLETED = "completed"

@mcp.tool
def advance_workflow(workflow_id: str, action: str) -> str:
    """Advance workflow to next state"""
    # State machine logic
```

### Phase 5: Development Process

#### 5.1 The EVE Development Cycle

**1. Discover** (Identify the opportunity)
- Pain point analysis
- API research
- Stakeholder interviews

**2. Design** (Plan the MCP architecture)
- Tool/resource mapping
- Data flow design
- Error handling strategy
- 🔒 Security architecture

**3. Develop** (Build the MCP server)
- Start with simple tools
- Add complexity incrementally
- Test each tool individually
- Implement security measures

**4. Deploy** (Make it production-ready)
- Add authentication
- Implement monitoring
- Create documentation
- Security audit

**5. Distribute** (Scale to team/organization)
- Package for easy installation
- Create onboarding materials
- Monitor adoption and feedback
- Regular security updates

#### 5.2 Testing Strategy

**Unit Testing**
```python
async def test_tool():
    result = await mcp_server._call_tool("tool_name", {"param": "value"})
    assert result.success
```

**Integration Testing**
```python
async def test_api_integration():
    # Test with real APIs (in test environment)
```

**Security Testing**
```python
async def test_api_key_not_exposed():
    # Ensure no keys in responses
    # Test input validation
    # Check for injection vulnerabilities
```

**User Acceptance Testing**
- Test with actual users
- Gather feedback on tool usefulness
- Iterate based on real usage patterns

### Phase 6: Deployment & Scaling

#### 6.1 Production Considerations

**🔒 Authentication**
```python
from fastmcp.server.auth import EnvBearerAuthProvider

mcp = FastMCP(
    "Production Server",
    auth=EnvBearerAuthProvider()  # Reads from FASTMCP_AUTH_TOKEN env var
)
```

**Middleware**
```python
from fastmcp.server.middleware import LoggingMiddleware, RateLimitMiddleware

mcp.add_middleware(LoggingMiddleware())
mcp.add_middleware(RateLimitMiddleware(requests_per_minute=100))
```

**Monitoring**
```python
@mcp.tool
async def monitored_tool(param: str, ctx: Context) -> str:
    ctx.info(f"Tool called with param: {param}")
    # Tool implementation
    ctx.info("Tool completed successfully")
```

**🔒 Security Hardening**
```python
# Environment variable management
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

# API key rotation support
API_KEY = os.environ.get("NOTION_API_KEY")
if not API_KEY:
    raise ValueError("NOTION_API_KEY environment variable not set")

# Input validation
from pydantic import BaseModel, validator

class ProjectUpdate(BaseModel):
    project_id: str
    status: str
    
    @validator('status')
    def validate_status(cls, v):
        allowed = ['planning', 'active', 'completed', 'on-hold']
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v
```

#### 6.2 Distribution Strategy

**Personal Use**
- Single-user installation
- Local file storage
- Simple configuration
- Personal API keys

**Team Use**
- Shared server deployment
- Centralized authentication
- Team-specific configurations
- Shared API key management

**Enterprise Use**
- High availability deployment
- Enterprise authentication (SSO)
- Audit logging and compliance
- Key rotation policies

---

## 🎯 MCP Development Checklist

### Pre-Development
- [ ] Pain point clearly identified and documented
- [ ] API research completed (endpoints, auth, limits)
- [ ] Tool/resource architecture planned
- [ ] Success metrics defined
- [ ] 🔒 Security requirements identified

### Development
- [ ] Basic FastMCP server structure created
- [ ] Core tools implemented and tested
- [ ] Resources designed and implemented
- [ ] Error handling added
- [ ] 🔒 Input validation implemented
- [ ] 🔒 API keys properly managed
- [ ] Documentation written

### Production
- [ ] Authentication configured
- [ ] Middleware added (logging, rate limiting)
- [ ] Performance tested
- [ ] 🔒 Security audit completed
- [ ] 🔒 Secrets scanning configured
- [ ] Deployment automated
- [ ] Monitoring enabled

### Post-Launch
- [ ] Usage analytics implemented
- [ ] User feedback collected
- [ ] Performance monitored
- [ ] 🔒 Security logs reviewed
- [ ] Iterative improvements planned
- [ ] Regular updates scheduled

---

## 🚀 Common MCP Patterns & Templates

### Pattern 1: Secure API Wrapper
```python
import os
from typing import Optional
import httpx
from fastmcp import FastMCP

class SecureAPIWrapper:
    def __init__(self):
        api_key = os.environ.get("API_KEY")
        if not api_key:
            raise ValueError("API_KEY environment variable not set")
            
        self.client = httpx.AsyncClient(
            base_url="https://api.example.com",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0
        )

@mcp.tool
async def api_call(endpoint: str, params: dict = {}) -> dict:
    """Generic API call wrapper with error handling"""
    try:
        response = await wrapper.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        return {"error": f"API call failed: {str(e)}"}
```

### Pattern 2: Data Aggregator with Caching
```python
from datetime import datetime, timedelta
from typing import Dict, List
import asyncio

# Simple in-memory cache
cache: Dict[str, tuple[datetime, any]] = {}

@mcp.tool
async def aggregate_metrics(sources: List[str], cache_minutes: int = 5) -> dict:
    """Aggregate data from multiple sources with caching"""
    results = {}
    tasks = []
    
    for source in sources:
        # Check cache
        if source in cache:
            cached_time, cached_data = cache[source]
            if datetime.now() - cached_time < timedelta(minutes=cache_minutes):
                results[source] = cached_data
                continue
        
        # Fetch fresh data
        tasks.append(get_source_data(source))
    
    # Fetch all uncached data in parallel
    fresh_data = await asyncio.gather(*tasks)
    
    # Update cache and results
    for source, data in zip(sources, fresh_data):
        cache[source] = (datetime.now(), data)
        results[source] = data
    
    return aggregate_data(results)
```

### Pattern 3: Workflow Orchestrator with Rollback
```python
@mcp.tool
async def execute_workflow(workflow_name: str, params: dict) -> str:
    """Execute workflow with rollback on failure"""
    workflow = get_workflow(workflow_name)
    completed_steps = []
    
    try:
        for step in workflow.steps:
            result = await execute_step(step, params)
            completed_steps.append((step, result))
            params.update(result)
        return "Workflow completed successfully"
    except Exception as e:
        # Rollback completed steps
        for step, result in reversed(completed_steps):
            await rollback_step(step, result)
        return f"Workflow failed and rolled back: {str(e)}"
```

---

## 🎭 The EVE Philosophy Applied

### Test on Yourself First
- Build tools YOU need and use daily
- Validate with your own workflows
- Iterate based on personal pain points

### Scale Elegantly
- Design for personal use, architect for team use
- Keep interfaces simple, make backends powerful
- Plan for growth from day one

### Executive-Ready from Start
- Include proper error handling
- Implement comprehensive logging
- Design for audit and compliance
- 🔒 Security baked in, not bolted on

### Filter the BS
- Focus on tools that save significant time
- Avoid "cool but useless" functionality
- Prioritize decision-support over entertainment

---

## 🔥 Success Metrics

### Personal Productivity
- Time saved per day/week
- Number of manual tasks eliminated
- Improved decision speed
- Reduced context switching

### Team Efficiency
- Reduced duplication of effort
- Faster information access
- Better coordination
- Improved documentation

### Executive Impact
- Improved decision quality
- Reduced time to insight
- Enhanced strategic visibility
- Better risk management

### 🔒 Security Metrics
- Zero exposed credentials
- 100% input validation coverage
- Audit trail completeness
- Incident response time

---

## 🚀 Real Example: Notion Dashboard MCP Server

Here's how the methodology applies to our Notion example:

**1. Pain Point**: 30 minutes daily updating project dashboards
**2. API Research**: Notion API v1, great Python SDK
**3. Tool Design**:
   - `organize_project_docs` - Find and structure scattered documents
   - `update_project_status` - Update status across pages
   - `generate_dashboard` - Create summary views
   - `link_related_pages` - Connect related content

**4. Security Implementation**:
   - API key in environment variable
   - Input validation on all parameters
   - Rate limiting to respect Notion limits
   - Audit logging for all operations

**5. Testing & Iteration**:
   - Start with single project updates
   - Add bulk operations
   - Implement smart search
   - Add progress tracking

**Result**: 30-minute task → 30-second conversation with Claude

---

*This methodology is your blueprint for building MCP servers that don't just work - they transform how you work.*

**Next Steps:**
1. Apply this methodology to identify your first high-impact MCP opportunity
2. Use the templates and patterns to accelerate development
3. Follow the testing and deployment guidelines for production-ready results
4. Scale your successes across your team and organization

**Remember: Start simple, iterate fast, scale smart! 🚀** 