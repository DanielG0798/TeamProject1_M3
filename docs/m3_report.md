# InstructAI: CourseGuide AI
## M3 Multi-Agent System, Cost Analysis, and Evaluation Plan

## Executive Summary

CourseGuide AI is an instructor-configurable learning agent designed to help
college students in reasoning-intensive courses without replacing the
reasoning those courses are intended to develop. M1 interviews identified a
gap between unrestricted general-purpose AI and instructor expectations. M2
implemented a single agent with course-policy MCP tools. M3 extends that
prototype into a sequential multi-agent system with a Planner, Tutor, explicit
handoff, and memory MCP service.

The Planner classifies the request, retrieves course policy, checks relevant
memory, and selects one bounded next step. The Tutor receives that handoff and
produces the student-facing response while following policy. The evaluation
plan defines ten cases and combines automated keyword checking with human
review. The cost analysis identifies the two-model-call design as the main
technical cost risk. The user-testing plan will assess whether students
understand and value controlled guidance.

## 1. Problem and Target Users

College students in reasoning-intensive courses increasingly have access to
immediate general-purpose AI assistance, but that assistance is not
automatically aligned with an instructor's course context, permitted help
level, or expected reasoning process. Faculty discovery evidence shows concern
about preserving important student skills and preventing AI from replacing
student thinking.

CourseGuide AI focuses first on students in quantitative STEM coursework,
beginning with Physics. These students may need help with diagrams, setup,
notation, units, concepts, and reasoning rather than a complete numerical
answer. Instructors are important adopters because they configure allowed help
levels, approved sources, tone, and problem-solving rules. Institutions and
departments are potential buyers because they need governed, auditable, and
privacy-conscious AI use.

The M1 interviews support this problem. Paul, a mathematics faculty member,
questioned what it means to be a mathematician and expressed concern that
students may outsource reasoning to AI. He favored strict guardrails that
prevent complete ready-made answers. Lindsay described frustration when an AI
changed unrelated work instead of following a narrow request. Salle's use of
AI for precise editing showed the value of preserving the user's ownership and
voice. Jennifer and Joslyn connected trust to institutional acceptance,
responsible data handling, privacy, and vetted tools.

An agent is appropriate because the workflow requires context-dependent
decisions: identify the course, classify the request, retrieve instructor
rules, inspect student context, select an appropriate action, and reassess
after the student responds. A static FAQ cannot make these decisions.

The main open questions are whether students will choose controlled guidance
when unrestricted AI is faster, and how much control, transparency, privacy
protection, and institutional vetting instructors will require.

## 2. M3 System Architecture

The user submits a course ID and question to `src/m3_agent.py`. The program
starts the CoursePolicyServer and AgentMemoryServer MCP services. The Planner
calls `classify_help_request` and `lookup_course_policy`, and may call
`recall`. It returns a handoff containing `REQUEST_TYPE`,
`POLICY_CONSTRAINTS`, `STUDENT_CONTEXT`, `NEXT_STEP`, and
`MEMORY_TO_SAVE`.

The Tutor receives the original input and complete handoff. It follows the
course policy and produces the final response. It may call `remember` for a
useful durable note. The handoff occurs only after the Planner completes,
making sequential reasoning explicit. The architecture diagram and screen
recording are separate M3 deliverables.

## 3. Reasoning and Memory

M3 uses sequential reasoning: classify the request, retrieve policy, recall
relevant memory, identify known and unknown information, select one next step,
handoff to the Tutor, and generate the policy-constrained response.

The memory MCP service provides `remember` and `recall`. It stores the latest
100 course-specific notes in JSON. This is transparent and suitable for the
prototype, but substring matching may miss paraphrases. A future version
could use privacy-approved embeddings or a vector database.

## 4. Evaluation Plan

CourseGuide AI will be evaluated with ten cases across Physics 101, Chemistry
201, and Biology 201. The cases cover concept explanations, hints, setup
checks, analogies, direct-answer pressure, unit reminders, and
course-specific reasoning. Each case includes a course, student question,
expected keywords, and intended help type.

Automated checking records the input, expected keywords, actual output,
pass/fail status, and failure category. Human review checks correct course
context, appropriate help level, a useful next step, and policy compliance.
A response containing expected words still fails if it gives a prohibited
full solution or final numerical answer.

The proposed threshold is at least eight of ten cases passing both automated
and human review, with zero critical policy violations. Failures will be
classified as classification, policy retrieval, memory retrieval,
Planner-to-Tutor handoff, response generation, or execution/configuration
failures. The final pass rate and failure analysis must be added after the
ten live cases are actually run.

### Initial automated baseline

The first live run completed all ten cases and passed 4/10 cases (40%) under
the automated keyword check. Cases M3-007 through M3-010 passed. Cases
M3-001 through M3-006 failed because the responses requested more student
context or used a paraphrase rather than the exact expected keyword. This is
an automated baseline, not a final human-reviewed score.

