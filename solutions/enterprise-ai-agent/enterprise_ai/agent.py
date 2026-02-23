# Copyright 2026 Google LLC
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

import re
import google.auth
from dotenv import load_dotenv
load_dotenv()

from google.cloud import discoveryengine_v1
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams
from google.adk.tools import ToolContext, FunctionTool
from google.apps import chat_v1
from google.oauth2.credentials import Credentials

MODEL = "gemini-2.5-flash"

# Gemini Enterprise authentication injects a bearer token into the ToolContext state.
# The key pattern is "GE_AUTH_NAME_<random_digits>".
# We dynamically parse this token to authenticate our MCP and API calls.
GE_AUTH_NAME = "enterprise-ai"

VERTEXAI_SEARCH_TIMEOUT = 15.0

def get_project_id():
    """Fetches the consumer project ID from the environment natively."""
    _, project = google.auth.default()
    if project:
        return project
    raise Exception(f"Failed to resolve GCP Project ID from environment.")

def find_serving_config_path():
    """Dynamically finds the default serving config in the engine."""
    project_id = get_project_id()
    engines = discoveryengine_v1.EngineServiceClient().list_engines(
        parent=f"projects/{project_id}/locations/global/collections/default_collection"
    )
    for engine in engines:
        # engine.name natively contains the numeric Project Number
        return f"{engine.name}/servingConfigs/default_serving_config"
    raise Exception(f"No Discovery Engines found in project {project_id}")

def _get_access_token_from_context(tool_context: ToolContext) -> str:
    """Helper method to dynamically parse the intercepted bearer token from the context state."""
    escaped_name = re.escape(GE_AUTH_NAME)
    pattern = re.compile(fr"^{escaped_name}_\d+$")
    # Handle ADK varying state object types (Raw Dict vs ADK State)
    state_dict = tool_context.state.to_dict() if hasattr(tool_context.state, 'to_dict') else tool_context.state
    matching_keys = [k for k in state_dict.keys() if pattern.match(k)]
    if matching_keys:
        return state_dict.get(matching_keys[0])
    raise Exception(f"No bearer token found in ToolContext state matching pattern {pattern.pattern}")

def auth_header_provider(tool_context: ToolContext) -> dict[str, str]:
    token = _get_access_token_from_context(tool_context)
    return {"Authorization": f"Bearer {token}"}

def send_direct_message(email: str, message: str, tool_context: ToolContext) -> dict:
    """Sends a Google Chat Direct Message (DM) to a specific user by email address."""
    chat_client = chat_v1.ChatServiceClient(
        credentials=Credentials(token=_get_access_token_from_context(tool_context))
    )

    # 1. Setup the DM space or find existing one
    person = chat_v1.User(
        name=f"users/{email}",
        type_=chat_v1.User.Type.HUMAN
    )
    membership = chat_v1.Membership(member=person)
    space_req = chat_v1.Space(space_type=chat_v1.Space.SpaceType.DIRECT_MESSAGE)
    setup_request = chat_v1.SetUpSpaceRequest(
        space=space_req,
        memberships=[membership]
    )
    space_response = chat_client.set_up_space(request=setup_request)
    space_name = space_response.name
    
    # 2. Send the message
    msg = chat_v1.Message(text=message)
    message_request = chat_v1.CreateMessageRequest(
        parent=space_name,
        message=msg
    )
    message_response = chat_client.create_message(request=message_request)
    
    return {"status": "success", "message_id": message_response.name, "space": space_name}

vertexai_mcp = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://discoveryengine.googleapis.com/mcp",
        timeout=VERTEXAI_SEARCH_TIMEOUT,
        sse_read_timeout=VERTEXAI_SEARCH_TIMEOUT
    ),
    tool_filter=['search'],
    # The auth_header_provider dynamically injects the bearer token from the ToolContext
    # into the MCP call for authentication.
    header_provider=auth_header_provider
)

# Answer nicely the following user queries:
#  - Please find my meetings for today, I need their titles and links
#  - What is the latest Drive file I created?
#  - What is the latest Gmail message I received?
#  - Please send the following message to someone@example.com: Hello, this is a test message.

root_agent = LlmAgent(
    model=MODEL,
    name='enterprise_ai',
    instruction=f"""
        You are a helpful assistant that always uses the Vertex AI MCP search tool to answer the user's message, unless the user asks you to send a message to someone.
        If the user asks you to send a message to someone, use the send_direct_message tool to send the message.
        You MUST unconditionally use the Vertex AI MCP search tool to find answer, even if you believe you already know the answer or believe the Vertex AI MCP search tool does not contain the data.
        The Vertex AI MCP search tool accesses the user's data through datastores including Google Drive, Google Calendar, and Gmail.
        Only use the Vertex AI MCP search tool with servingConfig and query parameters, do not use any other parameters.
        Always use the servingConfig {find_serving_config_path()} while using the Vertex AI MCP search tool.
    """,
    tools=[vertexai_mcp, FunctionTool(send_direct_message)]
)
