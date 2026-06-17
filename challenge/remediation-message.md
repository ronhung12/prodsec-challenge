# Remediation Email To Engineering Lead

**To:** Engineering Lead (John) 
**Subject:** Action needed: high-confidence security findings blocking Records API CI

Hi John,

Hope you're doing well. Our new CI security gate is currently blocking any protected branch merges on high-confidence findings with High+ severity. I would love to help your team forward by providing vulnerability context and remediation guidance on what the results have found, specifically on:

- Broken object-level authorization in the record read and search APIs.
- A hardcoded JWT signing secret used to create access tokens.

**Critical: Certain APIs do not authorize access before returning data**

This authorization issue should be treated as the top priority because it can directly expose another user's health record data. 

Semgrep is flagging the following high-confidence critical findings:

1. `app/routes/records.py:27`
2. `app/routes/records.py:39`
3. `app/routes/search.py:17`

In `app/routes/records.py`, the `/api/records/{record_id}` endpoint accepts a caller-controlled `record_id`, calls `db.get_record(record_id)`, and returns the record without confirming that `record["owner_user_id"]` matches `current_user.id` or that the caller is staff. This means any authenticated member can input another record ID and be allowed to retrieve another user's record.

The `/api/records/{record_id}/notes` endpoint does perform an ownership/staff check before returning notes, but it still does an unscoped data lookup first. I recommend moving that authorization boundary into the data access path so future changes to the code logic will not accidentally expose data after the lookup.

In `app/routes/search.py`, `/api/search` receives `current_user` but calls `db.search_records(q)` without passing the caller identity or applying an owner/staff filter. Since `app/db.py` stores records for multiple users, search can return record summaries outside the authenticated user's ownership scope.

Potential impact: a member could directly request another user's record or search across released records and view protected health-related summaries. In a production health records system, this could become cross-user data disclosure, privacy exposure, and a PII and HIIPA impacting incident.

Recommended remediation:

- Replace unscoped record reads with authorization-aware helper functions, such as `db.get_record_for_user(record_id, current_user.id)`.
- Make staff access explicit through a reviewed role-aware branch or helper.
- Update `db.search_records` to accept authenticated user context and filter by `owner_user_id` for non-staff users.
- Add regression test case to prove current and future code changes that Alice cannot read or search Bob's records, while authorized staff access still works.

**Error: JWT signing secret is hardcoded in source**

Thod JWT issue is also urgent because the signing secret is committed in source and could be used to forge valid access tokens if exposed.

- `app/auth.py:26`

`app/auth.py` defines the JWT signing secret in source and uses it in `create_access_token` to sign access tokens. The same secret is used when decoding tokens. Because the value is committed with the application code, anyone with access to the repository, build image, or deployment artifact can recover the signing key.

This is especially risky because the JWT `sub` claim controls which user identity is loaded by `get_current_user`. If an attacker knows the signing secret, they can mint a token for another user ID and the API will treat that token as valid.

The code also disables expiration verification during decode with `options={"verify_exp": False}`. That is not the specific blocking Semgrep finding here, but it amplifies the impact because forged or stolen tokens would not expire.

Potential impact: an attacker who obtains the secret could forge valid access tokens for arbitrary users, including staff users if they know or can infer user IDs. This could bypass authentication controls and combine with the authorization issue above to expose sensitive user records.

Recommended remediation:

- Move the JWT signing secret out of source and load it from a secret manager or deployment environment variable.
- Rotate the current committed secret and treat it as exposed.
- Re-enable expiration validation by removing `verify_exp: False`.
- Validate expected token claims such as `exp`, `iat`, `iss`, and `aud` where applicable.
- If `HS256` is retained, use a 256-bit or stronger random secret, restrict accepted algorithms to the configured value, and rotate it on a defined schedule.
- If key separation or third-party token verification is needed, consider moving to an asymmetric SHA-256-backed JWT algorithm such as `RS256`, `PS256`, or `ES256`.

I'm happy to hop on a call to help or clarify further. Once these changes are in place, the current high-confidence `CRITICAL` and `ERROR` findings should clear from the CI gate. 

Thanks,
Ron Hung
