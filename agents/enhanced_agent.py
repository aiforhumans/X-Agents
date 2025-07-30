"""""""""""
# Agent Name: enhanced_agent
# Expertise: AI Assistant
# Task: Provides enhanced formatted responses
# Created: 2025-07-30 18:40:06
"""""""""""
#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# 🧬 TEMPLATE AGENT - Base Template for All Generated Agents
# ═══════════════════════════════════════════════════════════════════════════════
# Purpose: Provides template structure for dynamically created agents
# Function: get_agent - Returns configured LangChain agent
# ═══════════════════════════════════════════════════════════════════════════════

from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import sys
import typer
from pathlib import Path
from instruct_agent import InstructAgent
from ui import launch_ui, find_available_port
import gradio as gr
import textwrap

# ┌─ Configuration Import ─┐
# Add parent directory to path for config import
sys.path.append(str(Path(__file__).parent.parent))
from config import get_lm_studio_config, DEFAULT_AGENT_TYPE

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ 🤖 GET AGENT FUNCTION - Main agent factory                                 │
# └─────────────────────────────────────────────────────────────────────────────┘
def get_agent(name: str, expertise: str, task: str):
    """
    🤖 Factory function to create configured LangChain agent
    
    📋 Parameters:
        🏷️  name: Agent's unique identifier
        🎯 expertise: Domain of specialization  
        📝 task: Primary function description
        
    📋 Returns:
        🔧 Configured LangChain AgentExecutor
        
    📋 Components:
        🧠 LLM: ChatOpenAI (LM Studio)
        🛠️  Tools: Domain-specific functions
        💾 Memory: Conversation history
        ⚙️  Config: Agent behavior settings
    """
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ 🧠 LLM CONFIGURATION - Language model setup                            │
    # └─────────────────────────────────────────────────────────────────────────┘
    
    # ┌─ Load Configuration ─┐
    config = get_lm_studio_config()
    
    # ┌─ Initialize LLM ─┐
    llm = ChatOpenAI(
        openai_api_base=config["openai_api_base"],     # 🌐 LM Studio endpoint
        openai_api_key=config["openai_api_key"],       # 🔑 API key
        model_name=config["model_name"],               # 🤖 Model identifier
        temperature=config["temperature"]              # 🌡️  Response creativity
    )

    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ 🛠️  TOOL CONFIGURATION - Agent capabilities                           │
    # └─────────────────────────────────────────────────────────────────────────┘
    
    # ┌─ Enhanced Tool Function ─┐
    def tool_fn(input_text: str) -> str:
        """
        🛠️ Enhanced tool function with structured output
        
        📋 Purpose: Process input through agent's expertise filter with better formatting
        📋 Input: User query or command
        📋 Output: Structured response with agent context and capabilities
        """
        # ┌─ Generate structured response ─┐
        response = f"""
**{name}** ({expertise}) Analysis:

🔍 **Input Received:** {input_text}

📋 **Processing Steps:**
1. Analyzing query through {expertise.lower()} lens
2. Applying domain-specific knowledge
3. Generating contextual response

✨ **Capabilities Available:**
- {task}
- Domain expertise in {expertise.lower()}
- Contextual problem-solving
- Structured information delivery

💡 **Response:** I'm ready to help with your {expertise.lower()} needs. Please provide more specific details about what you'd like assistance with.
"""
        return response.strip()

    # ┌─ Configure Tools ─┐
    tools = [
        Tool(
            name=f"{name}_tool",                        # 🏷️  Tool identifier
            func=tool_fn,                               # 🔧 Tool function
            description=f"Handles {task}"               # 📝 Tool description
        )
    ]

    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ 💾 MEMORY CONFIGURATION - Conversation persistence                     │
    # └─────────────────────────────────────────────────────────────────────────┘
    
    # ┌─ Initialize Memory ─┐
    memory = ConversationBufferMemory(
        memory_key="chat_history",                      # 🔑 Memory key
        return_messages=True                            # 📋 Return message format
    )

    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ ⚙️  AGENT ASSEMBLY - Combine all components                           │
    # └─────────────────────────────────────────────────────────────────────────┘
    
    # ┌─ Create Agent ─┐
    agent = initialize_agent(
        tools,                                          # 🛠️  Available tools
        llm,                                           # 🧠 Language model
        agent=DEFAULT_AGENT_TYPE,                      # 🤖 Agent type
        verbose=True,                                  # 📋 Debug output
        memory=memory                                  # 💾 Conversation memory
    )
    
    # ┌─ Return Configured Agent ─┐
    return agent

def launch(
    agent_name: str = typer.Argument(..., help="🤖 Agent name to launch"),
    host: str = typer.Option("127.0.0.1", help="🌐 Host address"),
    port: int = typer.Option(7860, help="🔌 Port number")
):
    """
    🚀 Launch agent with Gradio web interface
    """
    # 🔎 Find an available port
    try:
        port = find_available_port(port)
    except OSError as e:
        typer.echo(f"❌ [ERROR] {e}")
        raise typer.Exit(1)
        
    # 📋 Load metadata
    manager = InstructAgent()
    try:
        metadata = manager.get_agent_metadata(agent_name)
    except Exception as e:
        typer.echo(f"❌ [ERROR] {e}")
        raise typer.Exit(1)

    # 🧠 Initialize agent
    agent = get_agent(
        name=metadata["name"],
        expertise=metadata["expertise"],
        task=metadata["task"]
    )

    # 🌐 Launch UI
    launch_ui(agent, host, port)
