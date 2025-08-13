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
import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from dotenv import load_dotenv

load_dotenv()

flight_server_params = StdioServerParameters(
    command="mcp-flight-search",
    args=["--connection_type", "stdio"],
    env={"SERP_API_KEY": os.getenv("SERP_API_KEY")},
)

flight_search_agent = LlmAgent(
    name="FlightSearchAgent",
    model="gemini-2.5-flash",
    instruction="You are a flight search tool. Your only function is to use the provided tools to search for flights.",
    description="An agent that can search for flights.",
    tools=[MCPToolset(connection_params=flight_server_params),],
)
