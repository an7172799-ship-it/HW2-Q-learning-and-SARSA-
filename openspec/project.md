# Project: DRL HW2 — Cliff Walking (Q-learning vs. SARSA)

## Purpose

Implement and compare two tabular temporal-difference control algorithms —
**Q-learning (off-policy)** and **SARSA (on-policy)** — on the classic
**Cliff Walking** environment (Sutton & Barto, 2nd ed., Example 6.6 / Fig. 6.4),
and analyse their learning curves, final greedy policies, and stability.

## Tech Stack

- Python 3.11
- NumPy 2.x (tabular Q updates)
- Matplotlib (learning curves, policy grid visualisation)

## Conventions

- Single-repo, flat Python layout (no package nesting required for this assignment).
- Reproducibility: every run accepts an integer `seed`; results averaged over 50 runs.
- Plots are committed alongside source so the report (`README.md`) renders on GitHub
  without needing to re-run training.
- OpenSpec change IDs follow the `NN-<kebab-slug>` numbering rule, starting from `01-`.

## Deliverables

- Source code (`cliff_walking.py`, `agents.py`, `main.py`)
- Plots (`learning_curves.png`, `policies.png`, `stability.png`)
- Numerical summary (`metrics.txt`)
- Report (`README.md`, in Chinese)
- OpenSpec specs (`openspec/specs/rl-agents/spec.md`)
- Handover doc (`HANDOVER.md`) for the next development iteration
