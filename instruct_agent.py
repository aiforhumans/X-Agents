#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# 🤖 INSTRUCT AGENT - Agent Management and Metadata Extraction
# ═══════════════════════════════════════════════════════════════════════════════
# Purpose: Provides agent metadata parsing and management functionality
# Functions: InstructAgent class with info() method
# ═══════════════════════════════════════════════════════════════════════════════

import re
from pathlib import Path
from typing import Dict, Any

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ 🤖 INSTRUCT AGENT CLASS - Agent metadata management                        │
# └─────────────────────────────────────────────────────────────────────────────┘
class InstructAgent:
    """
    🤖 Agent management class for metadata extraction and parsing
    
    📋 Features:
        📝 Parse agent metadata from file headers
        🔍 Validate agent file existence
        📋 Extract structured agent information
    """
    
    def __init__(self):
        """
        🚀 Initialize InstructAgent manager
        
        📋 Sets up agent directory path and metadata patterns
        """
        # ┌─ Configuration ─┐
        self.agents_dir = Path("agents")
        
        # ┌─ Metadata Parsing Patterns ─┐
        self.metadata_patterns = {
            'name': r'# Agent Name:\s*(.+)',
            'expertise': r'# Expertise:\s*(.+)', 
            'task': r'# Task:\s*(.+)',
            'created': r'# Created:\s*(.+)'
        }
    
    def info(self, agent_name: str) -> Dict[str, Any]:
        """
        📋 Extract agent metadata from file header
        
        📋 Parameters:
            🤖 agent_name: Name of the agent to analyze
            
        📋 Returns:
            📊 Dictionary containing agent metadata
            
        📋 Raises:
            FileNotFoundError: If agent file doesn't exist
        """
        # ┌─ Construct Agent File Path ─┐
        agent_file = self.agents_dir / f"{agent_name}.py"
        
        # ┌─ Validate File Existence ─┐
        if not agent_file.exists():
            raise FileNotFoundError(f"Agent file not found: {agent_file}")
        
        # ┌─ Read File Content ─┐
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise FileNotFoundError(f"Cannot read agent file {agent_file}: {e}")
        
        # ┌─ Extract Metadata ─┐
        metadata = {}
        
        # ┌─ Parse Each Metadata Field ─┐
        for field, pattern in self.metadata_patterns.items():
            match = re.search(pattern, content)
            if match:
                metadata[field] = match.group(1).strip()
            else:
                # ┌─ Provide Fallback Values ─┐
                fallbacks = {
                    'name': agent_name,
                    'expertise': 'General',
                    'task': 'Assistant',
                    'created': 'Unknown'
                }
                metadata[field] = fallbacks.get(field, 'Unknown')
        
        # ┌─ Add Computed Fields ─┐
        metadata['file_path'] = str(agent_file)
        metadata['agent_id'] = agent_name
        
        return metadata
    
    def list_agents(self) -> list:
        """
        📋 List all available agents in agents directory
        
        📋 Returns:
            📊 List of agent names (without .py extension)
        """
        # ┌─ Find All Agent Files ─┐
        if not self.agents_dir.exists():
            return []
        
        agent_files = list(self.agents_dir.glob("*.py"))
        
        # ┌─ Filter Out Template and Extract Names ─┐
        agents = []
        for agent_file in agent_files:
            agent_name = agent_file.stem
            # ┌─ Skip template files ─┐
            if agent_name not in ['template_agent', '__init__']:
                agents.append(agent_name)
        
        return sorted(agents)
    
    def validate_agent(self, agent_name: str) -> bool:
        """
        ✅ Validate if agent exists and has proper structure
        
        📋 Parameters:
            🤖 agent_name: Name of agent to validate
            
        📋 Returns:
            ✅ True if agent is valid, False otherwise
        """
        try:
            # ┌─ Check File Existence ─┐
            agent_file = self.agents_dir / f"{agent_name}.py"
            if not agent_file.exists():
                return False
            
            # ┌─ Check Basic Content ─┐
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ┌─ Verify get_agent Function Exists ─┐
            if 'def get_agent(' not in content:
                return False
            
            return True
            
        except Exception:
            return False