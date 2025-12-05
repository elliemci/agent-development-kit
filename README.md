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

## Agent with Callbacks

Callbacks are functionsthat execute at specific points in the agent'slifecycle used to intercept and modify agent behavior at different stages of execution. They can

1. Monitor and Log: Track agent activity and performance metrics
2. Filter Content: Block inappropriate requests or responses
3. Transform Data: Modify inputs and outputs in the agent workflow
4. Implement Security Policies: Enforce compliance and safety measures
5. Add Custom Logic: Insert business-specific processing into the agent flow

### ADK Callback Parameters and Context

#### CallbackContext

The CallbackContext object is provided to all callback types and contains:

- `agent_name`: The name of the agent being executed
- `invocation_id`: A unique identifier for the current agent invocation
- `state`: Access to the session state, allowing you to read/write persistent data
- `app_name`: The name of the application
- `user_id`: The ID of the current user
- `session_id`: The ID of the current session

Examples: # Access the state to store or retrieve data
user_name = callback_context.state.get("user_name", "Unknown")

      # Log the current agent and invocation
      print(f"Agent {callback_context.agent_name} executing (ID: {callback_context.invocation_id})")

#### ToolContext

The ToolContext object is provided to tool callbacks and contains:

agent_name: The name of the agent that initiated the tool call
state: Access to the session state, allowing tools to read/modify shared data
properties: Additional properties specific to the tool execution

Example: # Record tool usage in state
tools_used = tool_context.state.get("tools_used", [])
tools_used.append(tool.name)
tool_context.state["tools_used"] = tools_used

#### LlmRequest

The LlmRequest object is provided to the before_model_callback and contains:

- `contents`: List of Content objects representing the conversation history
- `generation_config`: Configuration for the model generation
- `safety_settings`: Safety settings for the model
- `tools`: Tools provided to the model

#### LlmResponse

The LlmResponse object is returned from the model and provided to the after_model_callback:

- content: Content object containing the model's response
- tool_calls: Any tool calls the model wants to make
- usage_metadata: Metadata about the model usage like tokens

### Types of Callbacks

included in the project

