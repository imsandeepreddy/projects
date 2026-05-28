#!/usr/bin/env python3
import os
import anthropic
from dotenv import load_dotenv
import json

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)


tools = [
   {
       "name": "get_disk_usage",
       "description": "Returns disk usage percentage for a given server name.",
       "input_schema": {
           "type": "object",
           "properties": {
               "server_name": {"type": "string", "description": "The server hostname"}
           },
           "required": ["server_name"]
       }
   },
   {
       "name": "restart_service",
       "description": "Restarts a given service name on a given server name.",
       "input_schema": {
           "type": "object",
           "properties": {
               "server_name": {"type": "string", "description": "The server hostname"},
               "service_name": {"type": "string", "description": "The service name"}
           },
           "required": ["server_name", "service_name"]
       }
   }
]


#What's the disk usage on prod-server-01?
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    tools=tools,
    system="You are a senior DevOps engineer. Be concise and use bullet points.",
    messages=[{"role": "user", "content": "Restart ngnix service on prod-server-01"}]
)

tool_block = next(b for b in response.content if b.type == "tool_use")
tool_name = tool_block.name
tool_input = tool_block.input
print(f"Claude wants to call: {tool_name} with {tool_input}")

#def get_disk_usage(server_name: str) -> dict:
#       # Mock — replace with real psutil or SSH call later
#       return {"server": server_name, "disk_usage_pct": 72}
#
#result = get_disk_usage(**tool_input)

def restart_service(server_name: str, service_name: str) -> bool:
       # Mock — replace with real logic
       return True

result = restart_service(**tool_input)

final_response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    tools=tools,
    messages=[
        {"role": "user", "content": "Restart ngnix service on prod-server-01"},
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tool_block.id, "content": json.dumps(result)}
        ]}
    ]
)
print(final_response.content[0].text)

