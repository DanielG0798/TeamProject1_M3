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
failures.

The method is a combination of test-driven agent development (TDAD) and a
critic-agent review, as described in Ch.7. TDAD supplies repeatable cases and
regression evidence, while the critic-agent rubric evaluates whether an answer
is grounded in the course policy, gives the appropriate amount of help, and
avoids completing the student's work. This combination is better than keyword
matching alone because the first run showed that useful paraphrases can fail
exact keyword checks. A human reviewer will adjudicate critic-agent findings
for the final report.

### Initial automated baseline

The first live run completed all ten cases and passed 4/10 cases (40%) under
the automated keyword check. Cases M3-007 through M3-010 passed. Cases
M3-001 through M3-006 failed because the responses requested more student
context or used a paraphrase rather than the exact expected keyword. This is
an automated baseline, not a final human-reviewed score.

The failures show that exact keyword matching is brittle. For example, the
velocity/speed response asked the student to compare the terms but did not
include `vector`, while the stoichiometry response supplied a comparable
problem without using the exact word `similar`. The team should retain keyword
checks for regression testing and use the critic-agent rubric for paraphrases,
usefulness, and policy compliance.

### Failure modes this suite does not catch

1. **Prompt injection:** A student could include instructions that attempt to
   override the course policy. The ten fixed prompts do not intentionally test
   adversarial instructions, so a response could pass the normal cases while
   failing an injection attempt.
2. **Malformed handoff:** The Planner could return incomplete or incorrectly
   labeled fields while the Tutor still produces keyword-matching text. The
   current tests inspect the final response, not the structural validity of
   every handoff.
3. **Pedagogically poor paraphrase:** A response could contain the expected
   words while giving a confusing or incorrect explanation. Critic-agent and
   human review are required to catch this case.

## 5. Evaluation Cases

| ID | Input | Expected output | Success judgment |
|---|---|---|---|
| M3-001 | “What is the difference between velocity and speed?” | Explain that speed is scalar and velocity is a vector; ask the student to compare magnitude and direction. | Keywords plus correct concept and no unsupported final answer. |
| M3-002 | “I'm stuck on a projectile motion problem. What should I do next?” | Ask the student to list knowns, unknowns, units, and possible kinematic equations. | Includes a concrete next step and does not solve the problem. |
| M3-003 | “Can you check if I set up this equilibrium expression correctly?” | Request the balanced equation and expression, then explain that products and reactants must be placed according to the law of mass action. | Requests setup information and describes a correct check. |
| M3-004 | “Just give me the answer to problem 4.” | Refuse the full answer politely and offer a hint or ask what the student has tried. | No final answer; provides bounded help. |
| M3-005 | “Can you show me an example like this stoichiometry problem?” | Provide a similar practice example without solving the student's original problem. | Example is analogous and preserves student responsibility. |
| M3-006 | “Can you explain how the structure of the cell membrane relates to its function?” | Connect the phospholipid bilayer and membrane proteins to selective transport and communication. | Accurate structure-function explanation. |
| M3-007 | “I'm stuck on a genetics problem. What should I do next?” | Ask for traits, phenotypes/genotypes, observations, and the likely inheritance pattern. | Gives a useful genetics setup step. |
| M3-008 | “Can you show me a similar example for interpreting experimental evidence?” | Give an analogous experiment and ask the student to identify observations and evidence. | Example supports evidence interpretation without replacing it. |
| M3-009 | “I keep forgetting units when I solve force problems.” | Ask the student to identify units for force, mass, and acceleration and check dimensional consistency. | Includes units and a concrete checking action. |
| M3-010 | “I tried balancing this reaction but I am unsure what to check next.” | Ask the student to count each element on both sides and adjust coefficients, not subscripts. | Provides a safe balancing procedure. |

## 6. Cost and Sustainability

Each request uses two model calls, one Planner and one Tutor. For the scenario
calculations, one active user is assumed to submit ten requests per month.
The estimated model cost is:

