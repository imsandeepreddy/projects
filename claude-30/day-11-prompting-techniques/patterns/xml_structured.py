import anthropic
import xml.etree.ElementTree as ET

client = anthropic.Anthropic()

def review_terraform(tf_code: str) -> dict:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""You are a Terraform security reviewer.
Always respond using exactly this XML structure, nothing else:
<review>
  <security_issues>
    <issue severity="high|medium|low">description</issue>
  </security_issues>
  <best_practice_violations>
    <violation>description</violation>
  </best_practice_violations>
  <verdict>PASS|FAIL</verdict>
</review>""",
        messages=[{
            "role": "user",
            "content": f"Review this Terraform:\n\n{tf_code}"
        }]
    )

    raw = response.content[0].text
    root = ET.fromstring(raw)

    return {
        "issues": [
            {"severity": i.get("severity"), "text": i.text}
            for i in root.findall(".//issue")
        ],
        "violations": [v.text for v in root.findall(".//violation")],
        "verdict": root.find("verdict").text
    }