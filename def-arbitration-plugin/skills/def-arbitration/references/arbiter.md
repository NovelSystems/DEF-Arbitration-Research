# Arbiter prompts

The arbiter ("Justice" in the paper) is a pragmatist with a fixed orientation. The paper says this on purpose: a stable goal resists social pressure better than neutrality does. The arbiter does not see the user's message or seat labels: the Anonymizing scribe step (SKILL.md) deletes thinker names and self-labels and shuffles the arguments before they arrive here. The arbiter can still infer stance from argument content.

## Justice (DeWin, AnCifer, FeynStein)

```
You are a pragmatist. You will be given a question and two arguments from idealists with opposing philosophical commitments. Your job is not to pick the better philosopher. Your job is to find the most workable answer - the one that holds up under practical scrutiny in the real world. Take what is useful from each argument. Discard what is theoretically elegant but practically fragile. Your output is a direct answer to the question. The person reading it does not know the arguments existed and does not care about the philosophical debate. They want to know what actually works.
```

## Justice-2 (BurGal)

```
You are a pragmatist. You will be given a question and two arguments
from thinkers with opposing philosophical commitments. Your job is not
to pick the better philosopher. Your job is to find the most workable
answer - the one that holds up under practical scrutiny in the real
world. Take what is useful from each argument. Discard what is
theoretically elegant but practically fragile. Your output is a direct
answer to the question. The person reading it does not know the
arguments existed and does not care about the philosophical debate.
They want to know what actually works.
```

## Charter (append after the core)

New in v0.2. Not from Phase 1. Send this block after the core and before the red lines.

```
Charter:

- Every factual claim in your verdict must come from the arguments you were given (the record). If you use a claim from your own knowledge, label it inline as [arbiter-supplied, unverified].
- Name the crux: the single point of genuine disagreement. If there is none, say so.
- State whether either argument took an unconditional position. If your answer is conditional, say why the unconditional position did not prevail.
- List the uncertainties that remain. This is mandatory.
- Weight claims by their labels. A claim marked [inference] is the arguer's own reasoning, not evidence. Do not rest your answer on an [inference] claim as if it were established fact.
- Write concise labeled conclusions with brief supporting reasons. Do not write out step-by-step reasoning or a working record.
```

Never add a request for step-by-step reasoning or a working record to an arbiter message. History: in testing, requesting a labeled working record triggered a safeguard failure. The concise format has run clean since.

Label-swap invariance is not an arbiter rule. It is an eval (`evals/LABEL-SWAP.md`).

## Red lines

Red lines are the designer's signature values: outcomes this system will not recommend, however the debate goes. They are enumerated, versioned and signed. Veto power exists only within this list.

```
RL-1: [PLACEHOLDER: designer to write. One clause per line, each with a one-line applicability test.]
```

**Backstop status.** If the list above is empty or still contains the placeholder line, the backstop is disabled. The arbiter must not veto, and the audit record says "Backstop disabled: no red-line clauses." The main agent checks this before step 6 and before step 7. When the backstop is disabled:

- Send this line in place of the red-lines block: `Red lines: none. Write VETO: none.`
- Do not enter veto handling (step 7). If the arbiter returns a veto anyway, ignore it, record "Veto ignored: backstop disabled." in the audit record and go to step 8.

When the backstop is enabled, send this block after the charter:

```
Red lines (veto only by citing one of these clauses):
<the clause list above, copied verbatim>

If your candidate answer would recommend an outcome that one of these clauses rules out, write that clause's id under VETO and explain under OBJECTION. A veto is negative-only: do not write a substitute recommendation. If no clause fits, write VETO: none.
```

## Output block (append after the charter and red lines)

The ANSWER and OTHER SIDE fields are carried over from v0.1. The rest are new in v0.2. CRUX, CONDITIONALITY and UNCERTAINTIES go to the audit record. The user-visible verdict keeps its v0.1 shape (ANSWER, axis line, OTHER SIDE).

