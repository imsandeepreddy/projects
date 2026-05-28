#!/usr/bin/env python3
import os
import json
import anthropic
from dotenv import load_dotenv
import json
from scorers.rule_based import score_response
from scorers.llm_judge import judge_response

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def run_system_under_test(log_content: str) -> str:
    # Call your Day 5 log assistant here
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="You are an SRE assistant. Analyse logs, identify root cause, suggest fix.",
        messages=[{"role": "user", "content": f"Analyse this log:\n{log_content}"}]
    )
    return response.content[0].text

def run_evals(dataset_path: str):
    with open(dataset_path) as f:
        dataset = json.load(f)
    results = []
    for test_case in dataset:
        print(f"Running {test_case['id']}...")
        response = run_system_under_test(test_case["log_content"])
        rule_scores = score_response(response, test_case)
        judge_scores = judge_response(test_case["log_content"], response)
        results.append({
            "id": test_case["id"],
            "difficulty": test_case["difficulty"],
            "response": response,
            "rule_scores": rule_scores,
            "judge_scores": judge_scores
        })
    return results

def print_summary(results: list):
    total = len(results)
    passed = sum(1 for r in results if r["rule_scores"]["overall_pass"])
    avg_judge = sum(r["judge_scores"]["overall"] for r in results) / total
    print(f"\n{'='*50}")
    print(f"EVAL SUMMARY")
    print(f"{'='*50}")
    print(f"Total tests:     {total}")
    print(f"Rule-based pass: {passed}/{total} ({passed/total*100:.0f}%)")
    print(f"Avg judge score: {avg_judge:.1f}/5")
    # Break down by difficulty
    for difficulty in ["easy", "medium", "hard"]:
        subset = [r for r in results if r["difficulty"] == difficulty]
        if subset:
            avg = sum(r["judge_scores"]["overall"] for r in subset) / len(subset)
            print(f"  {difficulty}: {avg:.1f}/5 ({len(subset)} cases)")

if __name__ == "__main__":
    results = run_evals("datasets/log_samples.json")
    print_summary(results)
    with open("results/latest_run.json", "w") as f:
        json.dump(results, f, indent=2)