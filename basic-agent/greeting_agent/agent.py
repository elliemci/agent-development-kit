from google.adk.agents import Agent

root_agent = Agent(
    # name of root agent must match the name of the dir the agnet.py is in
    name="greeting_agent",
    model="gemini-2.0-flash",  # check out the rest of the google models at https://ai.google.dev/gemini-api/docs/models
    description="Greeting agent",  # used to find out task/ work delegation
    instruction="""
    You are a friendly greeting agent. 
    Your task is to find out the user's name and 
    greet them warmly by name and make them feel welcome.""",
)
