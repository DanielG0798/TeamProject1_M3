# M3 Cost and Sustainability Analysis

## Cost structure

Each student request uses two model calls: one Planner call and one Tutor
call. The estimated cost is:

```text
2 × [(input tokens × input price per token)
+ (output tokens × output price per token)]
```

Usage-based costs include model calls, memory or retrieval storage, session
logging, misconception analytics, and optional image or diagram analysis.
Fixed costs include development, hosting, monitoring, course-material setup,
instructor configuration, safety testing, prompt-injection testing, privacy
review, and course-policy maintenance.

The following are planning estimates using an illustrative average model cost
of approximately $0.01 per completed request. They must be replaced with
current provider pricing and measured token counts before submission.

| Scenario | Requests/month | Model cost | Storage/logging | Fixed costs | Total |
|---|---:|---:|---:|---:|---:|
| Pilot course | 1,000 | $10 | $5 | $100 | $115 |
| Expected adoption | 10,000 | $100 | $20 | $150 | $270 |
| High usage | 50,000 | $500 | $75 | $300 | $875 |

The main scaling risk is that every request requires two model calls. Longer
prompts, course documents, memory retrieval, image analysis, and analytics can
increase the cost per request.

## Customers and revenue

The customer groups are students in quantitative STEM courses, instructors
who configure and approve the agent, and institutions or departments that
require governed AI use. Students are direct users; instructors are likely
the primary adopters; institutions may become paying customers.

The preferred initial revenue model is institutional or department licensing
based on the number of students or courses. Possible revenue streams include
per-student pricing, per-course pricing, token-usage tiers, department
licensing, institution-wide licensing, multimodal diagram analysis, analytics
exports, additional subjects, and education grants.

The M2 report identified a planning range of $20–$40 per student per year for
an institutional license. This amount must be validated through future
customer interviews and user testing.

## Market and break-even

The M2 research estimated the global AI-in-education market at approximately
$8.3 billion in 2025, growing toward approximately $57.2 billion by 2033.
The narrower serviceable market is U.S. colleges and universities offering
quantitative or diagram-heavy STEM courses. The M2 estimate was approximately
3.1 million potential students and $62–$124 million annually at $20–$40 per
student per year.

If monthly operating cost is `C` and monthly revenue per customer is `R`:

```text
Break-even customers = ceil(C / R)
```

Using the expected cost of $270 and a planning license of $150 per month:

```text
ceil($270 / $150) = 2 customers
```

This excludes sales, support, legal, compliance, and administrative costs.

The largest technical cost risk is the two-model-call architecture. The
largest market risk is adoption: students may prefer unrestricted AI, while
institutions may hesitate because of configuration, privacy, procurement, and
maintenance requirements. M3 demonstrates feasibility but does not yet prove
willingness to pay.
