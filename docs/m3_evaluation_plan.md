# M3 Evaluation Plan

CourseGuide AI will be evaluated using ten test cases representing concept
explanations, hints, setup checks, analogies, direct-answer pressure, unit
reminders, and course-specific reasoning across Physics 101, Chemistry 201,
and Biology 201. The cases are in `tests/m3_evaluation_cases.yaml`, and the
runner is `scripts/evaluate_m3.py`.

The evaluation uses automated keyword checking and human review. The runner
records the test ID, course, input, expected keywords, actual response,
pass/fail status, and failure category in `evaluation_results.csv`. This
creates a reproducible baseline for future M4 improvements.

Keyword matching alone cannot determine whether a response is safe, relevant,
or instructionally useful. A reviewer must assess correct course context,
appropriate help level, a useful next step, and compliance with the course
policy. A response containing the expected words still fails if it gives a
prohibited full solution or final numerical answer.

The ten cases cover multiple help types. Concept cases address velocity and
speed, cell membrane structure and function, and genetics. Next-step cases
address projectile motion, direct-answer requests, units in force problems,
and reaction balancing. Other cases test equilibrium setup, stoichiometry
examples, and interpretation of experimental evidence.

The proposed threshold is at least eight of ten cases passing both automated
and human review, with zero critical policy violations. Failures are
categorized as classification, course-policy retrieval, memory retrieval,
Planner-to-Tutor handoff, response generation, or execution/configuration
failures.

For each failed case, the team will document the output, likely root cause,
and whether the fix belongs in the prompt, MCP tool, memory layer, handoff
format, or model configuration. The team must not report a final pass rate
until all ten live cases have actually been run.

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
