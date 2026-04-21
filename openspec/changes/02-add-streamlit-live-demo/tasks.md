# Tasks — 02-add-streamlit-live-demo

- [x] 1. Dependencies
  - [x] 1.1 Create `requirements.txt` with streamlit, numpy, matplotlib.
- [x] 2. Streamlit app
  - [x] 2.1 Layout: title, caption, sidebar controls, main area.
  - [x] 2.2 Sidebar sliders: α, ε, γ, episodes, runs, seed, algorithm selection.
  - [x] 2.3 "Train" button triggers training; progress bar shows per-run progress.
  - [x] 2.4 Plot: learning curves (moving-average smoothed) for both algos.
  - [x] 2.5 Plot: final greedy policies side-by-side with cliff / start / goal.
  - [x] 2.6 Metrics table: last-100-ep mean reward + greedy path length.
  - [x] 2.7 Reuse `CliffWalkingEnv`, `run_sarsa`, `run_qlearning` (no duplication).
- [x] 3. Docs
  - [x] 3.1 README: "Live demo" section with Streamlit badge + deploy instructions.
- [x] 4. Spec
  - [x] 4.1 Delta spec under `specs/interactive-demo/spec.md`.
- [x] 5. Deploy steps (instructions only; deployment is done by user in browser)
  - [x] 5.1 Document the 4-click Streamlit Cloud setup in README.
