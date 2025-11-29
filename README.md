# ADK Agnet Development

## Setup Environment

```bash
# initialize a project create virutal environment with uv
uv init
uv venv
soure .venv/bin/activate
# install dependencies
uv add google-adk yfinance psutil litellm google-generativeai python-dotenv
```

Agent is a core component in ADK that acts as the "bhining" part of the application. It laverages the power of a LLM for:

Reasoning
Understanding natural language
Making decisions
Generating responses
Interacting with tools

Agent Structure
For ADK to discover and run your agents properly (especially with adk web), your project must follow a specific structure:

parent_folder/
agent_folder/ # agent's package directory
**init**.py # must import agent.py
agent.py # must define root_agent
.env # environment variables

## Essential Components:

1. **init**.py

Must import the agent module: from . import agent
This makes the agent discoverable by ADK

2. agent.py

Must define a variable named root_agent
This is the entry point that ADK uses to find agent

3. Command Location

Always run adk commands from the parent directory, not from inside the agent directory;
`adk` shows all command options
`adk web` spin off the FastAPI server with Web UI which makes an end point to sent requess to the agent

This structure ensures that ADK can automatically discover and load the agent when running commands like adk web or adk run.

## Key Components

1. Identity: name and description

- name (Required): A unique string identifier for your agent
- description (Optional, but recommended): A concise summary of the agent's capabilities. Used for other agents to determine if they should route a task to this agent.

2. Model

- Specifies which LLM powers the agent (e.g., "gemini-2.0-flash")
- Affects the agent's capabilities, cost, and performance

3. Instructions, define:

- Core task or goal
- Personality or persona
- Behavioral constraints
- How to use available tools
- Desired output format

4. Tools
   capabilities beyond the LLM's built-in knowledge, allowing the agent to:

- Interact with external systems
- Perform calculations
- Fetch real-time data
- Execute specific actions