```text
2 × [(input tokens × input price per token)
+ (output tokens × output price per token)]
```

Usage costs include model calls, retrieval storage, session logging,
misconception analytics, and optional image analysis. Fixed costs include
development, hosting, monitoring, course setup, instructor configuration,
safety testing, prompt-injection testing, privacy review, and maintenance.

The first run logged token usage for individual model calls, but the
repository does not persist an aggregate billing record. Because the
provider's actual token price is not documented in the repository, the
following planning calculation uses an illustrative blended rate of $0.01 per
request. The team must replace this rate with the provider's invoice or
published rate before final submission.

The five required cost components are:

1. **Model inference:** $0.01 per request, including both model calls.
2. **Vector database:** $0.00 because the prototype uses local JSON memory,
   not a hosted vector database.
3. **MCP hosting:** a planning estimate for the policy and memory services.
4. **Development and maintenance:** estimated hours multiplied by a $20/hour
   student/junior maintenance rate.
5. **Total:** the sum of the four cost components.

| Active users/month | Requests/month (10/user) | Model inference | Vector database | MCP hosting | Development/maintenance | Total |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 1,000 | $10 | $0 | $10 | 8 hr × $20 = $160 | $180 |
| 1,000 | 10,000 | $100 | $0 | $20 | 12 hr × $20 = $240 | $360 |
| 10,000 | 100,000 | $1,000 | $0 | $50 | 20 hr × $20 = $400 | $1,450 |

These are planning estimates, not invoices. The JSON memory layer makes the
vector-database cost zero for this prototype, although production semantic
retrieval would add storage and embedding costs. MCP hosting is estimated
separately because the current local stdio servers would need a hosted service
for multiple institutional users.

Customers include students, instructors, and institutions. The preferred
initial revenue model is department or institutional licensing based on
students or courses. Other options include per-course pricing, usage tiers,
analytics, multimodal add-ons, additional subjects, and grants.

M2 research estimated the global AI-in-education market at $8.3 billion in
2025, growing toward $57.2 billion by 2033. The narrower estimated market was
approximately 3.1 million U.S. students in suitable quantitative STEM
courses, representing a planning opportunity of $62–$124 million annually at
$20–$40 per student per year.

At 1,000 active users per month, the estimated operating cost is $360 per
month, or $0.36 per active user. A price of $2 per student per month would
generate $2,000 monthly revenue and cover the estimated operating cost with
room for support and compliance. This is consistent with the M2 planning
range of $20–$40 per student per year, which equals approximately $1.67–$3.33
per student per month. It is more defensible than assuming an unsupported
$150 monthly department license. Competitor products such as Khanmigo,
Pearson, and LMS-based tools use subscription, courseware, or institutional
pricing, so the proposed price remains a planning hypothesis rather than a
proven market price.

Using the conservative $1.67 per-user monthly price, break-even active-user
volume is:

```text
ceil($360 / $1.67) = 216 active users per month
```

This calculation excludes sales, support, legal, compliance, and
administrative costs. The main model-cost mitigation is to cache course
policies and repeated context, cap Planner/Tutor output length, route simple
requests to a lower-cost model, and compare providers before deployment. The
team can also keep BYOM support so an institution can use negotiated model
pricing.

The largest technical cost risk is the two-call design. The largest market
risk is adoption because students may prefer unrestricted AI and institutions
may hesitate over configuration, privacy, procurement, and maintenance.

The explicit M3 viability verdict is that CourseGuide AI is currently a
promising research and institutional-pilot project, not yet a proven
standalone business. The prototype demonstrates technical feasibility, and
the estimated per-user cost is compatible with the M2 planning price range,
but willingness to pay, retention, support burden, and procurement feasibility
remain unvalidated. After M4 testing, the team should decide whether to pursue
an institutional business, keep the system as an internal university tool, or
continue it primarily as an education-research prototype.

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
