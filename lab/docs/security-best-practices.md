# 🔒 MCP Security Best Practices
## *Building Secure MCP Servers from Day One*

---

## 🎯 Security First Mindset

Building MCP servers means creating bridges between AI models and your systems. Every bridge is a potential attack vector. This guide ensures your MCP servers are fortresses, not open doors.

---

## 🔑 API Key Management

### ❌ NEVER Do This
```python
# WRONG - Hardcoded API key
notion_client = Client(auth="secret_12345678")  # EXPOSED IN CODE!

# WRONG - API key in string
API_KEY = "sk-proj-abcd1234"  # VISIBLE IN REPO!
```

### ✅ ALWAYS Do This
```python
import os
from dotenv import load_dotenv

# Load from .env file (for local development)
load_dotenv()

# Get from environment
API_KEY = os.environ.get("NOTION_API_KEY")
if not API_KEY:
    raise ValueError("NOTION_API_KEY environment variable not set")

# Use the key
notion_client = Client(auth=API_KEY)
```

### 🛡️ Environment Setup

**Local Development (.env file)**
```bash
# .env file (NEVER commit this!)
NOTION_API_KEY=secret_12345678
OPENAI_API_KEY=sk-proj-abcd1234
DATABASE_URL=postgresql://user:pass@localhost/db
```

**Production (System Environment)**
```bash
# Windows
set NOTION_API_KEY=secret_12345678

# Mac/Linux  
export NOTION_API_KEY=secret_12345678
```

**Claude Desktop Config (Safe Method)**
```json
{
  "mcpServers": {
    "notion-server": {
      "command": "fastmcp",
      "args": ["run", "notion_server.py"],
      "cwd": "C:/path/to/server",
      "env": {
        "NOTION_API_KEY": "secret_12345678"
      }
    }
  }
}
```

---

## 🛡️ Input Validation

### Basic Validation Pattern
```python
from pydantic import BaseModel, validator, Field
from typing import Optional, List
import re

class ProjectUpdate(BaseModel):
    project_id: str = Field(..., regex="^[a-zA-Z0-9-]+$")
    status: str
    assignees: Optional[List[str]] = None
    
    @validator('status')
    def validate_status(cls, v):
        allowed = ['planning', 'active', 'completed', 'on-hold']
        if v.lower() not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v.lower()
    
    @validator('project_id')
    def validate_project_id(cls, v):
        if len(v) > 100:
            raise ValueError('Project ID too long')
        return v
    
    @validator('assignees', each_item=True)
    def validate_assignees(cls, v):
        if not re.match(r'^[\w._%+-]+@[\w.-]+\.[A-Z|a-z]{2,}$', v):
            raise ValueError(f'Invalid email address: {v}')
        return v

@mcp.tool
async def update_project(update: ProjectUpdate) -> str:
    """Update project with validated inputs"""
    # Input is already validated!
    return f"Updated project {update.project_id}"
```

### SQL Injection Prevention
```python
# WRONG - SQL Injection vulnerable
@mcp.tool
async def query_data(table: str, condition: str) -> list:
    query = f"SELECT * FROM {table} WHERE {condition}"  # DANGER!
    
# RIGHT - Parameterized queries
@mcp.tool
async def query_data(table: str, field: str, value: str) -> list:
    allowed_tables = ['projects', 'users', 'tasks']
    if table not in allowed_tables:
        raise ValueError(f"Invalid table: {table}")
    
    # Use parameterized query
    query = "SELECT * FROM ? WHERE ? = ?"
    return await db.execute(query, [table, field, value])
```

### Path Traversal Prevention
```python
import os
from pathlib import Path

@mcp.tool
async def read_project_file(filename: str) -> str:
    """Read file with path traversal protection"""
    # Define safe base directory
    base_path = Path("/safe/project/files")
    
    # Resolve and validate path
    requested_path = (base_path / filename).resolve()
    
    # Ensure path is within base directory
    if not str(requested_path).startswith(str(base_path)):
        raise ValueError("Invalid file path")
    
    # Additional validation
    if not requested_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    
    return requested_path.read_text()
```

---

## 🔐 Authentication & Authorization

### MCP Server Authentication
```python
from fastmcp.server.auth import EnvBearerAuthProvider

# Basic bearer token auth
mcp = FastMCP(
    "Secure Server",
    auth=EnvBearerAuthProvider()  # Reads FASTMCP_AUTH_TOKEN
)

# Custom auth with validation
class CustomAuthProvider:
    async def validate_token(self, token: str) -> bool:
        # Implement your validation logic
        return token == os.environ.get("VALID_TOKEN")

mcp = FastMCP(
    "Custom Auth Server",
    auth=CustomAuthProvider()
)
```

### Tool-Level Authorization
```python
from functools import wraps

def requires_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Get user context (implementation depends on your auth system)
        user = get_current_user()
        if not user or user.role != "admin":
            raise PermissionError("Admin access required")
        return await func(*args, **kwargs)
    return wrapper

@mcp.tool
@requires_admin
async def delete_all_projects() -> str:
    """Dangerous operation - admin only"""
    # Implementation
```

---

## 🚨 Error Handling & Information Disclosure

### ❌ Don't Expose Sensitive Info
```python
# WRONG - Exposes internal details
try:
    result = await api_call()
except Exception as e:
    return f"Error: {str(e)}"  # May contain API keys, paths, etc!
```

