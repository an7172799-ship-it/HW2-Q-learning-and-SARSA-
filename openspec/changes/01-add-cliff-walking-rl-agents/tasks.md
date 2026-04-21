# Tasks — 01-add-cliff-walking-rl-agents

- [x] 1. Environment
  - [x] 1.1 Implement `CliffWalkingEnv` (4×12, start (3,0), goal (3,11), cliff (3,1..10)).
  - [x] 1.2 Transition & reward rules: −1 per step, −100 + teleport on cliff entry, terminate at goal.
  - [x] 1.3 `epsilon_greedy` helper with uniform tie-breaking.
- [x] 2. Agents
  - [x] 2.1 `run_sarsa(env, num_episodes, alpha, gamma, epsilon, seed)`.
  - [x] 2.2 `run_qlearning(env, num_episodes, alpha, gamma, epsilon, seed)`.
  - [x] 2.3 `average_runs(...)` helper to average across independent seeds.
- [x] 3. Training driver
  - [x] 3.1 `main.py` runs 50 × 500 with α=0.5, γ=1.0, ε=0.1.
  - [x] 3.2 Saves `learning_curves.png`, `stability.png`, `policies.png`, `metrics.txt`.
  - [x] 3.3 Smoothing via 10-episode moving average.
- [x] 4. Report
  - [x] 4.1 `README.md` with environment, parameters, update rules, results, discussion.
- [x] 5. Validation
  - [x] 5.1 Q-learning greedy path length = 13 (cliff edge).
  - [x] 5.2 SARSA greedy path length ≥ 15 (safe path).
  - [x] 5.3 SARSA outperforms Q-learning on last-100-episode average reward.
