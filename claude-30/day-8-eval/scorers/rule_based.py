def score_response(response: str, test_case: dict) -> dict:
   scores = {}
   # Check 1 — did it identify a root cause at all?
   scores["has_root_cause"] = (
       "root cause" in response.lower() or
       "caused by" in response.lower() or
       "reason" in response.lower()
   )
   # Check 2 — does response mention expected keywords?
   keywords_found = [
       kw for kw in test_case["expected_fix_keywords"]
       if kw.lower() in response.lower()
   ]
   scores["keyword_coverage"] = len(keywords_found) / len(
       test_case["expected_fix_keywords"]
   )
   # Check 3 — does it include a fix suggestion?
   scores["has_fix_suggestion"] = any(word in response.lower() for word in [
       "fix", "solution", "resolve", "update", "change", "increase", "check"
   ])
   # Check 4 — response length sanity check
   scores["appropriate_length"] = 50 < len(response.split()) < 500
   scores["overall_pass"] = (
       scores["has_root_cause"] and
       scores["keyword_coverage"] >= 0.5 and
       scores["has_fix_suggestion"]
   )
   return scores