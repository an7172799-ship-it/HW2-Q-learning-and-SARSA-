# Change 02 — Add Streamlit live demo

## Why

The GitHub repo currently only shows static plots. We want a **live, interactive
demo** — a deployed web app where a visitor can adjust hyperparameters
(α, ε, γ, episodes, runs) and see Q-learning vs. SARSA train in real time, then
compare the resulting learning curves and greedy policies side-by-side.

Target host: **Streamlit Community Cloud** (free, zero-ops, auto-redeploys on git push).

## What changes

- **ADDED** capability `interactive-demo`:
  - A Streamlit app (`streamlit_app.py`) reusing the existing `CliffWalkingEnv`
    and `run_sarsa` / `run_qlearning` without duplication.
  - Sidebar controls for α, ε, γ, episodes, number of runs (averaged), seed.
  - Tabs/sections: learning curves (both algorithms), final greedy policies
    (grid of arrows, start/goal/cliff coloured), numeric summary.
  - Progress bar during training so the user sees it is live.
- **ADDED** `requirements.txt` pinning runtime deps for Streamlit Cloud.
- **MODIFIED** `README.md` to add a "Live demo" badge + deploy instructions.

## Impact

- No change to existing `cliff_walking.py` / `agents.py` / `main.py` behaviour.
- New files: `streamlit_app.py`, `requirements.txt`.
- `README.md`: section added.

## Acceptance criteria

- `streamlit run streamlit_app.py` starts the app locally without errors.
- Moving α or ε sliders and clicking "Train" re-runs training and refreshes plots.
- App finishes the default 5 runs × 500 episodes in < 30 s on a modest CPU.
- Streamlit Community Cloud can deploy directly from the repo with no extra
  config beyond `requirements.txt`.
