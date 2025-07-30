#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 UI MODULE - Gradio Interface for AI Agents
# ═══════════════════════════════════════════════════════════════════════════════
# Purpose: Encapsulate all Gradio UI setup and styling
# Functions: launch_ui, chat_fn, format_agent_response, format_final_answer, format_regular_response, find_available_port
# ═══════════════════════════════════════════════════════════════════════════════

# ────────────────────────────────────────────────────────────────────────────────
# 📦 IMPORTS
# ────────────────────────────────────────────────────────────────────────────────
import gradio as gr
import socket
import typer


# ┌─────────────────────────────────────────────────────────────────────────────┐
# 🚀 FUNCTION: launch_ui
# └─────────────────────────────────────────────────────────────────────────────┘
# Purpose: Initialize and launch the Gradio chat interface for the agent
# Parameters:
#   agent: Initialized LangChain agent object
#   meta: Dict containing agent metadata (name, expertise, task)
#   host: Server host address
#   port: Server port number
# ────────────────────────────────────────────────────────────────────────────────
def launch_ui(agent, meta: dict, host: str, port: int):
    """
    Setup Gradio ChatInterface and launch the server.
    """
    agent_name = meta.get('name', 'Agent')

    # Chat handler
    def chat_fn(message, history):
        """
        Process a user message through the agent and return formatted response with updated history.
        """
        try:
            raw = agent.run(message)
            formatted = format_agent_response(raw, meta)
            history = history or []
            history.append((message, formatted))
            return formatted, history
        except Exception as e:
            error_msg = f"🚨 **System Error**\n```\n{str(e)}\n```"
            return error_msg, history


    # Define interface
    demo = gr.ChatInterface(
        fn=chat_fn,
        title=f"🤖 **{agent_name}** - AI Agent",
        description=f"""
**🎯 Expertise:** {meta.get('expertise', 'General')}  
**📝 Primary Task:** {meta.get('task', 'Assistant')}

---
💡 **Quick Start Examples:**
""",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="slate",
            neutral_hue="slate",
            font=gr.themes.GoogleFont("Inter")
        ),
        examples=[
            f"Hello! I need help with {meta.get('expertise', 'general tasks').lower()}",
            "What are your main capabilities?",
            "Can you explain your expertise area?",
            "Show me an example of what you can do",
            f"Help me with a {meta.get('task', 'task').lower()} challenge"
        ]
    )
    # Custom CSS
    demo.css = r'''
    .contain { max-width: 1200px; margin: auto; }
    .gradio-container { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    /* ...existing styling... */
    '''
    typer.echo(f"🌐 Launching agent '{agent_name}' on http://{host}:{port}")
    demo.launch(server_name=host, server_port=port)


# ┌─────────────────────────────────────────────────────────────────────────────┐
# 🎨 FUNCTION: format_agent_response
# └─────────────────────────────────────────────────────────────────────────────┘
# Purpose: Beautify raw agent output with markdown, code, and list formatting
# Parameters:
#   raw_response: Raw string response from the agent
#   agent_meta: Dictionary containing agent metadata
# Returns:
#   Formatted response string
# ────────────────────────────────────────────────────────────────────────────────
def format_agent_response(raw_response: str, agent_meta: dict) -> str:
    response = str(raw_response).strip()
    formatted = f"🤖 **{agent_meta.get('name', 'Agent')}** ({agent_meta.get('expertise', 'General')})\n\n"
    if "```" in response:
        formatted += response
    elif response.startswith("Observation:") or (response.startswith("[") and "processing" in response):
        formatted += f"💭 **Agent Thinking:**\n```\n{response}\n```\n\n✨ **Response:** Processing..."
    elif "Final Answer:" in response:
        parts = response.split("Final Answer:")
        formatted += format_final_answer(parts[-1].strip())
    elif any(k in response.lower() for k in ["error","cannot","unable","failed"]):
        formatted += f"⚠️ **Notice:**\n{response}\n\n💡 **Tip:** Try related queries."
    else:
        formatted += format_regular_response(response)
    return formatted


# ┌─────────────────────────────────────────────────────────────────────────────┐
# 🎯 FUNCTION: format_final_answer
# └─────────────────────────────────────────────────────────────────────────────┘
# Purpose: Format the 'Final Answer' section from agent's chain-of-thought
# Parameters:
#   answer: The final answer string from the agent
# Returns:
#   Formatted final answer string
# ────────────────────────────────────────────────────────────────────────────────
def format_final_answer(answer: str) -> str:
    lines = answer.split('\n')
    out = ''
    for line in lines:
        if line.strip().startswith(('- ','• ')):
            out += f"  {line.strip()}\n"
        else:
            out += f"{line}\n"
    return out


# ┌─────────────────────────────────────────────────────────────────────────────┐
# 📝 FUNCTION: format_regular_response
# └─────────────────────────────────────────────────────────────────────────────┘
# Purpose: Format standard paragraphs and lists in responses
# Parameters:
#   response: The raw response string from the agent
# Returns:
#   Formatted response string with proper paragraph and list handling
# ────────────────────────────────────────────────────────────────────────────────
def format_regular_response(response: str) -> str:
    paras = [p.strip() for p in response.split('\n\n') if p.strip()]
    out = ''
    for p in paras:
        if p.startswith('- '):
            out += f"  {p}\n"
        else:
            out += f"{p}\n\n"
    return out


# ┌─────────────────────────────────────────────────────────────────────────────┐
# ⚙️ FUNCTION: find_available_port
# └─────────────────────────────────────────────────────────────────────────────┘
# Purpose: Scan for an open port starting from a default
# Parameters:
#   start_port: Initial port to test
# Returns:
#   Available port integer or raises OSError
# ────────────────────────────────────────────────────────────────────────────────
def find_available_port(start_port: int = 7860) -> int:
    for p in range(start_port, start_port+100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', p))
                typer.echo(f"✅ Found available port: {p}")
                return p
        except OSError:
            continue
    raise OSError(f"No ports free in {start_port}-{start_port+99}")
