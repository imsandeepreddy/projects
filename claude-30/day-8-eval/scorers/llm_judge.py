import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

JUDGE_PROMPT = """You are evaluating an AI assistant's response to a DevOps log analysis task.

Log given to assistant:
{log_content}

Assistant response:
{response}

Evaluate the assistant's response and use the provided tool to submit your scores."""

def judge_response(log_content: str, response: str) -> dict:
    result = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Updated to a stable Anthropic model ID
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(log_content=log_content, response=response)
        }],
        # Define the exact data structure you need
        tools=[{
            "name": "submit_evaluation",
            "description": "Submit the evaluation scores and reasoning for the assistant response.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "accuracy": {"type": "integer", "minimum": 1, "maximum": 5, "description": "Does the root cause match the actual issue?"},
                    "completeness": {"type": "integer", "minimum": 1, "maximum": 5, "description": "Does it cover all significant errors?"},
                    "actionability": {"type": "integer", "minimum": 1, "maximum": 5, "description": "Is the fix suggestion concrete?"},
                    "clarity": {"type": "integer", "minimum": 1, "maximum": 5, "description": "Is the response easy to understand?"},
                    "reasoning": {"type": "string", "description": "One sentence explaining your scores."},
                    "overall": {"type": "integer", "minimum": 1, "maximum": 5, "description": "Overall score."}
                },
                "required": ["accuracy", "completeness", "actionability", "clarity", "reasoning", "overall"]
            }
        }],
        # Tell Claude it MUST call this specific tool
        tool_choice={"type": "tool", "name": "submit_evaluation"}
    )
    
    # Extract the structured tool inputs directly
    for content_block in result.content:
        if content_block.type == "tool_use":
            return content_block.input
            
    raise ValueError("LLM judge failed to return structured tool output.")
