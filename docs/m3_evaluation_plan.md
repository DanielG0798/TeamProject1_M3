# M3 Evaluation Plan

CourseGuide AI will be evaluated with ten test cases covering concept
explanations, hints, setup checks, analogies, direct-answer pressure, unit
reminders, and course-specific reasoning across Physics 101, Chemistry 201,
and Biology 201. The cases are stored in `tests/m3_evaluation_cases.yaml`;
`scripts/evaluate_m3.py` records the results in `evaluation_results.csv`.

The evaluation combines automated keyword checking with human review.
Automated checking provides a reproducible baseline, but keywords alone
cannot determine whether a response is safe, relevant, or instructionally
useful. A reviewer will assess every response for correct course context,
appropriate help level, a useful next step, and compliance with the course
policy. A response containing expected words still fails if it gives a
prohibited full solution or final numerical answer.

The ten cases cover three concept/explanation scenarios, four bounded
next-step scenarios, one setup check, and two analogy/example scenarios. The
direct-answer case is especially important because policy compliance is a
safety requirement rather than only a quality preference.

The proposed threshold is at least eight of ten cases passing both automated
and human review, with zero critical policy violations. Failures will be
categorized as classification, course-policy retrieval, memory retrieval,
Planner-to-Tutor handoff, response generation, or execution/configuration
failures. For each failure, the team will document the output, likely root
cause, and whether the fix belongs in the prompt, MCP layer, memory layer,
handoff format, or model configuration. This baseline will be used to measure
M4 improvements.

## Initial automated baseline

The first live run completed all ten cases and passed 4/10 cases (40%) under
the keyword check. Cases M3-007 through M3-010 passed. Cases M3-001 through
M3-006 failed because the responses requested more student context or used a
paraphrase rather than the exact expected keyword. This is an automated
baseline, not a final human-reviewed score.

The failures show that exact keyword matching is brittle. For example, the
velocity/speed response asked the student to compare the terms but did not
include `vector`, while the stoichiometry response supplied a comparable
problem without using the exact word `similar`. The team should retain
keyword checks for regression testing and add rubric-based human review for
paraphrases, usefulness, and policy compliance.

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
