#!/usr/bin/env python3
"""
EVE-MCP-LAB: Personal Context Manager
====================================

An intelligent context management system that maintains state across conversations,
tracks decisions, and provides contextual insights for enhanced productivity.

This is our first experiment in building Personal AI Toolkit tools that scale
from individual use to executive team management.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

# Initialize our Context Manager MCP server
mcp = FastMCP(
    "Personal Context Manager",
    instructions="Intelligent context management for enhanced productivity and decision-making",
    dependencies=["fastmcp"],
)

# Configuration
CONTEXT_DIR = Path.home() / ".eve-mcp-lab" / "context"
CONTEXT_DIR.mkdir(parents=True, exist_ok=True)

class ContextType(str, Enum):
    """Types of context we can manage"""
    CONVERSATION = "conversation"
    DECISION = "decision"
    PROJECT = "project"
    TASK = "task"
    INSIGHT = "insight"
    RELATIONSHIP = "relationship"

class Priority(str, Enum):
    """Priority levels for context items"""
    CRITICAL = "critical"
    HIGH = "high" 
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class ContextItem:
    """A single context item with metadata"""
    id: str
    type: ContextType
    title: str
    content: str
    priority: Priority
    created_at: datetime
    updated_at: datetime
    tags: List[str]
    connections: List[str]  # IDs of related context items
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextItem':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        data['type'] = ContextType(data['type'])
        data['priority'] = Priority(data['priority'])
        return cls(**data)

class ContextManager:
    """Manages context storage and retrieval"""
    
    def __init__(self):
        self.context_file = CONTEXT_DIR / "context_store.json"
        self.contexts: Dict[str, ContextItem] = {}
        self.load_contexts()

    def load_contexts(self) -> None:
        """Load contexts from disk"""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r') as f:
                    data = json.load(f)
                    self.contexts = {
                        ctx_id: ContextItem.from_dict(ctx_data)
                        for ctx_id, ctx_data in data.items()
                    }
            except Exception as e:
                print(f"Error loading contexts: {e}")
                self.contexts = {}

    def save_contexts(self) -> None:
        """Save contexts to disk"""
        try:
            data = {
                ctx_id: ctx.to_dict()
                for ctx_id, ctx in self.contexts.items()
            }
            with open(self.context_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving contexts: {e}")

    def add_context(self, context: ContextItem) -> None:
        """Add a new context item"""
        self.contexts[context.id] = context
        self.save_contexts()

    def get_context(self, context_id: str) -> Optional[ContextItem]:
        """Get a context by ID"""
        return self.contexts.get(context_id)

    def search_contexts(self, query: str, context_type: Optional[ContextType] = None) -> List[ContextItem]:
        """Search contexts by content, title, or tags"""
        results = []
        query_lower = query.lower()
        
        for context in self.contexts.values():
            if context_type and context.type != context_type:
                continue
                
            if (query_lower in context.title.lower() or 
                query_lower in context.content.lower() or 
                any(query_lower in tag.lower() for tag in context.tags)):
                results.append(context)
        
        return sorted(results, key=lambda x: x.updated_at, reverse=True)

    def get_recent_contexts(self, limit: int = 10, context_type: Optional[ContextType] = None) -> List[ContextItem]:
        """Get recent contexts"""
        contexts = list(self.contexts.values())
        if context_type:
            contexts = [c for c in contexts if c.type == context_type]
        
        return sorted(contexts, key=lambda x: x.updated_at, reverse=True)[:limit]

# Initialize the context manager
context_manager = ContextManager()

@mcp.tool
def add_context(
    title: str,
    content: str,
    context_type: ContextType = ContextType.CONVERSATION,
    priority: Priority = Priority.MEDIUM,
    tags: List[str] = [],
    connections: List[str] = [],
    metadata: Dict[str, Any] = {}
) -> str:
    """
    Add a new context item to the intelligent context store.
    
    Args:
        title: Brief title for the context
        content: Detailed content/description
        context_type: Type of context (conversation, decision, project, etc.)
        priority: Priority level (critical, high, medium, low)
        tags: List of tags for categorization
        connections: List of context IDs this relates to
        metadata: Additional metadata as key-value pairs
    
    Returns:
        The ID of the created context item
    """
    now = datetime.now(timezone.utc)
    context_id = f"{context_type.value}_{now.strftime('%Y%m%d_%H%M%S')}"
    
    context_item = ContextItem(
        id=context_id,
        type=context_type,
        title=title,
        content=content,
        priority=priority,
        created_at=now,
        updated_at=now,
        tags=tags,
        connections=connections,
        metadata=metadata
    )
    
    context_manager.add_context(context_item)
    return f"✅ Context '{title}' added with ID: {context_id}"

@mcp.tool
def search_context(
    query: str,
    context_type: Optional[ContextType] = None,
    limit: int = 10
) -> str:
    """
    Search through stored contexts using natural language.
    
    Args:
        query: Search query (searches title, content, and tags)
        context_type: Optional filter by context type
        limit: Maximum number of results to return
    
    Returns:
        Formatted search results
    """
    results = context_manager.search_contexts(query, context_type)[:limit]
    
    if not results:
        return f"❌ No contexts found matching '{query}'"
    
    output = [f"🔍 Found {len(results)} contexts matching '{query}':\n"]
    
    for i, context in enumerate(results, 1):
        output.append(f"{i}. **{context.title}** ({context.type.value})")
        output.append(f"   Priority: {context.priority.value} | Updated: {context.updated_at.strftime('%Y-%m-%d %H:%M')}")
        output.append(f"   Content: {context.content[:100]}{'...' if len(context.content) > 100 else ''}")
        if context.tags:
            output.append(f"   Tags: {', '.join(context.tags)}")
        output.append("")
    
    return "\n".join(output)

@mcp.tool
def get_recent_context(
    limit: int = 10,
    context_type: Optional[ContextType] = None
) -> str:
    """
    Get recently added or updated contexts.
    
    Args:
        limit: Maximum number of contexts to return
        context_type: Optional filter by context type
    
    Returns:
        Formatted list of recent contexts
    """
    contexts = context_manager.get_recent_contexts(limit, context_type)
    
    if not contexts:
        return "❌ No contexts found"
    
    type_filter = f" ({context_type.value})" if context_type else ""
    output = [f"📋 Recent contexts{type_filter}:\n"]
    
    for i, context in enumerate(contexts, 1):
        output.append(f"{i}. **{context.title}** ({context.type.value})")
        output.append(f"   Priority: {context.priority.value} | Updated: {context.updated_at.strftime('%Y-%m-%d %H:%M')}")
        output.append(f"   Content: {context.content[:100]}{'...' if len(context.content) > 100 else ''}")
        if context.tags:
            output.append(f"   Tags: {', '.join(context.tags)}")
        output.append("")
    
    return "\n".join(output)

@mcp.tool
def get_context_details(context_id: str) -> str:
    """
    Get detailed information about a specific context item.
    
    Args:
        context_id: The ID of the context to retrieve
    
    Returns:
        Detailed context information
    """
    context = context_manager.get_context(context_id)
    
    if not context:
        return f"❌ Context '{context_id}' not found"
    
    output = [f"📄 Context Details: {context.title}\n"]
    output.append(f"**ID:** {context.id}")
    output.append(f"**Type:** {context.type.value}")
    output.append(f"**Priority:** {context.priority.value}")
    output.append(f"**Created:** {context.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    output.append(f"**Updated:** {context.updated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    if context.tags:
        output.append(f"**Tags:** {', '.join(context.tags)}")
    
    if context.connections:
        output.append(f"**Connected to:** {', '.join(context.connections)}")
    
    output.append(f"\n**Content:**\n{context.content}")
    
    if context.metadata:
        output.append(f"\n**Metadata:**")
        for key, value in context.metadata.items():
            output.append(f"  {key}: {value}")
    
    return "\n".join(output)

@mcp.tool
def update_context(
    context_id: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    priority: Optional[Priority] = None,
    tags: Optional[List[str]] = None,
    connections: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Update an existing context item.
    
    Args:
        context_id: ID of the context to update
        title: New title (optional)
        content: New content (optional)
        priority: New priority (optional)
        tags: New tags list (optional)
        connections: New connections list (optional)
        metadata: New metadata (optional)
    
    Returns:
        Confirmation message
    """
    context = context_manager.get_context(context_id)
    
    if not context:
        return f"❌ Context '{context_id}' not found"
    
    # Update fields if provided
    if title is not None:
        context.title = title
    if content is not None:
        context.content = content
    if priority is not None:
        context.priority = priority
    if tags is not None:
        context.tags = tags
    if connections is not None:
        context.connections = connections
    if metadata is not None:
        context.metadata.update(metadata)
    
    context.updated_at = datetime.now(timezone.utc)
    context_manager.save_contexts()
    
    return f"✅ Context '{context.title}' updated successfully"