This project includes three examples of the six callback patterns [Types of Callbacks](https://google.github.io/adk-docs/callbacks/types-of-callbacks/):

1. Agent Callbacks: before_after_agent/

- Before Agent Callback: Runs at the start of agent processing
- After Agent Callback: Runs after the agent completes processing

2. Model Callbacks: before_after_model/

- Before Model Callback: Intercepts requests before they reach the LLM
- After Model Callback: Modifies responses after they come from the LLM

3. Tool Callbacks: before_after_tool/

- Before Tool Callback: Modifies tool arguments or skips tool execution
- After Tool Callback: Enhances tool responses with additional information

### Project Structure

agent-with-callbacks/
│
├── before_after_agent/ # Agent callback example
│ ├── **init**.py # Required for ADK discovery
│ └──agent.py # Agent with agent callbacks
│
├── before_after_model/ # Model callback example
│ ├── **init**.py # Required for ADK discovery
│ └── agent.py # Agent with model callbacks
│
└── before_after_tool/ # Tool callback example
├── **init**.py # Required for ADK discovery
└── agent.py # Agent with tool callbacks

### Run

`cd agent-with-callbacks`
`adk web`

Select an agent from the dropdown menu in the wen UI

## Workflows

ADK offers different types of workflow agents:

- **Sequential Agents**: for strict ordered execution
- **Loop Agents**: for repeated execution of sub-agents based on conditions
- **Parallel Agents**: for concurrent execution of independent sub-agents

## Sequential Workflow Agent

Sequential Agents are workflow agents in ADK that:

1. Execute in a Fixed Order: Sub-agents run one after another in the exact sequence they are specified
2. Pass Data Between Agents: Using state management to pass information from one sub-agent to the next
3. Create Processing Pipelines: Perfect for scenarios where each step depends on the previous step's output

Use Sequential Agents for a deterministic, step-by-step workflow where the execution order matters.

### Lead Qualification Pipeline

`lead_qualification_agent` as a Sequential Agent that implements a lead qualification pipeline for sales teams. This Sequential Agent orchestrates three specialized sub-agents:

1. Lead Validator Agent: Checks if the lead information is complete enough for qualification

- Validates for required information like contact details and interest
- Outputs a simple "valid" or "invalid" with a reason

2. Lead Scorer Agent: Scores valid leads on a scale of 1-10

- Analyzes factors like urgency, decision-making authority, budget, and timeline
- Provides a numeric score with a brief justification

3. Action Recommender Agent: Suggests next steps based on the validation and score

- For invalid leads: Recommends what information to gather
- For low-scoring leads (1-3): Suggests nurturing actions
- For medium-scoring leads (4-7): Suggests qualifying actions
- For high-scoring leads (8-10): Suggests sales actions

lead_qualification_agent Sequential Agent orchestrates this process by:

1. Running the Validator first to determine if the lead is complete
2. Running the Scorer next (which can access validation results via state)
3. Running the Recommender last (which can access both validation and scoring results)

The output of each sub-agent is stored in the session state using the output_key parameter:

`validation_status`
`lead_score`
`action_recommendation`

### Project Structure

sequential-workflow/
│
├── lead_qualification_agent/ # Main Sequential Agent package
│ ├── **init**.py # Package initialization
│ ├── agent.py # Sequential Agent definition (root_agent)
│ │
│ └── subagents/ # Sub-agents folder
│ ├── **init**.py # Sub-agents initialization
│ │
│ ├── validator/ # Lead validation agent
│ │ ├── **init**.py
│ │ └── agent.py
│ │
│ ├── scorer/ # Lead scoring agent
│ │ ├── **init**.py
│ │ └── agent.py
│ │
│ └── recommender/ # Action recommendation agent
│ ├── **init**.py
│ └── agent.py
│
└── .env.example # Environment variables example

### Run

`cd sequential-workflow`
`adk web`

**Qualified Lead** Example:

Lead Information:
Name: Sarah Johnson
Email: sarah.j@techinnovate.com
Phone: 555-123-4567
Company: Tech Innovate Solutions
Position: CTO
Interest: Looking for an AI solution to automate customer support
Budget: $50K-100K available for the right solution
Timeline: Hoping to implement within next quarter
Notes: Currently using a competitor's product but unhappy with performance

**Unqualified Lead** Example

Lead Information:
Name: John Doe
Email: john@gmail.com
Interest: Something with AI maybe
Notes: Met at conference, seemed interested but was vague about needs

## Loop Agent

The LinkedIn Post Generator uses a sequential pipeline with a loop component to:

1. Generate an initial LinkedIn post
2. Iteratively refine the post until quality requirements are met

It demonstrates several key patterns:

1. Sequential Pipeline: A multi-step workflow with distinct stages
2. Iterative Refinement: Using a loop to repeatedly refine content
3. Automatic Quality Checking: Validating content against specific criteria
4. Feedback-Driven Refinement: Improving content based on specific feedback
5. Loop Exit Tool: Using a tool to terminate the loop when quality requirements are met

### WorkfLow Architecture

The system is composed of the following components:

#### Root Sequential Agent

LinkedInPostGenerationPipeline - A SequentialAgent that orchestrates the overall process:

1. First runs the initial post generator
2. Then executes the refinement loop

#### Initial Post Generator

`InitialPostGenerator` - An LlmAgent that creates the first draft of the LinkedIn post with no prior context.

#### Refinement Loop

PostRefinementLoop - A LoopAgent that executes a two-stage refinement process:

1. First runs the reviewer to evaluate the post and possibly exit the loop
2. Then runs the refiner to improve the post if the loop continues

#### Sub-Agents Inside the Refinement Loop

1. Post Reviewer (PostReviewer) - Reviews posts for quality and provides feedback or exits the loop if requirements are met
2. Post Refiner (PostRefiner) - Refines the post based on feedback to improve quality

#### Tools

1. Character Counter - Validates post length against requirements (used by the Reviewer)
2. Exit Loop - Terminates the loop when all quality criteria are satisfied (used by the Reviewer)

#### Loop Control with Exit Tool

A key design pattern in this example is the use of an exit_loop tool to control when the loop terminates. The Post Reviewer has two responsibilities:

1. Quality Evaluation: Checks if the post meets all requirements
2. Loop Control: Calls the exit_loop tool when the post passes all quality checks

When the exit_loop tool is called:

- It sets tool_context.actions.escalate = True
- This signals to the LoopAgent that it should stop iterating

This approach follows ADK best practices by:

- Separating initial generation from refinement
- Giving the quality reviewer direct control over loop termination
- Using a dedicated agent for post refinement
- Using a tool to manage the loop control flow
  Usage
  To run this example:

cd loop-workflow
adk web

Then in the web interface, enter a prompt like: "Generate a LinkedIn post about what I've learned from Agent Development Kit tutorial."

The system will:

1. Generate an initial LinkedIn post
2. Review the post for quality and compliance with requirements
3. If the post meets all requirements, exit the loop
4. Otherwise, provide feedback and refine the post
5. Continue this process until a satisfactory post is created or max iterations reached
6. Return the final post

Example Input

Generate a LinkedIn post about what I've learned from Agent Development Kit tutorial.

The loop terminates in one of two ways:

1. When the post meets all quality requirements, reviewer calls the exit_loop tool
2. After reaching the maximum number of iterations
