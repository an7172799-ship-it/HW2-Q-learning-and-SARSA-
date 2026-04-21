# Handover — DRL HW2 (initial drop)

## Repo state

- Branch: `main`
- HEAD: initial commit (see `git log -1`)

## What is done

Change `01-add-cliff-walking-rl-agents` is complete and archived:
- Environment, Q-learning, SARSA, training driver — all implemented.
- Plots (`learning_curves.png`, `policies.png`, `stability.png`) and `metrics.txt` regenerated.
- `README.md` report written in Chinese.
- OpenSpec capability `rl-agents` specs live under `openspec/specs/rl-agents/spec.md`.
- Change folder under `openspec/changes/01-.../` is kept for provenance (marked with `ARCHIVED` sentinel after `dev/ending.sh` runs).

## Current source of truth

`openspec/specs/rl-agents/spec.md` — if the code diverges from it, the spec wins.

## Next change number

Use prefix **02-** for the next proposal.

## Suggested next actions

1. `bash dev/startup.sh` to sync + read this handover.
2. Possible `02-` ideas:
   - Hyperparameter sweep (α ∈ {0.1, 0.25, 0.5, 0.75}, ε-decay schedules).
   - Add Expected SARSA for a three-way comparison.
   - Add Double Q-learning to show overestimation bias.
3. When done, `bash dev/ending.sh` to validate tasks.md, archive specs, rewrite
   this file, and push to GitHub.

## Environment notes

- Python 3.11, numpy 2.4.2, matplotlib 3.10.8 (tested on Windows 11 / Git Bash).
- `openspec` CLI is optional — the directory tree is maintained manually here.
