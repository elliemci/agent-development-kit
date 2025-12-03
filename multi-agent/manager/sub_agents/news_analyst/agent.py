from google.adk.agents import Agent
from google.adk.tools import google_search

# Since the agent uses Build-in tool it can not be imported as sub-agent,
# but it needs to be wrapped with AgentTool and use as a tool, its replay
# is passed back to the parent agent, which summarizes the answer and generates
# a response to the user

news_analyst = Agent(
    name="news_analyst",
    model="gemini-2.0-flash",
    description="News analyst agent",
    instruction="""
    You are a helpful assistant that can analyze news articles and provide a summary of the news.

    When asked about news, you should use the google_search tool to search for the news.

    If the user ask for news using a relative time, you should use the get_current_time tool to get the current time to use in the search query.
    
    Delegate back to manager agent for any no news related queries.
    """,
    tools=[google_search],
)
