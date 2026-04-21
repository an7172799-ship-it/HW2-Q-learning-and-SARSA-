# Capability: interactive-demo — current specification

Sourced from change `02-add-streamlit-live-demo` (archived on first implementation).

## Requirement: Streamlit app entry point

The repository SHALL provide a top-level `streamlit_app.py` that Streamlit
Community Cloud can launch without any additional configuration beyond
`requirements.txt`.

### Scenario: local launch

- **GIVEN** dependencies from `requirements.txt` are installed
- **WHEN** the user runs `streamlit run streamlit_app.py`
- **THEN** the app opens in a browser and renders the sidebar controls and an
  empty main area prompting the user to click "Train".

## Requirement: Interactive hyperparameters

The app SHALL expose the following controls in the sidebar:

- α (learning rate) ∈ [0.05, 1.0]
- ε (exploration) ∈ [0.0, 0.5]
- γ (discount) ∈ [0.5, 1.0]
- episodes ∈ [50, 1000]
- runs ∈ [1, 20]
- seed (integer)
- algorithm selector: {SARSA, Q-learning, both}

### Scenario: adjust and train

- **GIVEN** the user moves one or more sliders
- **WHEN** they click the "Train" button
- **THEN** the app trains under the new settings, shows a progress bar, and
  refreshes the learning curves, policy plots, and metric table.

## Requirement: Live progress

The app SHALL display a progress indicator so the visitor can see training is
actually running, not frozen.

### Scenario: multi-run progress

- **GIVEN** runs > 1
- **WHEN** training is in progress
- **THEN** the progress bar advances as each run completes, and its label shows
  the current run number and episode.

## Requirement: Reuse existing implementation

The Streamlit app SHALL reuse `CliffWalkingEnv`, `run_sarsa`, `run_qlearning`
from `cliff_walking.py` / `agents.py` without duplicating their logic.

### Scenario: single source of truth

- **GIVEN** the core algorithms or environment are modified
- **WHEN** the Streamlit app is re-launched
- **THEN** the demo reflects the updated behaviour automatically.
