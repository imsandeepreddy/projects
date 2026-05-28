#!/usr/bin/env python3
import os
import anthropic
from dotenv import load_dotenv
import json
import subprocess
import shlex
import argparse

# 1. Parse command line arguments first
parser = argparse.ArgumentParser(description="SRE AI Agent with dry-run protection.")
parser.add_argument(
    "--dry-run", 
    action="store_true", 
    help="Simulate file writes and structural updates without modifying disk or cluster state."
)
args = parser.parse_args()

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
       "name": "write_file_contents",
       "description": "Overwrite or create a local file with new content. Respects dry-run protection mode.",
       "input_schema": {
           "type": "object",
           "properties": {
               "path": {"type": "string", "description": "File path to write to"},
               "content": {"type": "string", "description": "The exact full text content to write"}
           },
           "required": ["path", "content"]
       }
   },
   {
       "name": "run_shell_command",
       "description": "Run whitelisted shell command.",
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

def write_file_contents(path: str, content: str) -> dict:
    """Updates or creates a local file. Blocks execution if --dry-run is active."""
    if args.dry_run:
        print(f"\n[DRY RUN] Would write the following content to '{path}':")
        print("-" * 40)
        print(content)
        print("-" * 40)
        return {
            "path": path, 
            "status": "dry-run-skipped", 
            "message": "[DRY RUN ENABLED] File changes were simulated and logged but not saved to disk."
        }
        
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"path": path, "status": "success", "message": "File updated successfully."}
    except Exception as e:
        return {"error": f"Failed to write file: {str(e)}"}

WHITELIST = {"ls", "cat", "head", "echo", "kubectl"}

def run_shell_command(command: str) -> dict:
    """
    Executes a shell command safely if the base command is whitelisted.
    Automatically appends --dry-run flags to critical kubernetes mutation tasks if active.
    """
    try:
        parsed_args = shlex.split(command)
        if not parsed_args:
            return {"error": "Empty command provided."}
            
        base_command = parsed_args[0]
        
        if base_command not in WHITELIST:
            return {
                "error": f"Command '{base_command}' is not whitelisted.",
                "whitelisted_commands": list(WHITELIST)
            }
            
        # Intercept and protect cluster mutation if running in dry-run mode
        if args.dry_run and base_command == "kubectl" and "apply" in parsed_args:
            if "--dry-run=client" not in parsed_args and "--dry-run=server" not in parsed_args:
                parsed_args.append("--dry-run=client")
                command = shlex.join(parsed_args)
                print(f"[DRY RUN] Appended safety flag. Executing: {command}")
                
        result = subprocess.run(
            parsed_args, 
            capture_output=True, 
            text=True, 
            timeout=15 
        )
        
        return {
            "command": command,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Command execution timed out after 15 seconds."}
    except Exception as e:
        return {"error": f"Execution failed: {str(e)}"}


available_tools = {
    "get_file_contents": get_file_contents,
    "write_file_contents": write_file_contents,
    "run_shell_command": run_shell_command
}

messages = [{"role": "user", "content": "Analyze the application state. Read sample.log, use kubectl tools to inspect our running system if needed, find the configuration mismatch, and fix configmap.yaml."}]

# Inform system prompt if it is operating inside a simulation
mode_instruction = "IMPORTANT: Dry-run execution framework is active. File mutations will be captured locally via console stdout." if args.dry_run else "Standard operational mode active. Modifications write straight to infrastructure."

while True:
    response = client.messages.create(
       model="claude-haiku-4-5-20251001",
       max_tokens=2048, 
       system=f"""
        You are an elite SRE AI assistant. Your goal is to detect and resolve infrastructure anomalies.
        {mode_instruction}
        When given an issue:
        1. Examine local files (`sample.log`, configurations) using file tools.
        2. Execute `kubectl` commands (e.g., `kubectl get pods`, `kubectl describe pod <name>`, `kubectl logs`) to see live runtime contexts.
        3. Identify the root cause (e.g., configuration variable mismatches).
        4. Fix the local file (`configmap.yaml`) using the `write_file_contents` tool.
        5. Use `kubectl apply -f configmap.yaml` and `kubectl rollout restart` via shell to apply changes to cluster.
        Be precise. Output a final summary with: Root Cause, Fix Applied, Action Taken.
       """,
       tools=tools,
       messages=messages
    )

    messages.append({
        "role": "assistant",
        "content": response.content
    })

    if response.stop_reason == "end_turn":
       for block in response.content:
           if block.type == "text":
               print(block.text)
       break
    elif response.stop_reason == "tool_use":
       tool_blocks = [b for b in response.content if b.type == "tool_use"]
       
       tool_results_content = []
       for tool_block in tool_blocks:
           tool_name = tool_block.name
           tool_input = tool_block.input
           tool_id = tool_block.id
           
           print(f"\n[AI Tool Call] {tool_name} with args: {tool_input}")
           
           if tool_name in available_tools:
               result_dict = available_tools[tool_name](**tool_input)
           else:
               result_dict = {"error": f"Tool '{tool_name}' is not implemented locally."}
               
           print(f"[Tool Response]: {result_dict}\n")
           
           tool_results_content.append({
               "type": "tool_result",
               "tool_use_id": tool_id,
               "content": json.dumps(result_dict)
           })
           
       messages.append({
           "role": "user",
           "content": tool_results_content
       })
