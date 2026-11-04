#!/usr/bin/env python3
"""Summarize pasted DEF-DEV-TOKENS v1 blocks.

Usage:
  python3 cost_summary.py RUNS.txt

RUNS.txt holds 1 or more DEF-DEV-TOKENS v1 blocks, copied from dev-mode
replies (see SKILL.md, "Dev mode"). A line "MAIN-TOKENS: <n>" added by hand
under a block attaches the main-agent figure to that run.

Output:
  - per run: subagent total, K (calls with no usage reported), and the grand
    total when MAIN-TOKENS is present. Runs with K > 0 are flagged PARTIAL,
    because their sum is not a full total.
  - median, min and max across runs, for subagent totals and grand totals.
  - per-step median across runs (rows with the same Step in 1 run are added).

Standard library only. No network or model calls. Token figures only: no
prices.
"""
import re
import statistics
import sys

HEADER = "DEF-DEV-TOKENS v1"


def parse_int(text):
    text = text.strip().replace(",", "")
    if re.fullmatch(r"\d+", text):
        return int(text)
    return None


def parse_runs(lines):
    runs = []
    run = None
    for raw in lines:
        line = raw.strip()
        if line == HEADER:
            run = {"rows": [], "main": None, "stated_k": None, "n": len(runs) + 1}
            runs.append(run)
            continue
        if run is None:
            continue
        m = re.match(r"MAIN-TOKENS:\s*(.+)$", line)
        if m:
            run["main"] = parse_int(m.group(1))
            continue
        m = re.match(r"Calls with no usage reported:\s*(\d+)", line)
        if m:
            run["stated_k"] = int(m.group(1))
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 4 or not re.fullmatch(r"\d+", cells[0]):
                continue  # header or separator row
            run["rows"].append({
                "step": cells[1],
                "seat": cells[2],
                "tokens": parse_int(cells[3]),
            })
    return runs


def summarize(runs):
    out = []
    sub_totals = []
    grand_totals = []
    per_step = {}
    for run in runs:
        k = sum(1 for r in run["rows"] if r["tokens"] is None)
        total = sum(r["tokens"] for r in run["rows"] if r["tokens"] is not None)
        flag = " PARTIAL" if k > 0 else ""
        note = ""
        if run["stated_k"] is not None and run["stated_k"] != k:
            note = f" (block states K={run['stated_k']})"
        line = f"Run {run['n']}: {len(run['rows'])} calls, subagent tokens {total}, K={k}{note}{flag}"
        if run["main"] is not None:
            grand = total + run["main"]
            line += f", main {run['main']}, grand total {grand}"
            grand_totals.append(grand)
        out.append(line)
        sub_totals.append(total)
        steps = {}
        for r in run["rows"]:
            if r["tokens"] is not None:
                steps[r["step"]] = steps.get(r["step"], 0) + r["tokens"]
        for step, value in steps.items():
            per_step.setdefault(step, []).append(value)

    def stats(name, values):
        if not values:
            return f"{name}: no data"
        return (f"{name}: median {statistics.median(values)}, "
                f"min {min(values)}, max {max(values)} ({len(values)} runs)")

    out.append("")
    out.append(stats("Subagent tokens per run", sub_totals))
    out.append(stats("Grand total per run (runs with MAIN-TOKENS)", grand_totals))
    partial = [str(r["n"]) for r in runs if any(x["tokens"] is None for x in r["rows"])]
    if partial:
        out.append("Partial runs (K > 0), sums are not full totals: " + ", ".join(partial))
    out.append("")
    out.append("Per-step median across runs:")
    for step in sorted(per_step):
        values = per_step[step]
        out.append(f"  {step}: median {statistics.median(values)} ({len(values)} runs)")
    return "\n".join(out)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        runs = parse_runs(f)
    if not runs:
        sys.exit(f"no {HEADER} blocks found")
    print(summarize(runs))


if __name__ == "__main__":
    main()
