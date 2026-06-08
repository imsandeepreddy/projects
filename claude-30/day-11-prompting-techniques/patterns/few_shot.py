import anthropic

client = anthropic.Anthropic()

def classify_alert(alert_text: str) -> str:
    examples = [
        {
            "alert": "CPU usage 95% on prod-web-01 for 10 minutes",
            "classification": "SEV2 | Resource exhaustion | Immediate action required"
        },
        {
            "alert": "SSL certificate expires in 3 days for api.example.com",
            "classification": "SEV3 | Certificate management | Schedule renewal today"
        },
        {
            "alert": "Disk at 60% on dev-db-01",
            "classification": "SEV4 | Disk usage | Monitor, no immediate action"
        }
    ]

    few_shot_content = "\n\n".join([
        f"Alert: {e['alert']}\nClassification: {e['classification']}"
        for e in examples
    ])

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"""{few_shot_content}

Alert: {alert_text}
Classification:"""
        }]
    )
    return response.content[0].text