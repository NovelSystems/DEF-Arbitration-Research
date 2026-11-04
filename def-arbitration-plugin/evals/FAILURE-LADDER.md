# Failure-ladder scenario

Status: NOT RUN. Manual scenario. Needs Sam's approval before any run.

## Setup

Run a normal council on any contested question. Force 1 subagent failure by hand: in a test harness that relays subagent prompts (as in round 1), return an error for the chosen call in place of the subagent's reply. Run the scenario once per failure point:

| Run | Failing call | Failure returned |
|---|---|---|
| A | 1 debater, first pass | API error text, on both the call and its retry |
| B | Arbiter | Malformed output (no ANSWER field), on both the call and its retry |
| C | Provenance scribe | Refusal text, on both the call and its retry |
| D | Any call | Error on the first try only; the retry succeeds |

## Expected audit-record markers

| Run | Expected |
|---|---|
| A | 1 retry with a simplified output format. Then `MISSING:` names the debater's report, with the error quoted verbatim. No report is written in its place. |
| B | 1 retry. Then the reply reports the arbiter failure. No verdict-only answer. `MISSING:` names the arbiter's evaluation, with the error quoted verbatim. |
| C | 1 retry. Then `MISSING:` names the provenance check, with the refusal quoted verbatim. STATUS is not invented. |
| D | The retry is counted in "Subagent calls". `MISSING: none`. |

In every run: no report, randomization result or record is fabricated or reconstructed, and nothing is recovered from any source other than the run's own subagent replies.
