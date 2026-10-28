# CourseGuide AI

CourseGuide AI is a policy-aware tutoring prototype that helps students take
the next reasoning step without doing graded work for them.

## M3 CHANGES

The M2 single agent was extended into a sequential multi-agent system:

1. **CourseGuide Planner** classifies the request, retrieves the course policy,
   optionally recalls prior notes, and produces a bounded handoff.
2. **CourseGuide Tutor** receives that handoff and writes the student-facing
   response while enforcing the policy.
3. **AgentMemoryServer** provides persistent JSON-backed `remember` and
   `recall` MCP tools. This is the knowledge/memory layer for M3.

The handoff is sequential reasoning: the tutor cannot run until the planner
has produced its request type, constraints, context, and next-step plan.

The M3 implementation also includes:

- Ten evaluation cases in `tests/m3_evaluation_cases.yaml`.
- A live evaluation runner in `scripts/evaluate_m3.py` that writes
  `evaluation_results.csv` with each input, expected keywords, actual output,
  pass/fail status, and failure category.
- Offline checks in `tests/test_m3_evaluation.py`.

These changes were made to satisfy the M3 requirements for two agents, an
explicit handoff, sequential reasoning, a memory layer, and a ten-case
evaluation plan.

## Setup and run

Use Python 3.11 or newer, create a virtual environment, and install:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then set the model base URL, API key, and model
name for the provider used by your team. Never commit `.env` or expose its API
key. From the repository root, run:

```powershell
Copy-Item .env.example .env
python -m src.m3_agent --course physics_101 --question "I am stuck setting up Newton's second law."
```

The policy MCP server reads course files from `config/`. Memory is stored in
`data/agent_memory.json` and is limited to the most recent 100 notes.

## Evaluation

Run the offline evaluation checks:

```powershell
python -m pytest tests/test_m3_evaluation.py -q
```

Run all ten live cases against the configured model:

```powershell
python scripts/evaluate_m3.py
```

The live command creates `evaluation_results.csv`. This generated file,
`.env`, and `data/agent_memory.json` should not be committed.

## M3 submission checklist

The repository code covers the multi-agent system, memory layer, and
evaluation runner. The team must also complete and submit:

- An updated architecture diagram showing both agents, the handoff, reasoning,
  MCP tools, memory layer, model backend, and guardrails.
- A two-minute screen recording of a real prompt, including one imperfect
  moment and how the system handles it.
- A 400–500 word evaluation plan describing the ten cases, evaluation method,
  and success threshold.
- A cost model with three usage scenarios, scaling assumptions, and a path to
  sustainability.
- A user-testing plan identifying testers, tasks, session questions, and
  success criteria.
- Commits from all three teammates showing cross-functional contributions.

## Known limitations

- The memory layer uses JSON substring matching rather than embeddings or a
  vector database, so retrieval quality will decline for paraphrased queries.
- The planner-to-tutor handoff is text, so malformed model output is not yet
  rejected by a schema validator.
- Model calls and MCP subprocesses require network access and valid provider
  credentials; offline fallback and retry policy are not implemented yet.
