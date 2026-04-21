# Handover — DRL HW2 (post change 02)

## Repo state

- Branch: `main`
- Published to: <https://github.com/an7172799-ship-it/HW2-Q-learning-and-SARSA->
- Live demo: Streamlit Community Cloud (see README "Live demo" section)

## What is done

Change `01-add-cliff-walking-rl-agents` — **archived**
- Environment, Q-learning, SARSA, training driver, plots, report.
- Capability spec: `openspec/specs/rl-agents/spec.md`.

Change `02-add-streamlit-live-demo` — **archived**
- `streamlit_app.py` (interactive controls, progress bar, live plots).
- `requirements.txt` for Streamlit Cloud.
- README updated with Live demo section + deploy instructions.
- Capability spec: `openspec/specs/interactive-demo/spec.md`.

## Current source of truth

- `openspec/specs/rl-agents/spec.md` — environment + algorithms
- `openspec/specs/interactive-demo/spec.md` — live demo contract

If code diverges from either spec, the spec wins.

## Next change number

Use prefix **03-** for the next proposal.

## Suggested next actions

1. `bash dev/startup.sh` to sync + read this handover.
2. Verify Streamlit Cloud deployment: open the app URL, train once, confirm
   plots render.
3. Possible `03-` ideas:
   - Add Expected SARSA / Double Q-learning for a 3-way comparison.
   - ε-decay schedule option in both `main.py` and the Streamlit app.
   - Cache the training results keyed on (seed, α, γ, ε, episodes, runs) so the
     same demo-click returns instantly a second time.
4. When done, `bash dev/ending.sh` to archive and push.

## Environment notes

- Python 3.11; numpy 2.4.2; matplotlib 3.10.8; streamlit ≥ 1.37.
- Streamlit Cloud auto-deploys on push to `main`.
- `openspec` CLI is optional — directory maintained manually.
