# AI-Assisted PR Security Reviewer

I would add the reviewer as a lightweight GitHub PR check that reads the pull request diff, SAST scan results, is given repo-specific security context and post review comments on lines of code flagged by our scan results.

## Inputs

The reviewer should receive scoped, redacted context:

- PR diff with changed files, changed functions, and relevant application context.
- Semgrep JSON/SARIF findings with rule id, severity, confidence, file, line, and message.
- Test and CI status, especially authorization, token validation, and cross-user access tests.
- Redacted secret findings only. The reviewer should receive path, variable name, and rule id, not raw secret values.

## Outputs

The reviewer should post PR comments on any high confidence medium+ severity findings using a predictable format:

```text
Security Review: Needs changes

Risk: Critical
Confidence: High
Decision: Block
Suggested owner: API owner

Finding:
- File: app/routes/records.py:27
- Issue: Route reads a record by caller-controlled ID without owner/staff authorization.
- Evidence: db.get_record(record_id) is called before any current_user ownership check.
- Impact: Authenticated users may retrieve another user's record.
- Suggested fix: Use an authorization-aware data access helper or pass current_user.id into the query.
```

Decision meanings:

- `Block`: deterministic evidence exists, such as a high-confidence Semgrep finding at `HIGH`, `CRITICAL`, or legacy `ERROR` severity
- `Comment`: the AI reviewer sees a plausible security concern or the severity is only a medium, but it does not necessitate blocking the CI
- `Needs Review`: the PR changes auth, authorization, record access, JWT handling, secret handling, or outbound network behavior in a way that needs human security review.

## Guardrails

- Do not block on anything except the highest confidence high severity vulnerabilities. 
- Require deterministic evidence for PR failure, AI reviewer cannot block without evidence
- Avoid sending raw secrets, tokens, environment files, or customer data to third-party models.
- Scope model input to changed files plus security-relevant neighbors instead of sending the whole repository, i.e do not scan static asset folders and scope test files accordingly.
- Detect likely false positives by checking for nearby owner/staff guards, authorization-aware helper names, and tests that prove cross-user denial.
- Log reviewer inputs, scanner rule versions, and model version for auditability.

## Evaluation

I would evaluate the reviewer with seeded PRs and ongoing review metrics:

- Seed broken access control variants, such as `db.get_record(record_id)` in a route without an owner check, search without `owner_user_id` filtering, and staff-only routes missing role checks.
- Seed safe variants, such as `list_records_for_user(current_user.id)`, role-aware data access helpers, and explicit staff guards before privileged access.
- Track whether high-confidence Semgrep findings are summarized accurately and never downgraded by the AI without human approval.
- Track false positives by measuring how often engineers mark AI comments as not actionable.
- Track false negatives by adding missed broken access control patterns back into Semgrep rules or regression tests.
- Collect engineering feedback on whether comments are specific enough to fix without a separate security meeting.

The goal is for AI to improve triage and developer experience while deterministic CI remains responsible for enforcing the security gate.
