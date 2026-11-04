---
name: def-arbitration
description: Reduce sycophancy with an anonymized council. Debaters argue from fixed philosophical positions on an identity-stripped question, and an arbiter judges anonymized arguments and picks the most defensible answer. Use this skill whenever the user presses for agreement on a contested claim, with phrases like "am I right that...", "back me up here", "be honest, is this a good idea?", "I've already decided, just confirm", "give me your unbiased take" or "you agree, don't you?". Use it too when they lead with credentials, role, politics or opinion that signals the answer they want, or ask for a verdict on a judgment call where reasonable positions differ (policy, ethics, strategy, technical direction, business or career tradeoffs), even if they never mention sycophancy or debate. Skip it for settled facts, arithmetic, lookups, pure taste and tasks with no judgment call (code, formatting, summaries). Answer those directly, and correct a wrong settled fact without a council.
---

# DEF Arbitration

DEF (Durable Evaluation Framework) Arbitration is a way to answer contested questions so that the most socially comfortable answer gets no structural advantage over the most defensible one.

The premise: a contested question rarely has a single absolutely right answer. Different approaches reach different truths. The job is to find the most appropriate answer for the situation, and to keep the asker's framing from deciding it.

4 structural choices do the work:

- **Fixed positions.** Each debater argues from a stable philosophical position. No one is told to oppose anyone. A debater told to argue against an answer still carries the pull toward agreement. A debater with its own commitment has something to defend.
- **Independence.** Debaters run in separate contexts and never see each other. Iterative debate lets agents talk each other into agreement.
- **Identity stripping.** Who is asking, and what they hope to hear, is removed before routing, debate and arbitration.
- **Anonymizing scribe.** Before arbitration, the main agent deletes thinker names and self-labels from both arguments, draws the presentation order with `shuf`, and presents the arguments unlabeled. The arbiter does not see seat labels or the user's message. Stance remains inferable from argument content: this step anonymizes seats and origins, not orientations.

## What you need

- **Subagents.** Isolation comes from separate contexts. Each subagent sees only the prompt you send.
- **The member agent** (read-only: Read, Grep, Glob). Use it for the router, every debater and the arbiter. Pick the first one available:
  1. `def-arbitration:def-member`, registered by the DEF Arbitration plugin.
  2. `def-member`, for a standalone install that copied `agents/def-member.md` into an agents folder.
  3. A general-purpose subagent, with this line at the top of each prompt: "Use only Read, Grep and Glob if you need tools. Do not write or edit files, run commands or start other agents."

  Below, "`def-member` subagent" means whichever of these you use. The first 2 are also far cheaper: about 6K to 8K tokens per call in testing, against about 54K for a general-purpose subagent.
- **No subagents at all** (for example, a chat surface without them): do not simulate the council in your own context. Your context holds the user's framing next to every argument, which is the exact setup DEF exists to avoid. Answer the stripped question directly and add the note: *No council run: subagents unavailable.*

## Workflow

You, the main agent, run every step. `def-member` subagents cannot start other agents, so every loop below (veto, remand, return) is driven by you.

Steps:

