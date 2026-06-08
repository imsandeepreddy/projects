import anthropic

client = anthropic.Anthropic()

def analyze_incident(log_snippet: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""You are a senior SRE. When analyzing incidents,
think through the problem step by step before giving your conclusion.
Show your reasoning explicitly.""",
        messages=[{
            "role": "user",
            "content": f"""Analyze this log and identify the root cause.
Think through it step by step.

<log>
{log_snippet}
</log>

Steps to follow:
1. Identify the first error signal
2. Trace the cascade of failures
3. Pinpoint the root cause
4. Suggest the fix"""
        }]
    )
    return response.content[0].text