"""Run the ten-case M3 evaluation plan and write structured CSV results."""
from __future__ import annotations

import argparse
import asyncio
import csv
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "m3_evaluation_cases.yaml"
sys.path.insert(0, str(ROOT))

# UTF-8 text that was mis-decoded as cp1252 shows up as runs like "â€‘" (a UTF-8
# lead byte followed by continuation bytes). Match each run by its lead byte's
# length so only well-formed sequences are touched.
# Bytes 0x81, 0x8D, 0x8F, 0x90 and 0x9D have no cp1252 character and arrive as raw
# C1 control characters, so those are accepted as continuation characters too.
_CONTINUATION = (
    re.escape(bytes(range(0x80, 0xC0)).decode("cp1252", errors="ignore"))
    + "\u0080-\u009f"
)
_MOJIBAKE = re.compile(
    f"[Â-ß][{_CONTINUATION}]"
    f"|[à-ï][{_CONTINUATION}]{{2}}"
    f"|[ð-ô][{_CONTINUATION}]{{3}}"
)


def load_cases() -> list[dict]:
    with CASES_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    cases = data.get("test_cases", [])
    if len(cases) != 10:
        raise ValueError(f"M3 evaluation requires exactly 10 cases, found {len(cases)}")
    return cases


def _run_to_bytes(run: str) -> bytes:
    raw = bytearray()
    for char in run:
        try:
            raw += char.encode("cp1252")
        except UnicodeEncodeError:
            raw.append(ord(char))  # undefined cp1252 byte kept as a C1 control
    return bytes(raw)


def _repair_run(match: re.Match[str]) -> str:
    try:
        return _run_to_bytes(match.group()).decode("utf-8")
    except UnicodeError:
        return match.group()


def normalize_text(text: str) -> str:
    """Repair UTF-8 characters that were mis-decoded as cp1252.

    Each suspect run is converted back only if it decodes as valid UTF-8, so
    correct text (curly quotes, subscripts, arrows) is left unchanged.
    """
    return _MOJIBAKE.sub(_repair_run, text)


def keyword_matched(keyword: str, text: str) -> bool:
    """Return True if any "|"-separated alternative of keyword appears in text.

    "similar|comparable" matches either word; a plain keyword matches itself.
    Matching is a case-insensitive substring check.
    """
    lowered = text.lower()
    return any(
        alternative.strip().lower() in lowered
        for alternative in keyword.split("|")
        if alternative.strip()
    )


def missing_keywords(case: dict, text: str) -> list[str]:
    """Return the expected keywords (as written) that text does not satisfy."""
    return [
        keyword
        for keyword in case["expected_keywords"]
        if not keyword_matched(keyword, text)
    ]


async def evaluate(output_path: Path, model: str | None = None) -> tuple[int, int]:
    # Imported here so the keyword helpers and offline tests need no model SDK.
    from src.m3_agent import ask

    output_path.parent.mkdir(parents=True, exist_ok=True)
    passed = 0
    cases = load_cases()
    with output_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "test_case_id",
                "course_id",
                "input",
                "expected_keywords",
                "expected_output",
                "human_review",
                "critic_score",
                "actual_output",
                "pass_fail",
                "failure_category",
                "missing_keywords",
            ],
        )
        writer.writeheader()
        for case in cases:
            try:
                response = normalize_text(
                    await ask(case["course_id"], case["question"], model)
                )
                missing = missing_keywords(case, response)
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
                    "expected_output": case["expected_output"],
                    "human_review": "",
                    "critic_score": "",
                    "actual_output": response,
                    "pass_fail": status,
                    "failure_category": failure_category,
                    "missing_keywords": "; ".join(missing),
                }
            )
            if missing:
                print(f"{case['id']}: {status} (missing: {', '.join(missing)})")
            else:
                print(f"{case['id']}: {status}")
    return passed, len(cases)


def main() -> None:
    # Windows consoles default to a legacy code page; keep printed output UTF-8.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Run the M3 ten-case evaluation")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "docs" / "evaluation_results_m4.csv",
        help="Results CSV to write (default: docs/evaluation_results_m4.csv)",
    )
    parser.add_argument("--model", default=None, help="Model name override")
    args = parser.parse_args()
    passed, total = asyncio.run(evaluate(args.output, args.model))
    print(f"Overall pass rate: {passed}/{total} ({passed / total:.0%})")


if __name__ == "__main__":
    main()