The failures show that exact keyword matching is brittle. For example, the
velocity/speed response asked the student to compare the terms but did not
include `vector`, while the stoichiometry response supplied a comparable
problem without using the exact word `similar`. The team should retain
keyword checks for regression testing and add rubric-based human review for
paraphrases, usefulness, and policy compliance.

## 5. Evaluation Cases

| ID | Course | Scenario | Expected evidence |
|---|---|---|---|
| M3-001 | Physics 101 | Velocity versus speed | velocity, speed, vector |
| M3-002 | Physics 101 | Projectile-motion next step | known, unknown, hint |
| M3-003 | Chemistry 201 | Equilibrium setup check | expression, products, reactants |
| M3-004 | Physics 101 | Direct-answer request | hint, answer |
| M3-005 | Chemistry 201 | Stoichiometry analogy | example, similar |
| M3-006 | Biology 201 | Cell membrane explanation | membrane, structure, function |
| M3-007 | Biology 201 | Genetics next step | inheritance, pattern, information |
| M3-008 | Biology 201 | Experimental evidence analogy | example, evidence, observation |
| M3-009 | Physics 101 | Units in force problems | units, force |
| M3-010 | Chemistry 201 | Reaction-balancing next step | balance, check |

## 6. Cost and Sustainability

Each request uses two model calls, one Planner and one Tutor. The estimated
model cost is:

```text
2 × [(input tokens × input price per token)
+ (output tokens × output price per token)]
```

Usage costs include model calls, retrieval storage, session logging,
misconception analytics, and optional image analysis. Fixed costs include
development, hosting, monitoring, course setup, instructor configuration,
safety testing, prompt-injection testing, privacy review, and maintenance.

The following planning scenarios use an illustrative average cost of $0.01
per request and must be replaced with current provider pricing and measured
token counts:

| Scenario | Requests/month | Model cost | Storage/logging | Fixed costs | Total |
|---|---:|---:|---:|---:|---:|
| Pilot course | 1,000 | $10 | $5 | $100 | $115 |
| Expected adoption | 10,000 | $100 | $20 | $150 | $270 |
| High usage | 50,000 | $500 | $75 | $300 | $875 |

Customers include students, instructors, and institutions. The preferred
initial revenue model is department or institutional licensing based on
students or courses. Other options include per-course pricing, usage tiers,
analytics, multimodal add-ons, additional subjects, and grants.

M2 research estimated the global AI-in-education market at $8.3 billion in
2025, growing toward $57.2 billion by 2033. The narrower estimated market was
approximately 3.1 million U.S. students in suitable quantitative STEM
courses, representing a planning opportunity of $62–$124 million annually at
$20–$40 per student per year.

If monthly cost is `C` and revenue per customer is `R`, break-even customers
equal `ceil(C / R)`. At $270 monthly cost and $150 monthly revenue per
department, the illustrative break-even point is two departments. This
excludes sales, support, legal, and compliance costs.

The largest technical cost risk is the two-call design. The largest market
risk is adoption because students may prefer unrestricted AI and institutions
may hesitate over configuration, privacy, procurement, and maintenance.
M3 demonstrates feasibility but does not yet prove willingness to pay.

## 7. User-Testing Plan

The team will recruit five external testers who fit the target profile:
undergraduate students in reasoning-intensive or quantitative STEM courses
who have used tutoring tools or general-purpose AI. Team members and the
instructor will not be testers. Sessions will last approximately 20 minutes
in person or by video call, using anonymous labels.

The task is to submit a course-related question normally given to a tutor or
chatbot, review the response, and explain whether the next step is useful.
The facilitator will observe actions, hesitation, confusion, understanding of
the next step, opinion of the help level, and willingness to use the system
again.

The facilitator will ask what the tester expected, whether the response was
clear, what the agent wanted them to do next, where they hesitated, whether
the help level was appropriate, what would build trust, and whether they would
use the agent again.

Success criteria are that four of five testers complete the task without help,
four can explain the next step, three would use the agent again, no critical
policy violations occur, and four understand that the system guides reasoning
rather than completing assignments. The team will record repeated confusion,
requests for complete answers, privacy concerns, and understanding of the
Planner/Tutor roles. Findings will support the M4 proceed, pivot, or scope
down decision.

## 8. Limitations and Risks

Memory uses JSON substring matching, the handoff is not schema validated, and
model/MCP calls require network access and valid credentials. Keyword
evaluation can overstate quality, so human review is required. Production
deployment would also require data-retention controls, consent, deletion
procedures, access controls, privacy review, and institutional approval.

## 9. M3 Completion Checklist

- [ ] Architecture diagram added.
- [ ] Two-minute narrated recording completed.
- [ ] Ten live cases run and CSV attached.
- [ ] Actual pass rate and failed-case analysis added.
- [ ] Current provider pricing verified.
- [ ] User-testing sessions completed and summarized.
- [ ] Cross-functional commits from all three teammates.
- [ ] `.env` and generated memory files excluded from Git.
