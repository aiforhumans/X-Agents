#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# 🌐 APP LAUNCHER - Gradio Web Interface for Agents
# ═══════════════════════════════════════════════════════════════════════════════
# Purpose: CLI entrypoint to load agent metadata, initialize agent, and launch UI

import importlib.util
import typer
from pathlib import Path
from instruct_agent import InstructAgent
from ui import launch_ui
import gradio as gr
import textwrap
# Parameters:
#   agent_name: Name of the agent to launch
#   host: Server host address
#   port: Server port number
# ───────────────────────────────────────────────────────────────────────────────
def launch(
    agent_name: str = typer.Argument(..., help="🤖 Agent name to launch"),
    host: str = typer.Option("127.0.0.1", help="🌐 Host address"),
    port: int = typer.Option(7860, help="🔌 Port number")
):
    """
    🚀 Launch agent with Gradio web interface
    """
    # 📋 Load metadata
    manager = InstructAgent()
    try:
        meta = manager.info(agent_name)
        typer.echo(f"📋 Loading agent: {meta['name']}")
        typer.echo(f"🎯 Expertise: {meta['expertise']}")
        typer.echo(f"📝 Task: {meta['task']}")
    except FileNotFoundError as e:
        typer.echo(f"❌ [ERROR] {e}")
        raise typer.Exit(1)

    # 🔧 Validate and load agent module
    agent_file = Path("agents") / f"{agent_name}.py"
    if not agent_file.exists():
        typer.echo(f"❌ [ERROR] Agent file not found: {agent_file}")
        raise typer.Exit(1)
    spec = importlib.util.spec_from_file_location(agent_name, agent_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # ⚙️ Initialize agent
    agent = mod.get_agent(
        name=meta['name'], expertise=meta['expertise'], task=meta['task']
    )
    typer.echo("✅ Agent loaded successfully!")

    # 💬 Launch UI
    # Dedent custom CSS if used in launch_ui
    if hasattr(launch_ui, "custom_css"):
        launch_ui.custom_css = textwrap.dedent(launch_ui.custom_css)
    launch_ui(agent, meta, host, port)

# ┌─────────────────────────────────────────────────────────────────────────────┐
# 🚀 MAIN ENTRY POINT: Run CLI
# └─────────────────────────────────────────────────────────────────────────────┘
if __name__ == "__main__":
    typer.run(launch)
