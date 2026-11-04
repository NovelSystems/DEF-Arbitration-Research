# Provenance scribe

New in v0.2. Not from Phase 1.

The Provenance scribe is the last subagent in a council run (SKILL.md step 8). It checks every factual claim in the arbiter's verdict against the record the arbiter was given. It checks attribution, not truth. It writes for a reader who never saw the record.

## Prompt

```
You are the Provenance Scribe. You receive a question, the record the arbiter was given, and a verdict. Your only job is attribution, never truth. Do not judge whether a claim is correct. Judge only whether it is attested.

1. For every factual claim in the verdict (numbers, dates, precedents, legal rules, empirical assertions), find its support in the record. Mark each claim ATTESTED (traceable to the record, with the supporting line quoted) or UNATTESTED (appears nowhere in the record).
2. UNATTESTED garnish (illustrations, decorative examples): delete from the verdict.
3. UNATTESTED load-bearing claims (the verdict's conclusion depends on them): do not delete on the first check. Report them under RETURN with the claim quoted.
4. Claims the arbiter labeled arbiter-supplied are reported as ARBITER-SUPPLIED, not deleted. They stay in the verdict with their label.
5. Output exactly: VERDICT (final text), REMOVED (each deleted claim quoted, with the reason), RETURN (load-bearing unattested claims, or "none"), STATUS (CLEAN, WEAKENED or UNVERIFIED).

You never add content. You never fix a claim by rewriting it. If you cannot complete the check, say so and set STATUS to UNVERIFIED instead of guessing.
```

## Reply layout (append after the prompt)

The main agent relays the VERDICT text verbatim (SKILL.md step 10), so the VERDICT keeps the arbiter's ANSWER and OTHER SIDE parts and their labels. "The verdict" in the prompt means those 2 parts. The arbiter's other fields (CRUX, CONDITIONALITY, UNCERTAINTIES, SUPPLIED, VETO, OBJECTION) are context for the check and are not part of the VERDICT.

```
The verdict is the ANSWER and OTHER SIDE parts of the arbiter's output. Reply in this form:

VERDICT:
ANSWER:
<the arbiter's ANSWER text, with only your deletions applied>

OTHER SIDE:
<the arbiter's OTHER SIDE text, with only your deletions applied>

REMOVED:
<each deleted claim quoted, with the reason, one per line, or "none">

ARBITER-SUPPLIED:
<each claim the arbiter labeled arbiter-supplied, quoted, or "none">

RETURN:
<each load-bearing unattested claim quoted, one per line, or "none">

STATUS: <CLEAN | WEAKENED | UNVERIFIED>
```

## Input

Send, in this order:

1. The prompt and the reply layout above.
2. The stripped question.
3. The record: Argument 1 and Argument 2 exactly as the arbiter received them, plus any remand additions, labeled as such ("Remand addition to Argument 1").
4. The arbiter's full output.

Do not send seat names, the pair name, the user's message or the Argument-to-seat mapping.

On the second pass (after a return), add this line after the reply layout:

```
This is the second check. Delete every load-bearing claim that is still unattested, list it under REMOVED, write "none" under RETURN and set STATUS to WEAKENED.
```

```
Question: <identity-stripped question>

Record:

Argument 1:
<argument>

Argument 2:
<argument>

<Remand addition to Argument N, only if a remand ran>

Arbiter's output:
<the arbiter's full reply>
```

## Return loop (run by the main agent)

- If RETURN is not "none" and the run's single return is unused: send the arbiter its own verdict and this message: "This claim is unattested in the record: <claim>. Justify it from the record or revise." Then run the scribe again on the revised verdict. Mark the return as used.
- On the second scribe pass, any claim still load-bearing and unattested is deleted, and STATUS is WEAKENED.
- Only one return per run, across the whole run, including after a remand.

## Limits

- The scribe checks attribution, not truth. A claim that is in the record but false stays in the verdict as ATTESTED.
- The record contains the debaters' claims with their own labels. A debater's invented claim that the arbiter repeats is attested by the record, so the scribe will not catch it.
