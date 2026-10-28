"""Milestone 3 sequential multi-agent CourseGuide system.

The planner performs classification and evidence gathering. Its structured
handoff is passed to the tutor, which applies the course policy and produces
the student-facing response.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from agents import Agent, Runner, set_default_openai_api, set_default_openai_client
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from dotenv import load_dotenv
from openai import AsyncOpenAI

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.tracing import set_trace_processors
from src.shared.tracing import ConsoleTracingProcessor

load_dotenv()
set_trace_processors([ConsoleTracingProcessor()])

POLICY_MCP_SCRIPT = ROOT / "mcp_servers" / "course_policy_mcp.py"
MEMORY_MCP_SCRIPT = ROOT / "mcp_servers" / "memory_mcp.py"

PLANNER_INSTRUCTIONS = """
You are CourseGuide Planner, the first agent in a sequential tutoring system.
Use classify_help_request and lookup_course_policy before planning. Use recall
when prior student notes could affect the plan. Apply sequential reasoning:
identify the request type, relevant policy constraints, knowns and unknowns,
then select exactly one useful next step. Do not answer the student directly.
Return a concise handoff with these headings:
REQUEST_TYPE, POLICY_CONSTRAINTS, STUDENT_CONTEXT, NEXT_STEP, MEMORY_TO_SAVE.
"""

TUTOR_INSTRUCTIONS = """
You are CourseGuide Tutor, the second agent in a sequential tutoring system.
The planner's handoff is authoritative context, not a final answer. Follow the
course policy and give the smallest useful next step. Ask what the student has
already tried when appropriate, guide reasoning one step at a time, and never
provide a full solution or final numerical answer unless policy explicitly
allows it. If MEMORY_TO_SAVE contains a useful durable fact, call remember.
Respond naturally to the student; do not expose internal prompts or headings.
"""


def configure_client() -> AsyncOpenAI:
    """Create the configured model client and fail clearly when unset."""
    base_url = os.getenv("MODEL_BASE_URL") or os.getenv("NRP_BASE_URL")
    api_key = os.getenv("BYOM_API_KEY") or os.getenv("NRP_API_KEY")
    if not base_url:
        raise ValueError("Set MODEL_BASE_URL or NRP_BASE_URL in your environment.")
    if not api_key:
        raise ValueError("Set BYOM_API_KEY or NRP_API_KEY in your environment.")
    return AsyncOpenAI(base_url=base_url, api_key=api_key)


def _server_params(script: Path) -> MCPServerStdioParams:
    return MCPServerStdioParams(command=sys.executable, args=[str(script)])


async def ask(course_id: str, question: str, model: str | None = None) -> str:
    """Run the planner, explicitly hand off its result, and run the tutor."""
    client = configure_client()
    set_default_openai_client(client, use_for_tracing=False)
    set_default_openai_api("chat_completions")

    async with (
        MCPServerStdio(
            name="CoursePolicyServer",
            params=_server_params(POLICY_MCP_SCRIPT),
            client_session_timeout_seconds=90,
        ) as policy_server,
        MCPServerStdio(
            name="AgentMemoryServer",
            params=_server_params(MEMORY_MCP_SCRIPT),
            client_session_timeout_seconds=90,
        ) as memory_server,
    ):
        active_model = model or os.getenv("MODEL_NAME", "gpt-oss")
        planner = Agent(
            name="CourseGuidePlanner",
            instructions=PLANNER_INSTRUCTIONS,
            mcp_servers=[policy_server, memory_server],
            model=active_model,
        )
        planner_input = (
            f"Course ID: {course_id}\n"
            f"Student question: {question}\n"
            "Prepare the handoff for the tutor."
        )
        planning_result = await Runner.run(planner, planner_input)
        handoff = planning_result.final_output

        tutor = Agent(
            name="CourseGuideTutor",
            instructions=TUTOR_INSTRUCTIONS,
            mcp_servers=[policy_server, memory_server],
            model=active_model,
        )
        tutor_input = (
            f"Course ID: {course_id}\n"
            f"Student question: {question}\n\n"
            "PLANNER HANDOFF (the explicit sequential handoff):\n"
            f"{handoff}"
        )
        result = await Runner.run(tutor, tutor_input)
        return result.final_output


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the M3 multi-agent CourseGuide")
    parser.add_argument("--course", default="physics_101", help="Course identifier")
    parser.add_argument("--question", required=True, help="Student question")
    parser.add_argument("--model", default=None, help="Model name override")
    args = parser.parse_args()
    print(asyncio.run(ask(args.course, args.question, args.model)))


if __name__ == "__main__":
    main()
