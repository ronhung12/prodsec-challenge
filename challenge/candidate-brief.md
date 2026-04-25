# Senior Product Security Engineer Take-Home

You will receive a small FastAPI service modeling a simplified records API. Your job is to design CI that protects it, write one piece of custom detection logic, and communicate findings to the engineering team that owns it.

Time: ~ 3 hours

We are not looking for maximum tool count, exhaustive OWASP coverage, or scanner output pasted into a report. We are looking for senior product security judgment: useful automation, low-noise triage, honest coverage limits, and communication an engineering team would act on.

## Scenario

You are the Product Security Engineer supporting this service. Engineering wants lightweight CI coverage for security issues, but recurring product risk is not limited to generic injection. A common failure mode is broken access control: services trusting client-supplied resource identifiers instead of verifying access using authenticated identity and server-side authorization logic.

Assume this is a real service owned by a busy engineering team. Your goal is to raise the security bar without turning CI into a source of noisy, unactionable blocking failures.

## Deliverables

Submit a public GitHub repository containing:

1. A working GitHub Actions CI pipeline.
2. One custom detection rule or targeted check for a vulnerability class that off-the-shelf scanners miss.
3. A one-page triage writeup.
4. A remediation message you would actually send to the engineering lead.
5. A short `ai-security-review.md` describing an AI-assisted PR security reviewer for this repo.
6. A short AI tools usage note.

## What To Build

Set up CI that catches what standard tooling can catch. Include practical severity gating that would be reasonable for a product engineering team.

Read the code and identify at least one important issue your CI does not catch. Write one custom detection rule or targeted check for that class. Semgrep, CodeQL, tests, or an equivalent approach are all acceptable. We care more about whether the check generalizes than whether it matches the exact seeded code.

Your one-page writeup should cover:

- Real findings you would prioritize, with severity and rationale.
- Findings you believe are false positives or acceptable in context, with rationale.
- What your pipeline catches.
- What your pipeline does not catch.
- Where you would invest next if this was a production service.

Your remediation message should be the message you would send day-to-day to an engineering lead. Keep it specific, risk-based, and actionable.

## AI-Assisted PR Security Reviewer

Add a short `ai-security-review.md` describing how you would design an AI-assisted PR security reviewer for this repo. Do not build a full LLM agent unless you want to. We care more about operational judgment than framework familiarity.

Your `ai-security-review.md` should define:

- Inputs: diff, route map, auth model notes, and scanner findings.
- Outputs: risk label, finding summary, confidence, suggested owner, and block/comment/escalate decision.
- Guardrails: no blocking on low-confidence AI-only findings, deterministic evidence required for PR failure, likely false-positive detection, and avoiding sending secrets to third-party models.
- Evaluation: seeded test cases, false positive rate, missed BAC variants, and engineering feedback.

## AI Tools Usage

Designing the AI-assisted reviewer above is required. Using AI tools while completing this take-home is optional.

Include a short AI note, max 300-500 words:

- If you used AI, where did you use it and why?
- What did it get right?
- What did it get wrong or miss?
- How did you verify or challenge the output?
- Did it change your CI design, custom rule, or triage decision?
- If you did not use AI, where do you think AI would and would not be useful in this workflow?

## Presentation

After submission, you will present for 30 minutes:

- 10 minutes walking through your pipeline, custom rule, and top findings.
- 20 minutes of panel Q&A.

Be ready to discuss:

- Why you prioritized the issues you did.
- Which findings should block PRs and which should only comment or alert.
- What your custom rule would catch in a variant we did not seed.
- What your pipeline would miss.
- Where AI helped, where you did not trust it, and how you would use AI safely in product security CI.
