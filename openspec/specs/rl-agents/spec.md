# Capability: rl-agents — current specification

Sourced from change `01-add-cliff-walking-rl-agents` (archived on first
implementation).

## Requirement: Cliff Walking environment

The system SHALL provide a `CliffWalkingEnv` class implementing the 4×12 grid
world with start (3,0), goal (3,11), and cliff cells (3,1..10).

### Scenario: step into cliff

- **GIVEN** the agent is adjacent to the cliff
- **WHEN** the chosen action moves it into a cliff cell
- **THEN** the environment returns reward −100 and teleports the agent back to
  the start state without terminating the episode.

### Scenario: step to goal

- **GIVEN** the agent is adjacent to the goal
- **WHEN** the chosen action moves it onto the goal cell
- **THEN** the environment returns reward −1 and sets `done = True`.

### Scenario: normal step

- **GIVEN** the agent is at a non-terminal, non-cliff cell
- **WHEN** it takes any legal action that does not enter the cliff or goal
- **THEN** it receives reward −1 and moves one cell in the action direction,
  clamped at grid boundaries.

## Requirement: Q-learning agent (off-policy)

The system SHALL implement Q-learning that updates using the maximum next-state
action-value regardless of the action actually taken.

### Scenario: Q-learning update

- **GIVEN** transition (s, a, r, s')
- **WHEN** the agent updates Q
- **THEN** Q(s,a) ← Q(s,a) + α[r + γ·max_a' Q(s',a') − Q(s,a)], and the `max` is
  replaced by 0 when the episode terminates at s'.

## Requirement: SARSA agent (on-policy)

The system SHALL implement SARSA that updates using the action actually chosen
at the next state under the current ε-greedy policy.

### Scenario: SARSA update

- **GIVEN** transition (s, a, r, s', a') where a' is sampled from ε-greedy on Q
- **WHEN** the agent updates Q
- **THEN** Q(s,a) ← Q(s,a) + α[r + γ·Q(s',a') − Q(s,a)], and Q(s',a') is
  replaced by 0 when the episode terminates at s'.

## Requirement: Training driver

The system SHALL provide `main.py` that trains both algorithms under identical
hyperparameters and emits plots and metrics.

### Scenario: reproducible comparison

- **GIVEN** fixed seeds and hyperparameters α=0.5, γ=1.0, ε=0.1
- **WHEN** `python main.py` is run
- **THEN** it produces `learning_curves.png`, `stability.png`, `policies.png`,
  and `metrics.txt`, averaged over 50 runs of 500 episodes each.

## Requirement: Policy divergence

Under ε=0.1 the learned greedy policies SHALL differ in the expected qualitative
way: Q-learning hugs the cliff edge; SARSA takes a safer path.

### Scenario: path lengths

- **GIVEN** Q-functions produced at the end of training
- **WHEN** the greedy path from Start is traced
- **THEN** Q-learning's path length is 13 and SARSA's path length is ≥ 15.
