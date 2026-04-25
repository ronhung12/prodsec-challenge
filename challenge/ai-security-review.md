# AI-Assisted PR Security Reviewer

Use this template for the `ai-security-review.md` deliverable described in the candidate brief. Keep it short. The goal is to describe how you would safely add an AI-assisted PR security reviewer to this repo, not to build a full LLM agent.

## Inputs

Describe what context the reviewer should receive.

- Diff.
- Route map.
- Auth model notes.
- Scanner findings.
- Any other context you think is necessary.

## Outputs

Describe the reviewer's output format.

- Risk label.
- Finding summary.
- Confidence.
- Suggested owner.
- Block/comment/escalate decision.

## Guardrails

Describe how the system avoids unsafe or noisy behavior.

- No blocking on low-confidence AI-only findings.
- Require deterministic evidence for PR failure.
- Detect likely false positives.
- Avoid sending secrets to third-party models.
- Add any other trust, privacy, or workflow guardrails you believe matter.

## Evaluation

Describe how you would measure whether the reviewer is working.

- Seeded test cases.
- False positive rate.
- Missed broken access control variants.
- Engineering feedback.
- Any other effectiveness or safety metrics you would track.
