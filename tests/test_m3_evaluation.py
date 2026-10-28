"""Offline checks for the M3 evaluation plan."""
from __future__ import annotations

from scripts.evaluate_m3 import load_cases


def test_m3_evaluation_contains_ten_unique_cases():
    cases = load_cases()
    assert len({case["id"] for case in cases}) == 10
    assert all(
        case["question"]
        and case["expected_keywords"]
        and case["expected_output"]
        and case["success_judgment"]
        for case in cases
    )