### ✅ Safe Error Messages
```python
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)

@mcp.tool
async def safe_api_call(param: str) -> dict:
    """API call with safe error handling"""
    error_id = str(uuid4())
    
    try:
        return await make_api_call(param)
    except ValidationError as e:
        # User error - safe to show
        return {"error": f"Invalid input: {e.message}"}
    except APIError as e:
        # Log full error internally
        logger.error(f"API Error {error_id}: {e}", exc_info=True)
        # Return safe message to user
        return {"error": f"Service temporarily unavailable (ref: {error_id})"}
    except Exception as e:
        # Log full error internally
        logger.error(f"Unexpected error {error_id}: {e}", exc_info=True)
        # Return generic message
        return {"error": f"An error occurred (ref: {error_id})"}
```

---

## 🔄 Rate Limiting & Resource Protection

### Basic Rate Limiting
```python
from fastmcp.server.middleware import RateLimitMiddleware
from collections import defaultdict
from datetime import datetime, timedelta

# Built-in rate limiting
mcp.add_middleware(RateLimitMiddleware(
    requests_per_minute=60,
    burst_size=10
))

# Custom rate limiting per tool
rate_limit_storage = defaultdict(list)

def rate_limit(max_calls: int, window_minutes: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}"
            now = datetime.now()
            
            # Clean old entries
            rate_limit_storage[key] = [
                t for t in rate_limit_storage[key] 
                if now - t < timedelta(minutes=window_minutes)
            ]
            
            # Check limit
            if len(rate_limit_storage[key]) >= max_calls:
                raise Exception(f"Rate limit exceeded: {max_calls} calls per {window_minutes} minutes")
            
            # Record call
            rate_limit_storage[key].append(now)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@mcp.tool
@rate_limit(max_calls=10, window_minutes=1)
async def expensive_operation(data: str) -> str:
    """Rate-limited expensive operation"""
    # Implementation
```

---

## 📝 Secure Logging

### Logging Configuration
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure secure logging
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Rotate logs to prevent disk filling
    handler = RotatingFileHandler(
        'mcp_server.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Format without sensitive data
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Create sanitizer for logs
def sanitize_for_logging(data: dict) -> dict:
    """Remove sensitive fields from data before logging"""
    sensitive_fields = ['password', 'api_key', 'token', 'secret']
    sanitized = data.copy()
    
    for field in sensitive_fields:
        if field in sanitized:
            sanitized[field] = "***REDACTED***"
    
    return sanitized

@mcp.tool
async def process_user_data(user_data: dict, ctx: Context) -> str:
    """Process data with secure logging"""
    # Log sanitized version
    ctx.info(f"Processing user data: {sanitize_for_logging(user_data)}")
    
    # Process actual data
    result = await process_data(user_data)
    
    return "Data processed successfully"
```

---

## 🛡️ Dependency Security

### Package Management
```bash
# Use pip-audit to check for vulnerabilities
pip install pip-audit
pip-audit

# Keep dependencies updated
pip list --outdated
pip install --upgrade package_name

# Use requirements.txt with versions
fastmcp==1.0.0
httpx==0.24.1
pydantic==2.0.0
```

### Security Scanning in CI/CD
```yaml
# GitHub Actions example
name: Security Scan
on: [push]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run safety check
      run: |
        pip install safety
        safety check
    - name: Run bandit
      run: |
        pip install bandit
        bandit -r . -f json -o bandit-report.json
```

---

## 🔒 Production Deployment Security

### Environment Isolation
```python
# Use different configs for dev/prod
import os

class Config:
    def __init__(self):
        self.env = os.environ.get('ENVIRONMENT', 'development')
        
        if self.env == 'production':
            self.debug = False
            self.log_level = 'WARNING'
            self.require_auth = True
        else:
            self.debug = True
            self.log_level = 'DEBUG'
            self.require_auth = False

config = Config()
```

### Secure Server Configuration
```python
# Production server setup
if __name__ == "__main__":
    import ssl
    
    # Use HTTPS in production
    if os.environ.get('ENVIRONMENT') == 'production':
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain('cert.pem', 'key.pem')
        
        mcp.run(
            host='0.0.0.0',
            port=443,
            ssl=ssl_context,
            debug=False
        )
    else:
        mcp.run(debug=True)
```

---

## 📋 Security Checklist

### Development Phase
- [ ] All API keys in environment variables
- [ ] Input validation on every parameter
- [ ] SQL/NoSQL injection prevention
- [ ] Path traversal protection
- [ ] Rate limiting implemented
- [ ] Error messages don't leak info
- [ ] Logging excludes sensitive data
- [ ] Dependencies scanned for vulnerabilities

### Pre-Production
- [ ] Security audit performed
- [ ] Authentication required for sensitive tools
- [ ] Authorization checks implemented
- [ ] HTTPS configured for production
- [ ] Secrets rotation plan in place
- [ ] Monitoring and alerting configured
- [ ] Incident response plan documented

### Production
- [ ] Regular dependency updates
- [ ] Security patches applied promptly
- [ ] Logs monitored for anomalies
- [ ] Rate limits adjusted based on usage
- [ ] Regular security audits
- [ ] API key rotation schedule

---

## 🚨 Common Security Mistakes to Avoid

1. **Trusting User Input** - Always validate, never trust
2. **Storing Secrets in Code** - Use environment variables
3. **Verbose Error Messages** - Log internally, show generic errors
4. **Missing Rate Limits** - Protect against abuse
5. **Ignoring Dependencies** - Keep them updated and scanned
6. **No Audit Trail** - Log security events
7. **Weak Authentication** - Use strong tokens, rotate regularly
8. **Data in Logs** - Sanitize before logging

---

## 🔥 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [FastAPI Security Guide](https://fastapi.tiangolo.com/tutorial/security/)
- [MCP Security Documentation](https://modelcontextprotocol.io/docs/concepts/security)

---

*Security isn't a feature, it's a mindset. Build it in from the start, and your future self (and users) will thank you.*

**Remember: It's easier to build secure than to secure what's built! 🔒** 