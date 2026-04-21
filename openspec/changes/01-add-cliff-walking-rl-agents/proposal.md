# Change 01 — Add Cliff Walking RL agents (Q-learning & SARSA)

## Why

DRL HW2 requires implementing and comparing two tabular TD-control algorithms on
the Cliff Walking environment, then analysing learning curves, final policies, and
stability. No existing implementation is in this repo.

## What changes

- **ADDED** capability `rl-agents` with the following requirements:
  - A `CliffWalkingEnv` compatible with Sutton & Barto's 4×12 setup.
  - A Q-learning agent (off-policy TD control).
  - A SARSA agent (on-policy TD control).
  - A training driver that averages results across 50 runs × 500 episodes.
  - Outputs: learning-curve plot, policy visualisation, stability band, metrics text.

## Impact

- New capability: `rl-agents`.
- New files: `cliff_walking.py`, `agents.py`, `main.py`, `README.md`, plot PNGs.
- No existing code affected (first change in repo).

## Acceptance criteria

- Q-learning's greedy path from Start follows the cliff edge (length = 13).
- SARSA's greedy path avoids the cliff (length ≥ 15).
- Average reward over the last 100 episodes: SARSA > Q-learning under ε = 0.1.
- All plots reproducible from a fixed seed set.