@mcp.tool
def get_context_stats() -> str:
    """
    Get statistics about the context store.
    
    Returns:
        Formatted statistics
    """
    contexts = list(context_manager.contexts.values())
    
    if not contexts:
        return "📊 Context store is empty"
    
    # Count by type
    type_counts = {}
    for context in contexts:
        type_counts[context.type.value] = type_counts.get(context.type.value, 0) + 1
    
    # Count by priority
    priority_counts = {}
    for context in contexts:
        priority_counts[context.priority.value] = priority_counts.get(context.priority.value, 0) + 1
    
    output = [f"📊 Context Store Statistics\n"]
    output.append(f"**Total Contexts:** {len(contexts)}")
    output.append(f"\n**By Type:**")
    for type_name, count in sorted(type_counts.items()):
        output.append(f"  {type_name}: {count}")
    
    output.append(f"\n**By Priority:**")
    for priority_name, count in sorted(priority_counts.items()):
        output.append(f"  {priority_name}: {count}")
    
    # Most recent
    recent = sorted(contexts, key=lambda x: x.updated_at, reverse=True)[:3]
    output.append(f"\n**Most Recent:**")
    for context in recent:
        output.append(f"  {context.title} ({context.updated_at.strftime('%Y-%m-%d %H:%M')})")
    
    return "\n".join(output)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run() 