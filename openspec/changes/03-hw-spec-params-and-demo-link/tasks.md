# Tasks — 03-hw-spec-params-and-demo-link

- [x] 1. Driver
  - [x] 1.1 Extract the "run one config → save plots + metrics" body of `main.py` into a function.
  - [x] 1.2 Invoke the function twice: Sutton config (α=0.5, γ=1.0) and HW config (α=0.1, γ=0.9).
  - [x] 1.3 Use filename suffixes `_sutton` / `_hw` so outputs don't collide.
  - [x] 1.4 Write a single `metrics.txt` that contains both configs side-by-side.
- [x] 2. README
  - [x] 2.1 Replace deploy-instruction block with a badge/button linking to https://9hhvhevrdrgp4aaxd5rakm.streamlit.app/.
  - [x] 2.2 Update existing image references from `learning_curves.png` / `policies.png` / `stability.png` to the `_sutton` variants (primary experiment).
  - [x] 2.3 Add a new section "HW-spec parameters (α=0.1, γ=0.9)" showing the `_hw` plots and commentary.
- [x] 3. Regenerate outputs
  - [x] 3.1 Run `python main.py` and commit the new PNGs + metrics.txt.
- [x] 4. Spec
  - [x] 4.1 Update `openspec/specs/rl-agents/spec.md` to reflect that the driver
    emits two configs.
