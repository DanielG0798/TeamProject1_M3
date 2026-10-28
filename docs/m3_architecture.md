# CourseGuide AI M3 Architecture

## System overview

CourseGuide AI is a policy-aware tutoring system that uses two agents in a
sequential workflow. It provides useful guidance while preserving student
reasoning and following instructor-defined help boundaries.

## Request flow

1. The student submits a course ID and question.
2. CourseGuide Planner receives the request.
3. Planner calls `classify_help_request` and `lookup_course_policy`.
4. Planner calls `recall` when prior context may be useful.
5. Planner identifies the request type, policy restrictions, student context,
   and one useful next step.
6. Planner creates an explicit handoff.
7. CourseGuide Tutor receives the question and Planner handoff.
8. Tutor follows the course policy and generates the student-facing response.
9. Tutor may call `remember` for a useful durable note.

## Agent roles

### CourseGuide Planner

The Planner classifies the request, retrieves the course policy, checks
relevant memory, identifies known and unknown information, selects one bounded
next step, and creates the Tutor handoff. It does not write the final
student-facing response.

### CourseGuide Tutor

The Tutor reads the Planner handoff, follows the instructor policy, provides
the smallest useful next step, avoids prohibited full solutions, and saves
useful durable information when appropriate.

## Explicit handoff

The Tutor does not run until the Planner has completed its planning step. The
handoff contains:

- `REQUEST_TYPE`
- `POLICY_CONSTRAINTS`
- `STUDENT_CONTEXT`
- `NEXT_STEP`
- `MEMORY_TO_SAVE`

## MCP services

`CoursePolicyServer` provides `lookup_course_policy`,
`classify_help_request`, and `list_available_courses`. It reads course
policies from `config/`.

`AgentMemoryServer` provides `remember` and `recall`. Memory is stored in
`data/agent_memory.json`; the prototype keeps the latest 100 notes and uses
substring matching.

## Guardrails and limitations

- Course policy is retrieved before the final answer.
- The Tutor should not provide a full solution unless policy allows it.
- Memory is limited to short course-specific notes.
- `.env` and generated memory files must remain excluded from Git.
- Human review is required because keyword matching alone cannot guarantee
  safe or useful responses.
- Memory is not semantic, and the text handoff is not schema validated.

## Diagram content

The final diagram should show:

```text
Student
  |
  v
CourseGuide Planner
  |-- CoursePolicyServer:
  |     classify_help_request
  |     lookup_course_policy
  |-- AgentMemoryServer: recall
  |
  v
Explicit Planner Handoff
  |
  v
CourseGuide Tutor
  |-- AgentMemoryServer: remember
  |
  v
Policy-constrained student response
```
