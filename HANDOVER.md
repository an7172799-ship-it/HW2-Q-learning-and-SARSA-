# Handover — DRL HW2 (post change 03)

## Repo state

- Branch: `main`
- Published to: <https://github.com/an7172799-ship-it/HW2-Q-learning-and-SARSA->
- Live demo: <https://9hhvhevrdrgp4aaxd5rakm.streamlit.app/>

## What is done

Changes `01`, `02`, `03` are all **archived**:

- `01-add-cliff-walking-rl-agents` — environment, Q-learning, SARSA, training
  driver, plots, report.
- `02-add-streamlit-live-demo` — `streamlit_app.py`, `requirements.txt`, deploy
  instructions. URL now also embedded in the README.
- `03-hw-spec-params-and-demo-link` — driver now runs **two** configs in one
  shot (Sutton α=0.5/γ=1.0 and HW-spec α=0.1/γ=0.9); README section rewritten
  to cover both; Streamlit demo URL turned into a clickable button.

## Current source of truth

- `openspec/specs/rl-agents/spec.md` — environment, algorithms, and driver contract
- `openspec/specs/interactive-demo/spec.md` — live demo contract

If code diverges from either spec, the spec wins.

## Next change number

Use prefix **04-** for the next proposal.

## Suggested next actions

1. `bash dev/startup.sh` to sync + read this handover.
2. Possible `04-` ideas:
   - Expected SARSA / Double Q-learning (3-way comparison).
   - ε-decay schedule option.
   - Cache training results keyed on (α, γ, ε, episodes, runs, seed) so repeated
     Streamlit "Train" clicks with identical settings return instantly.
3. When done, `bash dev/ending.sh` to archive and push.

## Environment notes

- Python 3.11; numpy 2.4.2; matplotlib 3.10.8; streamlit ≥ 1.37.
- Streamlit Cloud auto-deploys on push to `main`.
- `openspec` CLI is optional — directory maintained manually.
