"""Persistent MCP memory tools used by the M3 multi-agent pipeline."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parents[1]
MEMORY_PATH = ROOT / "data" / "agent_memory.json"
mcp = FastMCP("AgentMemoryServer")


def _read_memory() -> list[dict[str, str]]:
    if not MEMORY_PATH.exists():
        return []
    with MEMORY_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"Memory file must contain a JSON list: {MEMORY_PATH}")
    return [item for item in data if isinstance(item, dict)]


def _write_memory(entries: list[dict[str, str]]) -> None:
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = MEMORY_PATH.with_suffix(".tmp")
    with temporary_path.open("w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)
    temporary_path.replace(MEMORY_PATH)


@mcp.tool()
def remember(course_id: str, student_note: str) -> str:
    """Store a short student note that can help with a later question."""
    note = student_note.strip()
    if not note:
        raise ValueError("student_note must not be empty")
    entries = _read_memory()
    entries.append({"course_id": course_id.strip(), "note": note})
    _write_memory(entries[-100:])
    return "Note saved."


@mcp.tool()
def recall(course_id: str, query: str = "") -> str:
    """Return saved notes for a course, optionally filtered by words in query."""
    terms = [term for term in query.lower().split() if term]
    matches = []
    for entry in _read_memory():
        if entry.get("course_id") != course_id:
            continue
        note = entry.get("note", "")
        if not terms or all(term in note.lower() for term in terms):
            matches.append(f"- {note}")
    return "\n".join(matches[-5:]) if matches else "No relevant memory found."


if __name__ == "__main__":
    mcp.run()
