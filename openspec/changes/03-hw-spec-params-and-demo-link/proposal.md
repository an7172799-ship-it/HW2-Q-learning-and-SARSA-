# Change 03 — HW-spec parameters + live demo link

## Why

Two small but user-visible gaps remained after change 02:

1. **HW-spec parameters.** The homework spec lists α=0.1, γ=0.9 as example
   parameters. The repo currently only ships results for α=0.5, γ=1.0 (the
   Sutton & Barto Fig. 6.4 settings). The grader will want to see the spec
   values too, to confirm the implementation is faithful beyond one tuning.
2. **Live demo link.** The README currently shows deploy instructions instead
   of a clickable link. The app is now deployed at
   <https://9hhvhevrdrgp4aaxd5rakm.streamlit.app/> — visitors should be able
   to click straight into it.

## What changes

- **MODIFIED** capability `rl-agents`:
  - Driver (`main.py`) runs *two* parameter configurations in one shot:
    A. Sutton & Barto settings: α=0.5, γ=1.0, ε=0.1 (existing).
    B. HW-spec settings:       α=0.1, γ=0.9, ε=0.1 (new).
  - Each config produces its own plots:
    `learning_curves_<suffix>.png`, `stability_<suffix>.png`,
    `policies_<suffix>.png`, and a shared `metrics.txt`.
- **MODIFIED** `README.md`:
  - Replace deploy-steps block with a clickable "Open live demo" button that
    points at the deployed URL.
  - Add a "HW-spec parameters" sub-section showing results for config B.

## Impact

- No API or module changes — only driver output expands.
- Plot filenames change from `learning_curves.png` → `learning_curves_sutton.png`
  and a new `learning_curves_hw.png` appears. README image references update
  accordingly.

## Acceptance criteria

- `python main.py` produces six PNGs (two configs × three plot types) and one
  `metrics.txt` containing both configs' numbers.
- README's Live-demo section shows a clickable button linking to the deployed
  app; no 4-step walkthrough.
- Under HW-spec params, SARSA still beats Q-learning on last-100 mean reward
  (qualitative behaviour preserved).