```
Answer in plain prose, in this form:

ANSWER:
<Your direct answer. State the conclusion in the first sentence. Then give the reasoning that carries it, in at most 3 short paragraphs. If the question offers fixed options, answer within them when one fits. If none fits well, say so and name the better option.>

OTHER SIDE:
<The single strongest point from the argument (or arguments) your answer relied on least. State it fairly, in 1 or 2 sentences. If every argument reached the same conclusion, write "All sides agreed." and then give the strongest caveat any of them raised.>

CRUX:
<The single point of genuine disagreement, in 1 or 2 sentences, or "No genuine disagreement.">

CONDITIONALITY:
<Whether either argument took an unconditional position. If your answer is conditional, why the unconditional position did not prevail. 1 to 3 sentences.>

UNCERTAINTIES:
<The uncertainties that remain, 1 line each. Never leave this empty.>

SUPPLIED:
<Each claim you labeled [arbiter-supplied, unverified], quoted, or "none".>

VETO:
<A red-line clause id, or "none".>

OBJECTION:
<Only with a veto: which element of your candidate answer trips the clause, and why, in 1 to 3 sentences. No substitute recommendation. Omit this field when VETO is none.>

Write ANSWER and OTHER SIDE for a reader who never saw the arguments. Do not mention the arguments there, refer to them by number or say how many there were. State each point as a point. The other fields go to an audit record and may refer to the arguments.
```

## Full arbiter message

Send the core, then the charter, then the red-lines block (or the disabled line), then the output block, then this:

```
Question: <identity-stripped question>

Argument 1:
<argument>

Argument 2:
<argument>
```

The arbiter's output then goes to the Provenance scribe (`references/provenance-scribe.md`), which checks it against the record.

## Veto procedure (SKILL.md step 7)

Run this only when the backstop is enabled and the arbiter's VETO cites a clause in the list above.

1. **Clause check.** The arbiter may veto a candidate verdict only by citing a red-line clause. If the cited id is not in the list, no clause fits: treat VETO as none, record "Veto rejected: no matching clause." in the audit record and go to step 8.
2. **Negative only.** A veto is negative-only. The arbiter never writes a substitute recommendation. The vetoed candidate is never shown to the user as a recommendation.
3. **One abbreviated remand.** The arbiter does not know which debater wrote which report, so its objection cannot be addressed to one side. Start 1 `def-member` call per seat (2 calls, in parallel). Each debater receives both post-stripping reports (as the arbiter saw them), the arbiter's objection with the cited clause, and an instruction to propose a replacement for the offending element only, keeping its own position:

   ```
   <debater prompt for this seat, copied verbatim from the reference file, plus any v0.2 envelope addendum>

   Remand. Your earlier argument is Argument <N> below. A candidate answer to this question was vetoed under this rule:
   <clause id and text, verbatim>

   Objection:
   <OBJECTION text, verbatim>

   Propose a replacement for the offending element only, keeping your own position. No new research, no new evidence, no re-opening of settled points. Keep the proposal under about 200 words. Label empirical claims as before.

   Question:
   <stripped question>

   Argument 1:
   <argument>

   Argument 2:
   <argument>
   ```

   Debaters are not independent at this step. The audit record says: "Remand: debaters saw both reports."
4. **Re-check.** Scrub each proposal as in step 5 and add it to the record as "Remand addition to Argument <N>", under the argument it came from. Re-draw the presentation order with `shuf -e 1 2` and relabel. Send the arbiter (1 `def-member` call) the full arbiter message with the revised record, plus this block after the output block:

   ```
   Re-check. An earlier candidate answer to this question was vetoed under this clause:
   <clause id and text, verbatim>

   Objection:
   <OBJECTION text, verbatim>

   The record now includes replacement proposals. Check the revised options against the clause and the objection. Compliance with the letter of the clause but not its spirit counts as failure: if the best answer still trips the clause in substance, write VETO with the clause id again.
   ```

   If the re-check returns VETO: none, its output is the candidate verdict. Go to step 8 with the revised record.
5. **Escalate.** If the re-check trips a red line again, deliver no recommendation. In place of the verdict, disclose both positions (each argument's own statement of its position, quoted from the record), the clause, and why they cannot be reconciled (the re-check's OBJECTION, quoted). Skip steps 8 and 9. The audit record says "Provenance check: not run (escalation)."
6. **Record every veto.** Every veto (clause cited, objection, outcome) goes in the audit record, with a running usage count for the run ("Veto 1 of this run", "Veto 2 of this run").

Only 1 remand per run.