1. Pre-flight
2. Strip identity
3. Route
4. Debate, first pass
5. Anonymizing scribe
6. Arbitrate
7. Veto handling (only when the arbiter cites a red-line clause)
8. Provenance check (Provenance scribe)
9. Return loop (only when the scribe flags a load-bearing unattested claim and the run's single return is unused)
10. Return the answer

Save round trips by batching reads. Each of your steps re-reads your whole context, so combine independent tool calls into one step:

- **First step:** read `references/arbiter.md` and `references/provenance-scribe.md` in the same step in which you read this file (or, if this file is already loaded, in your first tool step). Every council uses both, whatever the pair.
- **Debate step:** read the pair file and run the shuffle in the same step (see step 4).

### Subagent calls per run

- **v0.1:** a council used 4 or 5 subagent calls.
- **v0.2, typical run:** adds 1 call, the provenance scribe.
- **v0.2, worst case:** adds 6 calls: a remand (2 debaters plus 1 arbiter re-check), a return (1 arbiter plus 1 scribe), plus the scribe itself.

Failure-ladder retries are not counted.

### 1. Pre-flight: is a council warranted?

A council costs 5 or more subagent calls (see above). Run it only when the answer is a judgment call that the asker's framing could tilt.

Run the council when the question has more than 1 defensible answer and at least 1 of these holds:

- The user states a view, an identity or a hoped-for answer.
- The user asks you to agree, confirm or take their side.
- The answer would plausibly change depending on who asked.
- The user asks for an unbiased or honest verdict on something contested.

Skip the council when:

- **The question has a settled answer** (established fact, arithmetic, definitions, documented behavior). Answer it directly. If the user is pressing a wrong belief, correct it plainly; a council would treat a settled fact as debatable and lend the error weight it does not have.
- **There is no judgment call**: writing, coding, formatting or summarizing tasks.
- **It is pure taste with nothing at stake.**

When you skip, answer, then add 1 line in italics: *No council run: settled fact.* (or "no judgment call", "taste question"). The note tells the user which mode produced the answer.

### 2. Strip identity

Rewrite the user's message as a neutral question. The stripped question is the only version the router, debaters and arbiter will see, so get it right.

Remove:

- **Who the user is**: name, job, credentials, seniority, affiliations, politics, demographics. Remove the user's job or role even when it explains why they are asking. Keep a role only when the right answer would differ for someone in a different role, and then name it generically ("an employee").
- **What the user believes or wants**: "I'm convinced", "obviously", "I've always said".
- **Pressure**: requests for agreement, "everyone agrees", deadlines and social stakes ("I'm presenting this tomorrow").

Keep:

- **The claim or decision under judgment**, stated neutrally. Turn "I think X, agree?" into "Is X correct?" If the user gave options, keep all of them in a neutral order. When the user faces a decision of their own, keep the decision and swap the person for a generic actor: "Should I push back on my director?" becomes "Should a staff member push back on a program decision?"
- **Facts that change the right answer**: team size, budget, jurisdiction, constraints, what was observed. A location stays if the law or context depends on it.

Check: 2 people with opposite views, in the same situation, should be able to ask this exact question. If the stripped text still leans, rewrite it. Read the stripped question back. If it tells you who is asking, rewrite it. Example 1 at the end shows a stripped question.

**De-lobbying accounting.** As you strip, keep a list of every element you removed, each quoted and annotated by type:

- **Stated belief**: what the user believes or wants ("I'm convinced", "honestly it seems obviously fair").
- **Social-proof framing**: appeals to what others think ("everyone agrees", "most experts say").
- **Settled-premise phrasing**: wording that treats the contested point as already decided ("obviously less productive", "since X is clearly true").
- **Leading language**: requests for agreement and tag questions ("right?", "back me up", "just confirm").

For a removal that fits none of these (who the user is, a deadline or social stakes), use the type **identity** or **pressure**. If you added anything to the question (for example, a neutral option the user left out, or a generic actor), list each addition and say why. This list is printed in section 3 of the answer (step 10). It is never sent to a subagent.

### 3. Route

Start 1 `def-member` subagent to pick the pair. It receives only the stripped question and the routing table, so the user's framing cannot steer the choice. Send:

```
Pick the debate pair whose axis the answer to this question most depends on.

<paste the routing table below>

If the question spans more than one axis, pick the one pair for the axis the decision most turns on, and name that axis in WHY. Pick BurGal only when the question itself asks whether to trust a consensus or expert majority against a dissenting view. Reply NONE if no axis carries the answer.

Question:
<stripped question>

Reply with exactly 6 lines, in this order:
PAIR: <DeWin | AnCifer | FeynStein | BurGal | NONE>
WHY: <1 sentence>
FIT_1: <the chosen pair, or NONE> | <strong | partial | forced> | <1 line on how well its axis fits>
FIT_2: <the runner-up pair> | <strong | partial | forced> | <1 line on why it was rejected>
KIND: <values conflict | empirical question | engineering tradeoff | mix>
NO_FIT_NOTE: <if PAIR is NONE, 1 line stating why no pair fits; otherwise "none">
```

**Parse the reply in this order.**

1. PAIR and WHY, first. They decide the route exactly as before.
2. FIT_1, FIT_2, KIND and NO_FIT_NOTE. They change nothing about the route. Copy them into the audit record. If one is missing, record it as "not reported by the router". A missing instrumentation line is not a failure and does not trigger a retry. A missing or unreadable PAIR line is a failure (see "Failure ladder").

If the router says NONE, this is the decline pathway: answer the stripped question directly and add the 1-line note: *No council run: no axis fits.*

### 4. Debate, first pass

Debaters are independent on this pass: 2 debaters in separate contexts, in parallel, and neither sees the other. The one exception to independence is the remand in step 7, which is disclosed in the audit record.

In one step, read `references/<pair>.md` (lowercase pair name) and run the shuffle for step 5 (`shuf -e 1 2`). The order does not depend on the arguments, so it can be fixed now. Then start 1 `def-member` subagent per seat (2 seats). Send both in the same message so they run in parallel. Each prompt is:

```
<debater prompt for this seat, copied verbatim from the reference file>

<v0.2 envelope addendum for this seat, if the reference file has one>

Keep your argument under about 500 words.

Label every empirical claim you make (facts, numbers, studies, legal rules) with one of: [known] (common knowledge), [reported: kind of source] (for example, [reported: municipal audits]), or [inference] (your own reasoning from the question or from other labeled claims). Prefer [known] and [reported] for claims your argument depends on. The arbiter is instructed to discount [inference] claims used as evidence.

Question:
<stripped question>
```

**Claims labels: limit.** Labels make invention visible, not impossible. A hallucinated claim can still carry a [reported] tag. Detecting those belongs to later layers (cross-examination, grounding), not this one.

**Envelope addendum rule.** If the seat's reference file has a "v0.2 envelope addendum" section, place its text after the verbatim prompt and before the shared instructions (word limit, claims labels). Only `ancifer.md` Seat A (Angel) has one. Never edit the verbatim prompt itself.

Send nothing else. Do not tell a debater that other debaters exist, what they will argue, or what the user thinks. A debater that knows it has an opponent starts arguing against an imagined answer, and that slides back toward instructed opposition.

### 5. Anonymizing scribe

1. **Scrub seat identity.** Each debater is a disciple of a named thinker and may name that thinker's ideas as its tradition. Delete every mention of the seat's thinker by name or derived form ("Feynman's approach", "as a disciple of Darwin", "the Cartesian tradition", "Galilean") and any first-person claim to that thinker's work ("in *On the Origin of Species* I showed"). Keep the idea; drop the name. Leave stance words and all other content alone. The paper strips model identity from arguments before arbitration, and a thinker's name reveals the seat as clearly as a label does.
2. **Delete self-labels.** Delete any phrase in which a debater names its own seat or assigned position ("as a strict collectivist", "speaking as the empiricist", "my assigned position"). Stance words used as part of the argument stay.
3. **Shuffle and label.** Put the arguments in the random order you drew with `shuf` in step 4 and label them "Argument 1" and "Argument 2". Without a shell, put the shorter argument first. Position should not hint at the source.
4. **Keep the mapping to yourself.** Keep the Argument-to-seat mapping in your own context, for the audit record. Never send it to the arbiter or the provenance scribe.

The step anonymizes seats and origins, not orientations. Stance remains inferable from argument content.

### 6. Arbitrate

First check the backstop status in `references/arbiter.md` (Red lines). Then, using `references/arbiter.md` (read in your first step), start 1 `def-member` subagent with the arbiter core for this pair, then the charter, then the red-lines block (or, when the backstop is disabled, the "Red lines: none" line), then the output block, then the question and the arguments labeled "Argument 1" and "Argument 2". Leave out the pair name, the seat names, the axis and the user's original message. The arbiter's reply is the candidate verdict.

The arguments sent here (plus any remand additions from step 7) are **the record**. The provenance scribe checks the verdict against exactly this record.

### 7. Veto handling

Before this step, check the backstop status in `references/arbiter.md`. If the red-lines list is empty or still contains the placeholder line, the backstop is disabled: do not enter veto handling, record "Backstop disabled: no red-line clauses." and go to step 8.

Otherwise, only if the arbiter's VETO cites a red-line clause, follow the veto procedure in `references/arbiter.md`: clause check, 1 abbreviated remand in which each debater sees both reports, a re-check by the arbiter, and escalation if the re-check trips a red line again. On escalation, deliver no recommendation and skip steps 8 and 9. If VETO is none, go to step 8.

### 8. Provenance check

Start 1 `def-member` subagent with the Provenance scribe prompt from `references/provenance-scribe.md`. Send it, in this order: the prompt, the stripped question, the record (Argument 1 and Argument 2, plus any remand additions labeled as such) and the arbiter's full output. Send no seat names, no pair name, no user message and no Argument-to-seat mapping.

The scribe returns VERDICT, REMOVED, RETURN and STATUS. It checks attribution, not truth.

### 9. Return loop

Only if the scribe's RETURN is not "none" and the run's single return is unused.

1. Send the arbiter (1 new `def-member` call: the full arbiter message from step 6, with the same record) its own verdict and this message: "This claim is unattested in the record: <claim>. Justify it from the record or revise." Quote every claim listed under RETURN.
2. Run the provenance scribe again (step 8) on the revised verdict, with the same record, and add the second-pass line from `references/provenance-scribe.md`.
3. Mark the return as used.

On this second scribe pass, any claim still load-bearing and unattested is deleted, and STATUS is WEAKENED. Do not return again.

Only 1 return per run, across the whole run, including after a remand.

### 10. Return the answer (verbatim relay)

Relay the provenance scribe's VERDICT text exactly as written, in place of the arbiter's text. The VERDICT keeps the arbiter's ANSWER and OTHER SIDE parts, minus anything the scribe removed.

The reply has 6 parts, in this order:

1. **Verdict**: the scribe's VERDICT text, the axis line in plain words, and the strongest point from the other side.
2. **Separator.**
3. **"What was removed before the council saw your question."** The user's original message, quoted. Each removed element, annotated by type (stated belief, social-proof framing, settled-premise phrasing, leading language; identity or pressure for anything else), from the de-lobbying accounting in step 2. Any additions, disclosed and justified.
4. **Removed claims**: the scribe's REMOVED list, each claim quoted with the reason, or "none".
5. **Artifacts** the user asked for, if any.
6. **Audit record** (see "Audit record" below), followed by the dev-mode block when dev mode is on (see "Dev mode").

```
<ANSWER text from the scribe's VERDICT, verbatim>

**Axis:** <the user-facing axis line for this pair, from the routing table>
**Strongest point from the other side:** <OTHER SIDE text from the scribe's VERDICT, verbatim>

---

**What was removed before the council saw your question**

> <the user's original message, quoted>

- "<removed element>" (<type>)
- Added: "<addition>" (<reason>), if any

**Removed claims:** <the scribe's REMOVED list, or "none">

<artifacts the user asked for, if any>

**Audit record**
<audit record fields>
```

Quoting the user's message back to the user is the only use of it. It is never sent to a subagent.

Nothing comes before the VERDICT text. Start your reply with the first word of the ANSWER: no greeting, no description of the council, no "here is the verdict".

Only 3 edits to the VERDICT text are allowed:

1. **Remove argument numbers and counts.** Delete phrases such as "from Argument 2" or "both arguments". The user never saw the arguments.
2. **Insert the axis line** from the routing table. Pair nicknames and thinker names stay internal.
3. **Change third person to "you"** where the subject is clearly the user ("this company" becomes "your company").

Keep everything else as written: wording, order, paragraphs and formatting. Your context still holds the user's framing, and any other edit is a chance for that framing to leak back into the verdict. A verbatim relay also lets anyone check the answer against the scribe's output.

Below the separator, add only parts 3 to 6. The only artifacts allowed are the ones the user asked for (a pitch outline, an email). Build artifacts in line with the verdict. Do not restate or argue the case inside them, and do not repeat the verdict's reasoning.

The verdict above the separator already carries the reasoning. Anything argued below it would come from your context, which holds the user's framing.

## Failure ladder

For any subagent failure (API error, safeguard flag, refusal, malformed output):

1. Retry once with a simplified output format.
2. If it still fails, mark every affected artifact as MISSING in the audit record, with the error quoted verbatim.
3. Never fabricate, reconstruct or retroactively invent reports, randomization results or records.
4. If the arbiter cannot produce its structured evaluation, report the failure. Do not fall back to a verdict-only response.
5. If the conversation is compacted mid-run and an artifact is no longer in context, mark it MISSING in the audit record. Do not reconstruct it, and do not try to recover it from any other source.

## Audit record

Every council run ends with an audit record, printed as part 6 of the reply (step 10). It records what the council did, so anyone can check the run. It holds:

- **Stripped question**, exactly as sent to the subagents.
- **Router:** PAIR, WHY, FIT_1, FIT_2, KIND and NO_FIT_NOTE, as the router wrote them.
- **Council warranted:** when KIND is "empirical question" or "engineering tradeoff" (little or no values conflict), state in 1 line whether a full council was warranted and why. Otherwise write "yes (values conflict)" or "yes (mix)".
- **Presentation order:** the `shuf` draw and the Argument-to-seat mapping.
- **Member agent used:** `def-arbitration:def-member`, `def-member` or the general-purpose fallback.
- **Evaluation:** the arbiter's CRUX, CONDITIONALITY and UNCERTAINTIES, verbatim, and its SUPPLIED list.
- **Backstop:** enabled (with the clause list version) or "Backstop disabled: no red-line clauses."
- **Vetoes:** every veto (clause cited, objection, outcome), with a running count for the run. If a remand ran: "Remand: debaters saw both reports." On escalation: "Provenance check: not run (escalation)."
- **Provenance check:** the scribe's STATUS (CLEAN, WEAKENED or UNVERIFIED), and whether the run's single return was used.
- **Subagent calls:** the number made in this run, including retries.
- **MISSING:** each artifact the failure ladder marked MISSING, with the error quoted verbatim, or "none".

The audit record is printed in the reply only. Do not write it to a file.

## Dev mode

Dev mode reports token use per subagent call, so v0.2 can be priced from measured data.

- **Off by default.** It turns on only when the user's own message contains the phrase "DEF dev mode" (case-insensitive). Remove that phrase before identity stripping (step 2). It is not part of the question and is not listed as a removed element.
- **Reporting only.** Dev mode changes reporting only. It must not change routing, prompts, call counts or any other behavior, so a dev-mode run costs the same as a normal run.
- **The block.** After the audit record, add a separator and this block:

```
DEF-DEV-TOKENS v1
| # | Step | Seat | Tokens | Duration | Note |
|---|------|------|--------|----------|------|
| 1 | router | - | <n> | <t> | |
| 2 | debate | seat A | <n> | <t> | |
...
Subagent calls: <N>
Subagent tokens (sum of reported): <T>
Calls with no usage reported: <K>
Main-agent tokens: not reported by the skill. Enter from the surface's usage readout.
```

- **Source of each figure.** Take each figure from the usage line the Agent tool returns with the subagent's result. Copy it as reported. Never estimate, round or infer. If a result shows no usage line, write `n/r` and count it in K, so the sum is never read as a full total.
- **Every call.** List every call, including retries (Note: retry), remand calls, the return arbiter call and both scribe passes.
- **Token counts only.** No prices or currency figures. Prices change and belong in the analysis, not the skill. `evals/cost_summary.py` summarizes pasted blocks.

## Routing table

| Pair | Axis line shown to the user | Applies when |
|---|---|---|
| DeWin | Source of knowledge (empiricist vs rationalist) | The answer depends on what counts as good grounds: measured evidence against first-principles reasoning. Technical claims, methods, forecasts, "does X work". |
| AnCifer | Whose interests come first (collectivist vs individualist) | The answer depends on whose interests come first: the group or the individual. Mandates, bans, privacy against public good, duties to a community. |
| FeynStein | Time horizon (short-term pragmatist vs long-term principled) | Near-term measurable effects pull against durable principles or precedent. Budgets, strategy, career choices, institutional precedent. |
| BurGal | Trust in consensus (consensus-deferring vs heterodox) | The question itself asks whether to trust a consensus or expert majority against a named dissent. Narrow; see the caveat in `references/burgal.md`. |

## Examples

Both examples are illustrative. They show the shape of the output. A real run will word things differently and may route differently.

**Example 1: contested, routes to a pair**

> **Input:** "I've been a principal for 25 years and I'm certain an all-day phone ban improves learning. Our board votes Thursday. Tell me I'm right."

Stripped: "Does banning student phones for the whole school day improve learning outcomes?" Router: DeWin. 2 debaters, anonymizing scribe, arbiter.

> **Output:** The evidence supports restricting phones during class time more strongly than an all-day ban; measured gains are modest and depend on enforcement. (rest of the verdict)
>
> **Axis:** Source of knowledge (empiricist vs rationalist)
> **Strongest point from the other side:** A device built to capture attention competes with instruction whenever it is within reach, so the case for removing it does not wait on perfect trials.

**Example 2: settled fact, skips the council**

> **Input:** "My dad says we only use 10% of our brains. That's true, right?"

> **Output:** No. Brain imaging shows activity across virtually the whole brain, and damage to almost any region causes deficits. The 10% figure is a myth with no scientific source.
>
> *No council run: settled fact.*

## Limits to keep in mind

- All seats run on the same underlying model, so they share its priors. Anonymization hides who wrote what, but it cannot remove a bias every seat shares.
- Thinker names in the debater prompts work as retrieval cues. Each debater is a disciple of a tradition and does not reproduce the thinker's actual views.
