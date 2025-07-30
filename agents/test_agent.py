"""""""""""
# Agent Name: test_agent
# Expertise: Python Development
# Task: Code review and debugging assistance
"""""""""""

# agents/template_agent.py

from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import sys
from pathlib import Path

# Add parent directory to path for config import
sys.path.append(str(Path(__file__).parent.parent))
from config import get_lm_studio_config, get_agent_config

def get_agent(name: str, expertise: str, task: str):
    """
    Returns a LangChain agent configured based on provided metadata.

    Args:
        name: Agent's name
        expertise: Domain of expertise
        task: Description of the primary task
    """
    # Instantiate the LLM (LM Studio endpoint configured via env)
    llm_config = get_lm_studio_config()
    agent_config = get_agent_config()
    
    llm = ChatOpenAI(
        openai_api_base=llm_config["openai_api_base"],
        openai_api_key=llm_config["openai_api_key"],
        model_name=llm_config["model_name"],
        temperature=llm_config["temperature"]
    )

    # Example tool stub (extend per expertise/task)
    def tool_fn(input_text: str) -> str:
        return f"[{name} ({expertise}) processing]: {input_text}"

    tools = [
        Tool(
            name=f"{name}_tool",
            func=tool_fn,
            description=f"Handles {task}"
        )
    ]

    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = initialize_agent(
        tools, llm,
        agent=agent_config["agent_type"],
        verbose=agent_config["verbose"],
        memory=memory
    )
    return agent
