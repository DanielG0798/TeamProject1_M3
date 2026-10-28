"""Run the ten-case M3 evaluation plan and write structured CSV results."""
from __future__ import annotations

import argparse
import asyncio
import csv
from pathlib import Path

import yaml

from src.m3_agent import ask

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "m3_evaluation_cases.yaml"


def load_cases() -> list[dict]:
    with CASES_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    cases = data.get("test_cases", [])
    if len(cases) != 10:
        raise ValueError(f"M3 evaluation requires exactly 10 cases, found {len(cases)}")
    return cases


async def evaluate(output_path: Path, model: str | None = None) -> tuple[int, int]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    passed = 0
    cases = load_cases()
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "test_case_id",
                "course_id",
                "input",
                "expected_keywords",
                "actual_output",
                "pass_fail",
                "failure_category",
            ],
        )
        writer.writeheader()
        for case in cases:
            try:
                response = await ask(case["course_id"], case["question"], model)
                missing = [
                    keyword
                    for keyword in case["expected_keywords"]
                    if keyword.lower() not in response.lower()
                ]
                status = "PASS" if not missing else "FAIL"
                failure_category = "" if not missing else "response_keyword"
            except Exception as error:
                response = f"{type(error).__name__}: {error}"
                status = "FAIL"
                failure_category = "execution"
                missing = list(case["expected_keywords"])
            passed += status == "PASS"
            writer.writerow(
                {
                    "test_case_id": case["id"],
                    "course_id": case["course_id"],
                    "input": case["question"],
                    "expected_keywords": "; ".join(case["expected_keywords"]),
                    "actual_output": response,
                    "pass_fail": status,
                    "failure_category": failure_category,
                }
            )
            if missing:
                print(f"{case['id']}: {status} (missing: {', '.join(missing)})")
            else:
                print(f"{case['id']}: {status}")
    return passed, len(cases)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the M3 ten-case evaluation")
    parser.add_argument("--output", type=Path, default=ROOT / "evaluation_results.csv")
    parser.add_argument("--model", default=None, help="Model name override")
    args = parser.parse_args()
    passed, total = asyncio.run(evaluate(args.output, args.model))
    print(f"Overall pass rate: {passed}/{total} ({passed / total:.0%})")


if __name__ == "__main__":
    main()
