"""Offline checks for the M3 evaluation plan."""
from __future__ import annotations

import csv
from pathlib import Path

from scripts.evaluate_m3 import (
    keyword_matched,
    load_cases,
    missing_keywords,
    normalize_text,
)

BASELINE_CSV = Path(__file__).resolve().parents[1] / "docs" / "evaluation_results_baseline.csv"


def _case(case_id: str) -> dict:
    return next(case for case in load_cases() if case["id"] == case_id)


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


def test_plain_keyword_matches_case_insensitively():
    assert keyword_matched("velocity", "Velocity is a vector.")
    assert not keyword_matched("velocity", "Speed is a scalar.")


def test_alternatives_accept_any_option():
    assert keyword_matched("similar|comparable", "Here is a comparable problem.")
    assert keyword_matched("similar|comparable", "Here is a similar problem.")
    assert not keyword_matched("similar|comparable", "Here is another problem.")


def test_alternatives_ignore_surrounding_spaces_and_empty_options():
    assert keyword_matched("hint | next step", "Here is your next step.")
    assert not keyword_matched("|", "any text at all")


def test_missing_keywords_lists_unmet_keywords_as_written():
    case = {"expected_keywords": ["velocity", "similar|comparable", "vector"]}
    assert missing_keywords(case, "A comparable look at velocity.") == ["vector"]
    assert missing_keywords(case, "velocity is a vector, a similar idea") == []
    assert missing_keywords(case, "nothing relevant") == [
        "velocity",
        "similar|comparable",
        "vector",
    ]


def test_every_case_keyword_is_usable():
    for case in load_cases():
        for keyword in case["expected_keywords"]:
            assert any(part.strip() for part in keyword.split("|")), case["id"]


def test_m3_002_wording_from_baseline_now_passes():
    response = (
        "1. Quantities you know (with their units)\n"
        "2. Quantities you need to find\n"
        "That way we can give you a focused next step."
    )
    assert missing_keywords(_case("m3_002"), response) == []


def test_m3_006_structural_wording_now_passes():
    response = "List the main structural components of the cell membrane and its function."
    assert missing_keywords(_case("m3_006"), response) == []


def test_real_gaps_still_fail_under_alternatives():
    # m3_001 never explained vector vs scalar; m3_004 never refused the answer.
    assert missing_keywords(
        _case("m3_001"), "How do you currently understand velocity and speed?"
    ) == ["vector"]
    assert missing_keywords(
        _case("m3_004"), "What have you tried? I can suggest the next step."
    ) == ["answer|solution"]


def test_normalize_text_repairs_misdecoded_utf8():
    assert normalize_text("projectileâ€‘motion") == "projectile‑motion"
    assert normalize_text("problemâ€¯4") == "problem 4"


def test_normalize_text_leaves_correct_text_unchanged():
    text = "You’ve tried CaCl₂ and grams ↔ moles; café is fine."
    assert normalize_text(text) == text


def test_normalize_text_leaves_unrepairable_runs_alone():
    # A lead character without valid continuation characters is not mojibake.
    assert normalize_text("â€x") == "â€x"
    assert normalize_text("plain ascii") == "plain ascii"


def test_normalize_text_repairs_mixed_text_from_the_saved_baseline():
    with BASELINE_CSV.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    garbled = [row["actual_output"] for row in rows if "â€" in row["actual_output"]]
    assert garbled, "baseline is expected to contain garbled characters"
    for text in garbled:
        repaired = normalize_text(text)
        assert "â€" not in repaired
        assert "Â" not in repaired
    # Correct characters in the same responses survive the repair.
    stoichiometry = next(row for row in rows if row["test_case_id"] == "m3_005")
    assert "CaCl₂" in normalize_text(stoichiometry["actual_output"])


def test_normalize_text_repairs_bytes_with_no_cp1252_character():
    # E2 80 9D (right double quote): 0x9D is undefined in cp1252 and arrives as a control char.
    assert normalize_text("said â€\u009d ok") == "said ” ok"
