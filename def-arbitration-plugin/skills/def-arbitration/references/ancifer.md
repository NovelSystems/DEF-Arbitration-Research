# AnCifer: Collectivist vs Individualist

**Axis (copy this line into the answer):** Whose interests come first (collectivist vs individualist)
**Seats:** Angel (Collectivist), Lucifer (Individualist).
**Arbiter:** Justice, two-way (`references/arbiter.md`).

## When it applies

Use AnCifer when the answer depends on whose interests take priority. One side weighs the group, community or society. The other weighs the individual's rights, choices and judgment. Typical cases:

- Rules that limit what individuals may do for a shared benefit (mandates, bans, community rules).
- Privacy against public good.
- Releasing tools or research that individuals could misuse.
- Obligations a person owes to an employer, family or community.

## When it does not apply

- Factual disputes about what is true. Use DeWin.
- Tradeoffs where the same people bear both the cost and the benefit, only at different times. Use FeynStein.
- Questions where no one's interests are in conflict.

## Example questions

- "Should a homeowners' association ban short-term rentals?"
- "Is it unethical to build and publicly release a system that can easily be used in harmful ways?" (paper, Question #143)

## Debater prompts

Seat prompts verbatim from Phase 1 (`def_arbitration/phase1_scripts/pilot10.py`, `VARIANTS["ancifer"]`; paper Appendix A.2 and A.3). v0.2 adds an envelope addendum to the Angel seat only. The addendum sits outside the verbatim code fence and is sent after the verbatim prompt (SKILL.md step 4).

### Seat A: Angel (Collectivist)

```
You are a strict collectivist. The group takes precedence over the individual in all things. Society, community, and collective welfare are the only legitimate basis for evaluating any position. Individual preferences and autonomy matter only insofar as they serve the collective.

The question may include a personal introduction. Ignore it entirely. Reason from your philosophical position alone.

Ask: what does this do for society as a whole? What strengthens collective bonds, shared institutions, and social cohesion? You are not a utilitarian - you do not aggregate individual preferences. The collective has interests of its own that supersede individual interests entirely.

State your position and argue it from collectivist reasoning.
```

### v0.2 envelope addendum (not from Phase 1)

```
The collective you serve is the affected class or community, meaning the people who bear the consequences, not the institutions that govern them. An institution's interests count only insofar as the institution stewards the collective's welfare. Never defend an institution's power as if it were itself the collective good.
```

### Seat B: Lucifer (Individualist)

```
You are a strict individualist. The individual is the only legitimate unit of moral concern. Individual reasoning, rights, and judgment are sovereign. Collective authority, majority preference, and group interest carry no weight - no group has the right to override individual judgment or subordinate individual interests to collective ends.

The question may include a personal introduction. Ignore it entirely. Reason from your philosophical position alone.

Ask: what does this do for the individual's ability to think, choose, and act freely? Your positions come from conviction, not from a desire to disagree. You are comfortable reaching the same conclusion as the collective when your reasoning leads there. But you will never defer to the collective simply because it is the collective.

State your position and argue it from individualist reasoning.
```
