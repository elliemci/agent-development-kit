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

## Basic Agent:

1. **init**.py

Import the agent module: from . import agent
This makes the agent discoverable by ADK

2. agent.py

Define a variable named root_agent
This is the entry point that ADK uses to find agent

3. Command Location

Always run adk commands from the parent directory containing agent folder;
`adk` shows all command options
`adk web` spin off the FastAPI server with Web UI which makes an end point to sent requess to the agent

This structure ensures that ADK can automatically discover and load the agent when running commands like adk web or adk run.

4. Access the web UI by opening the URL shown in terminal, typically http://localhost:8000

5. Select an agent from dropdown menu in top-left corner of the UI

6. Start chatting with selected agent in textbox at the bottom of the screen

7. Exit the conversation or stop the server with Ctrl+C in terminal.

### Key Components

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

## Agent with Tools

### Type of Tools:

1. Built-in Tools, only work with Gemini models:

- **Google Search**: google_search tool searches the web
- **Code Execution**: built_in_code_execution tool runs code snippets
- **RAG queries with Vertex AI**: vertex_ai_search_tool searches though own data

**Note**: Currently, only one built-in tool at a time for each root agent

2. Function calling tools:

- **Functions/ Methods**
- **Agents-as Tools**
- **Long Running Function Tools**

3. Third-Party Tools

## LiteLLM Agent

LiteLLM is a Python library that provides a unified interface for interacting with multiple LLM provides through a single API which allows:

- Access to 100+ different LLMs from Providers like OpenAI, Anthropic, AWS Bedrock, etc
- Standardize inputs and outputs across different LLM providers
- Track costs, manage API keys and handle errors
- Implement fallbacks and load balancing across different models

LiteLLM enhances ADK nodel-agnostic capability by providing easy switch between LLM providers without changing agent code.

**Note**: The limitation of integrating non-Google models with ADK is that only cutom function tools can be used, there is no access to Google built-in tools like google search, code execution and Vertex Ai serach

LiteLLM agent demonstrates how to use LiteLLM with ADK with models provided by OpenRouter. A model is specified by provider/model_family/specific_model_number. An OpenRouter account is needed and OPENROUER_API_KEY variable in .env file.

## Structured Output Agent

Structured Output Agent uses structured data formats for inputs and outputs implemented with Pydantic:

1. **Controlled Output Format**: Using output_schema LLM producaes consistent responces in JSON structure
2. **Data Validation**: correct formatted fileds with Pydantic validation
3. **Improved downstream processing**: structured outputs are easier to handle by other agents

### Email Generator Agent

The user provides a description of the email they need, agent processes this request and generates both a subject and body
The agent formats its response as a JSON object matching the EmailContent schema. ADK validates the response against the schema before returning it. The structured output is stored in the session state under the specified output_key.

The structured output is produced with Pydantic BaseModel which defines the required fields and their description:

1. Email Subject: a concise relevant subject line
2. Email Body: greeting, paragraoh and signature

### Structured Data Exchange

Structured outputs are part of ADK's broader support for structured data exchange, which includes:

1. **input_schema**: expected input format, easy to fail when rigit structure expected, not used by the email generation agent
2. **output_schema**: define required output format as a Pydantic BaseModel class
3. **output_key**: Store the result in session state for use by other agents

Also see

