# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import os
import logging
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
import google.genai.types as types
from .agent import root_agent

load_dotenv()

async def run_single_turn(user_input, session_id, user_id, runner):
    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    async def get_final_response():
        async for event in events:
            if event.is_final_response() and event.content and event.content.parts:
                return event.content.parts[0].text
    return await get_final_response()

async def chat_loop(session_id, user_id, runner) -> None:
    """Main chat interface loop."""
    print("\nStarting chat. Type 'exit' or 'quit' to end.")
    print("Every message will be automatically stored in memory.\n")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("\nAssistant: Thank you for chatting. Have a great day!")
            break

        response = await run_single_turn(user_input, session_id, user_id, runner)
        if response:
            print(f"\nAssistant: {response}")

async def main():
    logging.getLogger("google.adk").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("mcp").setLevel(logging.WARNING)
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    agent_engine_id = os.getenv("AGENT_ENGINE_ID")

    memory_bank_service = VertexAiMemoryBankService(
        project=project, location=location, agent_engine_id=agent_engine_id
    )

    session_service = VertexAiSessionService(
        project=project, location=location, agent_engine_id=agent_engine_id
    )

    runner = Runner(
        agent=root_agent,
        app_name="vacation-planner-v2",
        session_service=session_service,
        memory_service=memory_bank_service,
    )

    USER_ID = "user-001"

    session1 = await runner.session_service.create_session(
        app_name="vacation-planner-v2",
        user_id=USER_ID,
    )

    await chat_loop(session1.id, USER_ID, runner)

    completed_session = await runner.session_service.get_session(
        app_name="vacation-planner-v2", user_id=USER_ID, session_id=session1.id
    )
    await memory_bank_service.add_session_to_memory(completed_session)


if __name__ == "__main__":
    asyncio.run(main())
