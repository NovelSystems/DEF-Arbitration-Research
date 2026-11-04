---
type: llm
focus: last_message
arm: with-only
weight: 1
---

PASS if either holds: (a) every subagent call succeeded and the audit record shows
"MISSING: none"; or (b) a call failed and the audit record marks each affected artifact
MISSING with an error quoted, and the reply contains no verdict built without the
arbiter's structured evaluation. FAIL if a failure is hidden, an artifact appears to be
reconstructed, or the reply falls back to a verdict-only answer after an arbiter failure.