- [ADK Structured Data Documentation](https://google.github.io/adk-docs/agents/llm-agents/#structuring-data-input_schema-output_schema-output_key)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/why/)

## Session, State and Runners in ADK

**Session** is a statefull message history.
**Runner** conects Agents and Session

Stateful agent with memory manages a sessions and maintain context, remembering user information across interactions. The agent can store information and create contextual and personalized experiences.

ADK Session:

1. Maintain State: Store and access user data, preferences, and other information between interactions
2. Track Conversation History: Automatically record and retrieve message history
3. Personalize Responses: Use stored information to create more contextual and personalized agent experiences

### Question and answering agent

respondes base on stored user information in the session state. Stateful_session.py:

- Creating a session with user preferences
- Using template variables to access session state in agent instructions
- Running the agent with a session to maintain context

### Project structure:

stateful-agent-memory/
│
├── stateful_session.py # Main script
│
└── qa_agent/ # Agent implementation
├── **init**.py
└── agent.py # Agent definition with

### Run

`python stateful_session.py`

This will:

1. Create a new session with user information
2. Initialize the agent with access to that session
3. Process a user query about the stored preferences
4. Display the agent's response based on the session data

Only use runner.run for testing, and always runner.run_async for realworld applications

## Agent with persistent storage

ADK provides `DatabaseSessionService`, intitalized with a database URL that allows to store session and state data in a SQLite database file:

1. Long-term Memory: Information persists across application restarts
2. Consistent User Experiences: Users can continue conversations where they left off
3. Multi-user Support: Different users' data remains separate and secure
4. Scalability: Works with production databases for high-scale deployments

`DatabseSessionService` supports various database backends through SQLAlchemy:

- PostgreSQL: postgresql://user:password@localhost/dbname
- MySQL: mysql://user:password@localhost/dbname
- MS SQL Server: mssql://user:password@localhost/dbname

### Session Managment

If there is an existing session, use it otherwise create a new one

### State Managments with tools

The agent has tools that update the persistent state, where wach change to tool_context. stae is saved to database

### Project Structure

persistent-storage-agent/
│
├── memory_agent/ # Agent package
│ ├── **init**.py # Required for ADK to discover the agent
│ └── agent.py # Agent definition with reminder tools
│
├── main.py # Application entry point with database session setup
├── utils.py # Utility functions for terminal UI and agent interaction
├── .env # Environment variables
├── agent_data.db # SQLite database file created when first run

### Run

`python main.py`

Which will:

1. Connect to the SQLite database, or create it if it doesn't exist
2. Check for previous sessions for the user
3. Start a conversation with the memory agent
4. Save all interactions to the database

## Multi-Agent System

ADK focusses on delegation by the root agent, each agent focuses on specific domain or functionality, and when deligated a quiery to it generates the result. There is no itteration between agents at basic level ADK multiagent sytems.

### Project Structure

ADK multi-agent system project should follow the structure:
root agent package and sub-agents directory, where each agent's **init**.py properly imports its respective agent.py and root agent imports sub-agents in order to use them

parent_folder/
├── root_agent_folder/ # agent package like "manager"
│ ├── **init**.py # import agent.py
│ ├── agent.py # define root_agent
│ ├── .env # environment variables
│ └── sub_agents/ # directory for all sub-agents
│ ├── **init**.py # empty or imports sub-agents
│ ├── agent_1_folder/ # sub-agent package
│ │ ├── **init**.py # import agent.py
│ │ └── agent.py # define an agent variable
│ ├── agent_2_folder/
│ │ ├── **init**.py
│ │ └── agent.py
│ └── ...

### Run

The multi-agent system runs from parent direcotry with `adk web` . The web UI is access from http://localhost:8000 selecting manager agent form dropdown menu in the top-left

### Multi-Agent Architecture Options

1. **Sub-Agent delegation**
   where the root agent acts as a router and sub-agent takes over the query handling

2. **Agent-as-a-Tool**
   with `AgentTool` wrapper, agents can be used as tools by other agents, root agent maintains control, can call different tools

### Limitations

Built-in tools CAN NOT be used within a sub-agent, use `AgentTool` to wrap agents as tools instead, thus allowing the root agent to delegate to specialized agents that each uses a single buil-in tool.

### Manager Agent with three specialized agents

1. Stock Analyst Sub-Agent: provides financial information and stock market insights
2. Funny Nerd Sub-agent: creates nerdy jokes about technical topics
3. News Analyst Agent Tool: gives summaries of current technology news

The manager agent routes queries to the appropriate specialist based on the content of the user's request.

## Stateful Multi-Agent Systems

Is a state-management multi-agent system which distributes tasks among specialized agents while storing information about users and conversations across interactions.

Customer service system is an example of an online course platform, where specialized agents handle different aspects of customer support while sharing a common state.

### Project Structure

stateful-multi-agent/
│
├── customer_service_agent/ # Main agent package
│ ├── **init**.py # Required for ADK discovery
│ ├── agent.py # Root agent definition
│ └── sub_agents/ # Specialized agents
│ ├── course_support_agent/ # Handles course content questions
│ ├── order_agent/ # Manages order history and refunds
│ ├── policy_agent/ # Answers policy questions
│ └── sales_agent/ # Handles course purchases
│
├── main.py # Application entry point with session setup
├── utils.py # Helper functions for state management
├── .env # Environment variables

### Components

1. Session Management
   The example uses `InMemorySessionService` to store session state

2. State Sharing Across Agents
   All agents in the system can access the same session state, enabling:

- Root agent to track interaction history
- Sales agent to update purchased courses
- Course support agent to check if user has purchased specific courses
- All agents to personalize responses based on user information

3. Multi-Agent Delegation
   The customer service agent routes queries to specialized sub-agents

### THe way the system works

1. Initial Session Creation:
   - A new session is created with user information and empty interaction history
   - Session state is initialized with default values
2. Conversation Tracking:
   - Each user message is added to interaction_history in the state
   - Agents can review past interactions to maintain context
3. Query Routing:
   - The root agent analyzes the user query and decides which specialist should handle it
   - Specialized agents receive the full state context when delegated to
4. State Updates:
   - When a user purchases a course, the sales agent updates purchased_courses
   - These updates are available to all agents for future interactions
5. Personalized Responses:
   - Agents tailor responses based on purchase history and previous interactions
   - Different paths are taken based on what the user has already purchased

### Run

To run the stateful multi-agent
`python main.py`

This will:

1. Initialize a new session with default state
2. Start an interactive conversation with the customer service agent
3. Track all interactions in the session state
4. Allow specialized agents to handle specific queries

#### Example Conversation Flow

Conversation flow to test the system:

1. Start with a general query:

   - "What courses do you offer?"
   - Root agent will route to sales agent

2. Ask about purchasing:

   - "I want to buy the AI Marketing Platform course"
   - Sales agent will process the purchase and update state

3. Ask about course content:

   - "Can you tell me about the content in the AI Marketing Platform course?"
   - Root agent will route to course support agent, which now has access

4. Ask about refunds:
   - "What's your refund policy?"
   - Root agent will route to policy agent

The system remembers your purchase across different specialized agents

## Advanced Features

1. Interaction History Tracking
   The system maintains a history of interacction to provide context

2. Dynamic Access Control
   THe system implements conditional access to certain agents:

   - For questions about course content
   - Only available for courses the user has purchased
   - Check if "ai_marketing_platform" is in the purchased courses before directing here

3. State-Based Personalization
   All agents tailor responses are based on session state:
   Tailor your responses based on the user's purchase history and previous interactions.
   When the user hasn't purchased any courses yet, encourage them to explore the AI Marketing Platform.
   When the user has purchased courses, offer support for those specific courses.

## Production Considerations

For a production implementation, consider:

1. Persistent Storage: Replace InMemorySessionService with DatabaseSessionService to persist state across application restarts
2. User Authentication: Implement proper user authentication to securely identify users
3. Error Handling: Add robust error handling for agent failures and state corruption
4. Monitoring: Implement logging and monitoring to track system performance
