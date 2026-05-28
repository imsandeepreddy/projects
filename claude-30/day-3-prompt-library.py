#!/usr/bin/env python3
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
#------------- Role + expertise level -----------------------------#
def call(system, user):
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=system,
        messages=[{"role": "user", "content": user}]
    )
    return r.content[0].text
# Test: same question, different roles
#junior = "You are a junior DevOps engineer with 1 year of experience. Explain things simply."
#senior = "You are a principal SRE at a FAANG company. Be terse, assume deep expertise."
#q = "How should I handle a Kubernetes pod that keeps OOMKilling?"
#print("JUNIOR:\n", call(junior, q))
#print("SENIOR:\n", call(senior, q))

#------------- Constrained -----------------------------#
constrained = """You are a DevOps assistant.
Rules:
- Never suggest solutions that require downtime
- Always include rollback steps
- Respond only about infrastructure topics; decline anything else
- Maximum 5 bullet points per answer
- Avoid pleasentaries"""

#def call(q):
#    r = client.messages.create(
#        model="claude-haiku-4-5-20251001",
#        max_tokens=512,
#        system=constrained,
#        messages=[{"role": "user", "content": q}]
#    )
#    return r.content[0].text

#print(call("How do I deploy a new version of my API?"))
#print(call("Write me a poem about Kubernetes"))  # should be declined

#-----------------Structured----------------------------------------------#
structured = """You are an incident responder.
Always respond in this exact format:
<severity>P1|P2|P3</severity>
<summary>One sentence description</summary>
<immediate_actions>
  <action>First thing to do</action>
  <action>Second thing to do</action>
</immediate_actions>
<escalate_to>Team or person name</escalate_to>
"""

incident = "Our payment service is returning 503s and error rate is at 45% for the last 10 minutes."
def call(q):
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=structured,
        messages=[{"role": "user", "content": q}]
    )
    return r.content[0].text
raw = call(incident)
print(raw)


