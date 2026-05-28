#!/usr/bin/env python3
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

#message = client.messages.create(
#    model="claude-haiku-4-5-20251001",
#    max_tokens=256,
#    messages=[{"role": "user", "content": "Explain Kubernetes operators in one sentence."}]
#)
#print(message.content[0].text)

try:
    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system="You are a senior DevOps engineer. Be concise and use bullet points.",
        messages=[{"role": "user", "content": "Explain Kubernetes operators in 5 sentences."}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
except anthropic.APIConnectionError as e:
    print(e)


