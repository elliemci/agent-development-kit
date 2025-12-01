import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# check avilable OenrRouter models at https://openrouter.ai/models
# choose cheap or free models for testing with OpenRouter free tier


# To use Grok 4.1 from xAI through OpenRouter
xai_model = LiteLlm(
    model="openrouter/x-ai/grok-4.1-fast:free", api_key=os.getenv("OPENROUTER_API_KEY")
)

# To use GPT-4o from OpenAI through OpenRouter
openai_model = LiteLlm(
    model="openrouter/openai/gpt-4o", api_key=os.getenv("OPENROUTER_API_KEY")
)
# To use Claude 3.5 Sonnet from Anthropic through OpenRouter
anthropic_model = LiteLlm(
    model="openrouter/anthropic/claude-3-5-sonnet",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_tokens=1000,
)

# To use Llama 3 70B from Meta through OpenRouter
meta_llama_model = LiteLlm(
    model="openrouter/meta-llama/meta-llama-3-70b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# To use Mistral Large through OpenRouter
mistral_model = LiteLlm(
    model="openrouter/mistral/mistral-large-latest",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

root_agent = Agent(
    name="joke_generating_agent",
    model=xai_model,
    description="Joke generating agent",
    instruction="""
    You are a funny joke generating agent. 
    Your task is to find out what kind of joke a user likes and 
    generate as funny as possible joke of that type.""",
)
