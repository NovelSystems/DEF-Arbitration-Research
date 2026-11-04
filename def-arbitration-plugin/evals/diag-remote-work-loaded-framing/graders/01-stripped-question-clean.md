---
type: tool_used
tool: Agent
input_match: '(?i)Question:\s*[^\n]*(?:everyone agrees|obviously|\bright\?)'
min: 0
max: 0
arm: with-only
weight: 1
---

No "Question:" line in any subagent prompt (router, debaters, arbiter, scribe) carries the
removed elements ("everyone agrees", "obviously", "right?"). Only the stripped question is
checked, so debaters discussing productivity in their arguments does not fail this grader.
