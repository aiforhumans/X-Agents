# Agents Overview

This document lists all agent modules in the `agents/` folder, summarizing their functions and capabilities.

---

## enhanced_agent.py
**Metadata:**
- **Agent Name:** enhanced_agent
- **Expertise:** AI Assistant
- **Task:** Provides enhanced formatted responses
- **Created:** 2025-07-30 18:40:06

**Main Function:**
- `get_agent(name: str, expertise: str, task: str)`
  - Returns a LangChain agent configured with:
    - **LLM:** ChatOpenAI (LM Studio)
    - **Tool:** Processes input with structured output and context
    - **Memory:** ConversationBufferMemory
    - **Capabilities:**
      - Domain-specific analysis
      - Contextual problem-solving
      - Structured information delivery
      - Enhanced response formatting

---

## test_agent.py
**Metadata:**
- **Agent Name:** test_agent
- **Expertise:** Python Development
- **Task:** Code review and debugging assistance

**Main Function:**
- `get_agent(name: str, expertise: str, task: str)`
  - Returns a LangChain agent configured with:
    - **LLM:** ChatOpenAI
    - **Tool:** Processes input and returns a formatted string indicating agent and expertise
    - **Memory:** ConversationBufferMemory
    - **Capabilities:**
      - Code review
      - Debugging assistance
      - General Python development support

---

## template_agent.py
**Status:** Empty template file. No functions or capabilities defined yet.

---

# How to Add New Agents
- Create a new Python file in `agents/`.
- Add metadata headers:
  - `# Agent Name: ...`
  - `# Expertise: ...`
  - `# Task: ...`
- Implement `get_agent(name: str, expertise: str, task: str)` returning a LangChain agent.
- Document capabilities in this file.
