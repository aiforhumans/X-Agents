# GenAI Stack

A LangChain-powered AI agent framework with modular UI separation and enhanced response formatting.

## 🚀 Overview
- **app.py**: CLI launcher using Typer. Loads agent metadata, imports agent module, and starts the UI.
- **ui.py**: Encapsulates all Gradio interface definitions and styling.
- **agents/**: Agent implementations with required metadata headers and `get_agent(name, expertise, task)` function.
- **config.py**: Centralized LM Studio and agent behavior settings (env overrides supported).
- **launching_agents/**: Multi-agent orchestration for parallel workflows.

## 📦 Installation
```powershell
git clone https://github.com/docker/genai-stack.git
cd genai-stack
pip install -r requirements.txt
```

## 🛠 Usage
### Launch single agent
```powershell
python app.py <agent_name> [--host 0.0.0.0] [--port 7860]
```

### Run multi-agent controller
```powershell
cd launching_agents; python multi_agent_controller.py
```

### Inspect configuration
```powershell
python config.py
```

## 📂 Project Structure
```
genai-stack/
├── app.py              # CLI entrypoint
├── ui.py               # Gradio UI module
├── config.py           # Environment-driven settings
├── agents/             # Agent definitions
│   ├── enhanced_agent.py
│   └── template_agent.py
├── launching_agents/   # Multi-agent orchestration
└── requirements.txt
```

## 📖 Contributing
- Follow Unicode & emoji conventions (🚀, 📋, ⚙️) in headers.
- Add new agents under `agents/` with metadata and `get_agent` signature.

_Please submit issues or PRs for improvements and feedback!_
