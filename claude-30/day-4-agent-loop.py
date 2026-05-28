#!/usr/bin/env python3
import os
import anthropic
from dotenv import load_dotenv
import json
import subprocess
import shlex

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)


tools = [
   {
       "name": "get_file_contents",
       "description": "Read contents of a local file.",
       "input_schema": {
           "type": "object",
           "properties": {
               "path": {"type": "string", "description": "File path to read"}
           },
           "required": ["path"]
       }
   },
   {
       "name": "run_shell_command",
       "description": "Run whitelisted shell command",
       "input_schema": {
           "type": "object",
           "properties": {
               "command": {"type": "string", "description": "The command that is to be executed"}
           },
           "required": ["command"]
       }
   }
]

def get_file_contents(path: str) -> dict:
    """Safely reads the contents of a local file."""
    try:
        if not os.path.exists(path):
            return {"error": f"File not found: {path}"}
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"path": path, "file_content": content}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

# Define exact allowed commands (and optionally their allowed base structures)
# For example, only allowing 'ls', 'cat', and 'head'
WHITELIST = {"ls", "cat", "head", "echo"}

def run_shell_command(command: str) -> dict:
    """
    Executes a shell command safely if the base command is whitelisted.
    Uses shlex to parse arguments safely and prevent shell injection.
    """
    try:
        # Split command into a list of arguments safely (handles quotes, spaces)
        args = shlex.split(command)
        if not args:
            return {"error": "Empty command provided."}
            
        base_command = args[0]
        
        # Security check against whitelist
        if base_command not in WHITELIST:
            return {
                "error": f"Command '{base_command}' is not whitelisted.",
                "whitelisted_commands": list(WHITELIST)
            }
            
        # Execute the process safely without shell=True
        # capture_output captures stdout and stderr; text=True handles string decoding
        result = subprocess.run(
            args, 
            capture_output=True, 
            text=True, 
            timeout=10 # Prevent infinite loops or hanging processes
        )
        
        return {
            "command": command,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Command execution timed out after 10 seconds."}
    except Exception as e:
        return {"error": f"Execution failed: {str(e)}"}


available_tools = {
    "get_file_contents": get_file_contents,
    "run_shell_command": run_shell_command
}

messages = [{"role": "user", "content": "Execute the bash commands present in test-commands file"}]

while True:
    #loop till stop_reason is received
    response = client.messages.create(
       model="claude-haiku-4-5-20251001",
       max_tokens=1024,
       tools=tools,
       messages=messages
    )

    messages.append({
        "role": "assistant",
        "content": response.content
    })

    if response.stop_reason == "end_turn":
       # Print out the final answer text blocks
       for block in response.content:
           if block.type == "text":
               print(block.text)
       break
    elif response.stop_reason == "tool_use":
       # Process every tool call request inside this turn
       tool_blocks = [b for b in response.content if b.type == "tool_use"]
       
       tool_results_content = []
       for tool_block in tool_blocks:
           tool_name = tool_block.name
           tool_input = tool_block.input
           tool_id = tool_block.id
           
           print(f"Claude wants to call: {tool_name} with {tool_input}")
           
           if tool_name in available_tools:
               # Dynamically resolve function call arguments matching the tool schema properties
               # schema maps 'path' -> get_file_contents(path=...)
               result_dict = available_tools[tool_name](**tool_input)
           else:
               result_dict = {"error": f"Tool '{tool_name}' is not implemented locally."}
               
           print(f"Tool execution result: {result_dict}")
           
           # Format the result block using the exact ID provided by Claude
           tool_results_content.append({
               "type": "tool_result",
               "tool_use_id": tool_id,
               "content": json.dumps(result_dict)
           })
           
       # 2. Append the user role message containing all tool outcomes back into history
       messages.append({
           "role": "user",
           "content": tool_results_content
       })


#What's the disk usage on prod-server-01?
#response = client.messages.create(
#    model="claude-haiku-4-5-20251001",
#    max_tokens=256,
#    tools=tools,
#    system="You are a senior DevOps engineer. Be concise and use bullet points.",
#    messages=[{"role": "user", "content": "Restart ngnix service on prod-server-01"}]
#)

#tool_block = next(b for b in response.content if b.type == "tool_use")
#tool_name = tool_block.name
#tool_input = tool_block.input
#print(f"Claude wants to call: {tool_name} with {tool_input}")

#def get_disk_usage(server_name: str) -> dict:
#       # Mock — replace with real psutil or SSH call later
#       return {"server": server_name, "disk_usage_pct": 72}
#
#result = get_disk_usage(**tool_input)

#def restart_service(server_name: str, service_name: str) -> bool:
#       # Mock — replace with real logic
#       return True
#
#result = restart_service(**tool_input)
#
#final_response = client.messages.create(
#    model="claude-haiku-4-5-20251001",
#    max_tokens=256,
#    tools=tools,
#    messages=[
#        {"role": "user", "content": "Restart ngnix service on prod-server-01"},
#        {"role": "assistant", "content": response.content},
#        {"role": "user", "content": [
#            {"type": "tool_result", "tool_use_id": tool_block.id, "content": json.dumps(result)}
#        ]}
#    ]
#)
#print(final_response.content[0].text)

