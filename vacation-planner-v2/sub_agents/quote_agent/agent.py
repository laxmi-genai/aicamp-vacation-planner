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

import random
from google.adk.agents import LlmAgent

TRAVEL_QUOTES = [
    "The world is a book and those who do not travel read only one page.",
    "Not all those who wander are lost.",
    "Life is either a daring adventure or nothing at all.",
    "Take only memories, leave only footprints.",
    "Travel is the only thing you buy that makes you richer.",
]

def get_travel_quote() -> str:
    """Returns a random travel quote."""
    return random.choice(TRAVEL_QUOTES)

quote_agent = LlmAgent(
    name="QuoteAgent",
    model="gemini-2.5-flash",
    instruction="You provide inspiring travel quotes.",
    description="An agent that can provide travel quotes.",
    tools=[get_travel_quote],
)
