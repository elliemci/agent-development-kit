import asyncio
import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()  # need env variables at the toot folder, since not running adk web

from qa_agent import qa_agent


# creat_session() and get_session() are async methods, either make the script async or use asyncio.run() to run async calls
# to make it fully async, wrap in async def main() amd call asyncio.run(main())
async def main():
    # Create a new session service to store state, there are also data base and Vertex AI storage options
    session_service_stateful = InMemorySessionService()

    initial_state = {
        "user_name": "Ellie McI",
        "user_preferences": """
            I like to trail run, do yoga and hike.
            My favorite food is Thai.
            I dont like watching TV, but like listening to Hidden Brain and Dr. Gundry Podcasts
            Loves to watch educational YouTube videos.
        """,
    }

    # Create a NEW session
    APP_NAME = "Ellie Bot"
    USER_ID = "ellie_mci"
    SESSION_ID = str(uuid.uuid4())  # creates a long unique random character

    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    print("CREATED NEW SESSION:")
    print(f"\tSession ID: {SESSION_ID}")

    runner = Runner(  # list the agents and the session
        agent=qa_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    new_message = types.Content(
        role="user", parts=[types.Part(text="What is Ellie's favorite podcast?")]
    )

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Final Response: {event.content.parts[0].text}")

    print("==== Session Event Exploration ====")
    session = await session_service_stateful.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    # Log final Session state
    print("=== Final Session State ===")
    for key, value in session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
