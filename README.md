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
  `evaluation_results.csv` with each input, expected keywords, expected output,
  human-review and critic-score fields, actual output, pass/fail status, and
  failure category.
- A committed baseline snapshot at
  `docs/evaluation_results_baseline.csv`. The runner's root-level
  `evaluation_results.csv` is a generated working file and should not be
  committed.
- Offline checks in `tests/test_m3_evaluation.py`.

These changes were made to satisfy the M3 requirements for two agents, an
explicit handoff, sequential reasoning, a memory layer, and a ten-case
evaluation plan.

## Setup and run one question in the terminal

Use Python 3.11 or newer. From the repository root, create a virtual
environment and install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then open `.env` and set the model base URL, API
key, and model name for the provider used by your team. Never commit `.env` or
expose its API key. The program needs network access to the configured model.

Run one question with PowerShell:

```powershell
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m src.m3_agent `
  --course physics_101 `
  --question "I am stuck setting up Newton's second law."
```

The tutor's response is printed directly in the terminal. To ask another
question, run the command again with a different `--question` value. For
example:

```powershell
.\scripts\run_m3.ps1 `
  -Course chemistry_201 `
  -Question "Can you help me decide what to check next in my equilibrium expression?"
```

The PowerShell launcher uses the repository's virtual environment and prints
the final CourseGuide Tutor response. Available course policy files are
`physics_101`, `chemistry_201`, and `biology_201`. If PowerShell blocks local
scripts, run the Python command above directly or allow scripts for the current
session with `Set-ExecutionPolicy -Scope Process Bypass`.

On macOS or Linux, the equivalent command is:

```bash
./scripts/run_m3.sh --course physics_101 --question "I am stuck setting up Newton's second law."
```

The policy MCP server reads course files from `config/`. Memory is stored in
`data/agent_memory.json` and is limited to the most recent 100 notes.

### Run with the helper scripts

If you would rather not type the full command, the `scripts/` folder has
shortcuts. Each one switches to the repository root and turns on `.venv` for
you if it exists. You still need to complete the setup above first (virtual
environment, `pip install`, and your `.env` file).

There are two versions of each script, so use the one that matches your
terminal. The `.sh` files only work on macOS, Linux, or Git Bash. They do
nothing useful in Windows PowerShell or Command Prompt, which can look like the
command was skipped. On Windows, use the `.ps1` files.

**Windows (PowerShell):**

```powershell
.\scripts\run_m3.ps1
```

If PowerShell says running scripts is disabled, allow it for this window only
and run the script again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**macOS / Linux:**

```bash
chmod +x scripts/*.sh        # only needed once, if the scripts are not executable
./scripts/run_m3.sh
```

Both versions ask the agent one example question: "I am stuck setting up
Newton's second law." for `physics_101`.

## Evaluation

Run the offline evaluation checks:

```powershell
python -m pytest tests/test_m3_evaluation.py -q
```

Run all ten live cases against the configured model:

```powershell
python scripts/evaluate_m3.py
```

The live command creates `evaluation_results.csv`. The committed baseline
snapshot records one 4/10 automated run; live runs can vary with model output.
The runner labels automated keyword misses as `response_keyword`; human review
should assign the root cause from the evaluation plan's categories. The
`human_review` and `critic_score` columns remain blank until those reviews are
performed. `.env` and `data/agent_memory.json` should not be committed.

### Run the evaluation with the helper script

`scripts/run_tests.ps1` (Windows) and `scripts/run_tests.sh` (macOS / Linux) do
the same thing as the live command above. They run all ten cases against your
configured model, print PASS or FAIL for each one, show the overall pass rate at
the end, and write `evaluation_results.csv`.

```powershell
.\scripts\run_tests.ps1
```

```bash
./scripts/run_tests.sh
```

Anything you add after the script name is passed along to the evaluation, so you
can pick a different model or save the results somewhere else:

```powershell
.\scripts\run_tests.ps1 --model your-model-name --output results\run1.csv
```

```bash
./scripts/run_tests.sh --model your-model-name --output results/run1.csv
```

Because this sends real requests to the model, it needs your `.env` credentials
and may take a few minutes. To run only the quick offline checks instead (no
model calls), use `python -m pytest tests/test_m3_evaluation.py -q` (shown above).

## M3 submission status

The repository contains the M3 implementation, evaluation plan, baseline
results, and supporting tests. The architecture diagram, screen recording,
cost and sustainability analysis, user-testing plan, and teammate contribution
evidence are maintained as separate submission materials.

The baseline had substantive quality gaps in cases `m3_001` and `m3_006`:
their outputs asked follow-up questions without explaining the requested
concepts. Other automated failures may be keyword misses rather than incorrect
guidance, so the baseline should not be treated as a final human-reviewed
score.

## Known limitations

- The memory layer uses JSON substring matching rather than embeddings or a
  vector database, so retrieval quality will decline for paraphrased queries.
- The planner-to-tutor handoff is text, so malformed model output is not yet
  rejected by a schema validator.
- Model calls and MCP subprocesses require network access and valid provider
  credentials; offline fallback and retry policy are not implemented yet.
