# Delta spec — capability `rl-agents`

## MODIFIED Requirements

### Requirement: Training driver

The system SHALL provide `main.py` that trains both algorithms under **two**
parameter configurations in one invocation and emits plots and metrics for
each:

- **Sutton & Barto** (textbook Fig. 6.4): α=0.5, γ=1.0, ε=0.1
- **HW spec** (course assignment example): α=0.1, γ=0.9, ε=0.1

Outputs for each configuration follow the filename convention
`<plot>_<suffix>.png` where `<suffix>` ∈ {`sutton`, `hw`}.

#### Scenario: reproducible two-config comparison

- **GIVEN** fixed seeds and both hyperparameter sets built into the driver
- **WHEN** `python main.py` is run
- **THEN** it produces
  `learning_curves_sutton.png`, `stability_sutton.png`, `policies_sutton.png`,
  `learning_curves_hw.png`, `stability_hw.png`, `policies_hw.png`,
  and a single `metrics.txt` comparing both configs.
