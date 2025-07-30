# X-Agents Development Guide

## Architecture Overview

This is a **LangChain-powered AI agent framework** with modular UI separation and multi-agent orchestration capabilities. The system uses **LM Studio** as the local LLM backend, not OpenAI directly.

### Core Components & Data Flow

1. **CLI Entry** (`app.py`) → **Metadata Parser** (`instruct_agent.py`) → **Dynamic Import** → **Agent Factory** → **UI Launch** (`ui.py`)
2. **Agent Discovery**: File-based with regex metadata extraction from `"""""""""""` headers
3. **Configuration Layer**: Environment-first with fallbacks, centralized in `config.py`
4. **UI Architecture**: Gradio ChatInterface with sophisticated response formatting pipeline

### Core Components

- **`app.py`**: CLI entrypoint using Typer. Dynamic imports agents via `importlib.util`, validates structure, launches UI
- **`config.py`**: Centralized configuration hub for LM Studio endpoints and agent behavior (env overrides supported)  
- **`instruct_agent.py`**: Regex-based metadata parser that extracts structured info from agent file headers
- **`ui.py`**: Complete Gradio ChatInterface with response formatting pipeline (`format_agent_response`, `format_final_answer`)
- **`agents/`**: Agent modules following strict template pattern with metadata headers and `get_agent()` factory
- **`launching_agents/`**: Multi-agent orchestration system (scaffolded, not implemented)

## Agent Development Pattern

### Required Agent Structure
Every agent in `agents/` must follow this **exact** pattern:

```python
"""""""""""
# Agent Name: my_agent
# Expertise: Domain Name  
# Task: What this agent does
# Created: YYYY-MM-DD HH:MM:SS
"""""""""""

def get_agent(name: str, expertise: str, task: str):
    # Must return configured LangChain AgentExecutor
    # Standard components: ChatOpenAI + Tools + ConversationBufferMemory
```

**Critical Requirements:**
- Triple-quoted string with exactly 9 quotes (`"""""""""""`) 
- Headers parsed by regex in `instruct_agent.py`: `r'# Agent Name:\s*(.+)'`
- Function signature must be `get_agent(name: str, expertise: str, task: str)`
- Must return LangChain `AgentExecutor` object

### Configuration Integration Pattern
Agents **must** import config centrally, not hardcode endpoints:

```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # Required for agents/
from config import get_lm_studio_config, DEFAULT_AGENT_TYPE

config = get_lm_studio_config()
llm = ChatOpenAI(
    openai_api_base=config["openai_api_base"],  # LM Studio endpoint
    openai_api_key=config["openai_api_key"],    # Usually "not-needed"  
    model_name=config["model_name"],
    temperature=config["temperature"]
)
```

## Development Workflows

### Creating New Agents
1. **Copy metadata template** from `enhanced_agent.py` (not `test_agent.py` - incomplete config)
2. **Implement `get_agent()` factory** with LangChain components
3. **Test discovery**: `python app.py <agent_name>` (requires agent file to exist)
4. **Auto-discovery**: `InstructAgent().list_agents()` finds all valid agents

### Essential Commands
```powershell
# Launch single agent with UI (REQUIRES AGENT_NAME argument)
python app.py enhanced_agent --host 0.0.0.0 --port 7860

# Test LM Studio connection and view all config
python config.py

# Debug agent metadata parsing
python -c "from instruct_agent import InstructAgent; print(InstructAgent().info('enhanced_agent'))"

# List all discovered agents  
python -c "from instruct_agent import InstructAgent; print(InstructAgent().list_agents())"
```

### Prerequisites for Development
- **LM Studio** must be running on `localhost:1234` (configurable via `OPENAI_API_BASE`)
- Agent files require valid metadata headers for auto-discovery
- UI system expects `launch_ui(agent, meta, host, port)` interface pattern

## Key Conventions

### Unicode & Emoji Headers
Files use consistent decorative headers with Unicode box drawing and emojis:
- `🚀` for main functions, `📋` for parameters/returns, `⚙️` for config
- `┌─────┐` box drawing for section separators
- `# ═══════` for major file headers

### Response Formatting Pipeline
The UI system (`ui.py`) has sophisticated response formatting:
- **Chain-of-thought detection**: Parses "Final Answer:" from LangChain reasoning
- **Agent thinking display**: Code blocks for "Observation:" and processing steps  
- **Structured formatting**: `format_agent_response()` → `format_final_answer()` → `format_regular_response()`
- **Error handling**: `⚠️` warnings with `💡` tips for failed queries
- **Markdown enhancement**: Auto-converts lists, paragraphs, and code blocks

### Environment Configuration
All settings use environment variable overrides:
- `OPENAI_API_BASE` for LM Studio endpoint (default: `http://localhost:1234/v1`)
- `MODEL_NAME`, `TEMPERATURE`, `AGENT_TYPE` for behavior tuning
- `AGENT_VERBOSE`, `AGENT_MAX_ITERATIONS`, `AGENT_TIMEOUT` for execution control

## Integration Points

### LM Studio Dependency
- System assumes LM Studio running locally on port 1234
- Uses OpenAI-compatible API format but connects to local inference
- `validate_lm_studio_connection()` and `get_available_models()` provide health checks

### Dynamic Agent Loading
- `app.py` uses `importlib.util` for runtime module import
- `instruct_agent.py` parses file headers with regex patterns
- Agent discovery is automatic based on file presence in `agents/`

### Multi-Agent Architecture (Planned)
- `launching_agents/` contains scaffolding for parallel agent workflows
- `interaction_tracker.py` and `multi_agent_controller.py` exist but not implemented
- Architecture supports background agent orchestration

## Critical Files to Understand

- **`enhanced_agent.py`**: Reference implementation showing full agent pattern
- **`config.py`**: All environment integration and connection logic  
- **`ui.py`**: Complete Gradio setup and response formatting system
- **`instruct_agent.py`**: Metadata parsing that enables agent auto-discovery
