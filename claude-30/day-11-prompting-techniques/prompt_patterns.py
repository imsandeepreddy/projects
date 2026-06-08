from patterns.chain_of_thought import analyze_incident
from patterns.few_shot import classify_alert
from patterns.xml_structured import review_terraform

SAMPLE_LOG = """
2024-01-15 14:32:01 ERROR db-pool: connection timeout after 30s
2024-01-15 14:32:02 ERROR api: failed to fetch user data - upstream timeout
2024-01-15 14:32:03 ERROR gateway: 503 returned to client - dependency unavailable
"""

SAMPLE_TF = """
resource "aws_db_instance" "main" {
  password = "hardcoded-secret-123"
  publicly_accessible = true
}
"""

if __name__ == "__main__":
    print("=== Chain of Thought ===")
    print(analyze_incident(SAMPLE_LOG))

    print("\n=== Few Shot ===")
    print(classify_alert("Memory at 98% on prod-db-01, OOM killer triggered"))

    print("\n=== XML Structured ===")
    result = review_terraform(SAMPLE_TF)
    print(result)