from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools.google_search_agent_tool import google_search  # pre-built too;


# custom tool
def get_current_time() -> dict:  # need to specify a return type
    # a docstring helps the agent understand what the tool does and when to call it
    """
    Get the current time in the format YYY-MM-DD HH:MM:SS
    """
    # return results in a dict as specific and as instructional as possible; ADK does swrap the result in a dict {result: "..."}
    return {"current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


root_agent = Agent(
    name="tool_agnet",
    model="gemini-2.0-flash",  # gemini-2.0-flash doesn't support mixing built-in tools with function tools with agent, but gemini-2.0-flash-exp supports the AgentTool functionality
    description="An agent that uses tools to answer questions about the current time and perform Google searches",
    instruction="""
    You are an helpful assistant that can use the google_search_agent_tool tool to 
    to perform Google searches for information when answering questions.
    """,
    tools=[google_search],  # built-in
    # tools=[get_current_time],  # custom tool
)
