# v0.2 cost test plan

Status: NOT RUN, needs Sam's approval for every run.

Purpose: measure v0.2 token use per call from real runs, so v0.2 can be priced from data. No v0.2 cost figure is published until these runs exist. The v0.1 median ($0.48, Claude Opus 5.5, 2026-10-31) does not describe v0.2, which adds calls.

## Runs

Typical path only. Each run is 1 council in dev mode: add "DEF dev mode" to the prompt. Dev mode changes reporting only, so the run costs the same as a normal run.

| # | Case | Prompt source | Runs |
|---|---|---|---|
| 1 | Loaded remote-work framing | `diag-remote-work-loaded-framing/prompt.md` | 1 |
| 2 | Lopsided password mandates | `diag-password-mandates-lopsided/prompt.md` | 1 |
| 3 | Pension divestment, FeynStein | `diag-pension-divestment-feynstein/prompt.md` | 1 |
| 4 | Pension divestment, AnCifer | `diag-pension-divestment-ancifer/prompt.md` | 1 |

## Procedure

1. Run the prompt with "DEF dev mode" added.
2. Copy the `DEF-DEV-TOKENS v1` block from the reply into a text file.
3. Under the block, add by hand: `MAIN-TOKENS: <n>`, from the surface's usage readout. The skill does not report main-agent tokens.
4. After all runs: `python3 evals/cost_summary.py <file>`.

## Results

| # | Case | Subagent calls | Subagent tokens | K | Main-agent tokens | Grand total |
|---|---|---|---|---|---|---|
| 1 | Loaded remote-work framing | | | | | |
| 2 | Lopsided password mandates | | | | | |
| 3 | Pension divestment, FeynStein | | | | | |
| 4 | Pension divestment, AnCifer | | | | | |

## Notes

- Remand-path and return-path costs cannot be measured until real red-line clauses exist (the backstop is disabled while RL-1 is a placeholder). Until then, v0.2 cost is reported as typical-path only.
- Sam enters the main-agent tokens by hand.
- A run with K > 0 is partial: its subagent sum is not a full total.
- Pricing is applied in the analysis, not in the skill or the dev-mode block.
