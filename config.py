#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIG - Configuration Management for LM Studio and Agents
# ═══════════════════════════════════════════════════════════════════════════════
# Purpose: Centralized configuration for LLM endpoints and agent settings
# Functions: get_lm_studio_config, get_agent_config
# ═══════════════════════════════════════════════════════════════════════════════

import os
from typing import Dict, Any

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ ⚙️ DEFAULT CONFIGURATION - Base settings for the system                   │
# └─────────────────────────────────────────────────────────────────────────────┘

# ┌─ Agent Configuration Defaults ─┐
DEFAULT_AGENT_TYPE = "chat-zero-shot-react-description"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MODEL_NAME = "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF"

# ┌─ LM Studio Configuration Defaults ─┐
DEFAULT_LM_STUDIO_BASE = "http://localhost:1234/v1"
DEFAULT_API_KEY = "not-needed"

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ 🌐 LM STUDIO CONFIGURATION - LLM endpoint settings                        │
# └─────────────────────────────────────────────────────────────────────────────┘
def get_lm_studio_config() -> Dict[str, Any]:
    """
    🌐 Get LM Studio configuration with environment variable overrides
    
    📋 Returns:
        📊 Dictionary containing LLM configuration
        
    📋 Environment Variables:
        🌐 OPENAI_API_BASE: LM Studio endpoint URL
        🔑 OPENAI_API_KEY: API key (usually 'not-needed' for local)
        🤖 MODEL_NAME: Model identifier
        🌡️  TEMPERATURE: Response creativity (0.0-1.0)
    """
    return {
        "openai_api_base": os.getenv("OPENAI_API_BASE", DEFAULT_LM_STUDIO_BASE),
        "openai_api_key": os.getenv("OPENAI_API_KEY", DEFAULT_API_KEY),
        "model_name": os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME),
        "temperature": float(os.getenv("TEMPERATURE", DEFAULT_TEMPERATURE))
    }

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ 🤖 AGENT CONFIGURATION - Agent behavior settings                          │
# └─────────────────────────────────────────────────────────────────────────────┘
def get_agent_config() -> Dict[str, Any]:
    """
    🤖 Get agent configuration settings
    
    📋 Returns:
        📊 Dictionary containing agent behavior settings
    """
    return {
        "agent_type": os.getenv("AGENT_TYPE", DEFAULT_AGENT_TYPE),
        "verbose": os.getenv("AGENT_VERBOSE", "true").lower() == "true",
        "max_iterations": int(os.getenv("AGENT_MAX_ITERATIONS", "3")),
        "timeout": int(os.getenv("AGENT_TIMEOUT", "30"))
    }

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ 🔧 UTILITY FUNCTIONS - Configuration helpers                              │
# └─────────────────────────────────────────────────────────────────────────────┘
def validate_lm_studio_connection() -> bool:
    """
    🔍 Validate if LM Studio is accessible
    
    📋 Returns:
        ✅ True if connection is successful, False otherwise
    """
    try:
        import requests
        config = get_lm_studio_config()
        
        # ┌─ Test Connection ─┐
        response = requests.get(
            f"{config['openai_api_base']}/models",
            timeout=5
        )
        return response.status_code == 200
        
    except Exception:
        return False

def get_available_models() -> list:
    """
    📋 Get list of available models from LM Studio
    
    📋 Returns:
        📊 List of model identifiers
    """
    try:
        import requests
        config = get_lm_studio_config()
        
        # ┌─ Fetch Models ─┐
        response = requests.get(
            f"{config['openai_api_base']}/models",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            return [model["id"] for model in data.get("data", [])]
        else:
            return []
            
    except Exception:
        return []

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ 📋 CONFIGURATION DISPLAY - Debug and info functions                       │
# └─────────────────────────────────────────────────────────────────────────────┘
def display_config():
    """
    📋 Display current configuration for debugging
    """
    print("🌐 LM Studio Configuration:")
    print("═══════════════════════════════════════")
    lm_config = get_lm_studio_config()
    for key, value in lm_config.items():
        print(f"  {key}: {value}")
    
    print("\n🤖 Agent Configuration:")
    print("═══════════════════════════════════════")
    agent_config = get_agent_config()
    for key, value in agent_config.items():
        print(f"  {key}: {value}")
    
    print(f"\n🔍 LM Studio Connection: {'✅ Active' if validate_lm_studio_connection() else '❌ Inactive'}")

if __name__ == "__main__":
    display_config()