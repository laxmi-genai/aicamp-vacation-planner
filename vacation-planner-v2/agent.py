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

from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

# Import the specialist agents we created
from .sub_agents.currency_converter import currency_converter_agent
from .sub_agents.flight_search import flight_search_agent
from .sub_agents.quote_agent import quote_agent


# NOTE: The gemini-2.5-flash model may not support multiple sub-agents of this type.
# Using this configuration may result in a "400 INVALID_ARGUMENT" error.
root_agent = LlmAgent(
    name="PlannerAgent",
    model="gemini-2.5-flash",
    instruction="""You are a master vacation planner. Your goal is to help the user plan a trip.
    You have access to specialist agents that can find information about currency conversion, flights, and travel quotes.

    When the user asks for information, you should:
    1. Determine which specialist agent is needed.
    2. Delegate the task to the appropriate agent.
       - If the user needs some inspiration to travel or is contemplating travel, use the quote agent.
    3. Receive the information from the specialist agent.
    4. Formulate a clear and friendly response to the user based on the information you received.
    5. Do not expose the inner workings of the sub-agents to the user.
    """,
    description="The main vacation planner agent that orchestrates sub-agents.",
    sub_agents=[
        currency_converter_agent,
        flight_search_agent,
        quote_agent,
    ],
    tools=[PreloadMemoryTool()],
)