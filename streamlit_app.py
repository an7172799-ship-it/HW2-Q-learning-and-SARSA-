"""Streamlit live demo: Q-learning vs. SARSA on Cliff Walking.

Launch locally:   streamlit run streamlit_app.py
Deploy:           https://share.streamlit.io  (point at this repo)
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from cliff_walking import CliffWalkingEnv
from agents import run_sarsa, run_qlearning, greedy_policy


# ---------- page config ----------
st.set_page_config(
    page_title="Cliff Walking: Q-learning vs. SARSA",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.title("Q-learning vs. SARSA on Cliff Walking")
st.caption(
    "Interactive reproduction of Sutton & Barto, Example 6.6 / Figure 6.4. "
    "Tune the hyperparameters in the sidebar, click **Train**, and watch "
    "the two algorithms diverge."
)

# ---------- sidebar controls ----------
with st.sidebar:
    st.header("Hyperparameters")
    alpha = st.slider("α (learning rate)", 0.05, 1.0, 0.5, 0.05)
    epsilon = st.slider("ε (exploration)", 0.0, 0.5, 0.1, 0.01)
    gamma = st.slider("γ (discount)", 0.5, 1.0, 1.0, 0.05)
    episodes = st.slider("Episodes", 50, 1000, 500, 50)
    runs = st.slider("Runs (averaged)", 1, 20, 5)
    seed = st.number_input("Seed", min_value=0, max_value=99_999, value=42, step=1)

    st.header("Algorithms")
    show_sarsa = st.checkbox("SARSA", value=True)
    show_q = st.checkbox("Q-learning", value=True)
    smooth = st.slider("Smoothing window", 1, 50, 10)

    go = st.button("Train", type="primary", use_container_width=True)
    st.caption("Tip: increase *Runs* for smoother curves, fewer runs for a faster demo.")


# ---------- helpers ----------
def moving_average(x, w):
    if w <= 1:
        return x
    kernel = np.ones(w) / w
    pad = np.full(w - 1, x[:w].mean())
    return np.concatenate([pad, np.convolve(x, kernel, mode="valid")])


def train_many(algo, n_runs, n_ep, a, g, e, base_seed, progress_cb):
    all_returns = np.zeros((n_runs, n_ep))
    last_Q = None
    for i in range(n_runs):
        env = CliffWalkingEnv()
        Q, returns = algo(env, n_ep, a, g, e, seed=base_seed + i)
        all_returns[i] = returns
        last_Q = Q
        progress_cb(i + 1, n_runs)
    return all_returns, last_Q


def trace_greedy_path(Q, max_steps=200):
    env = CliffWalkingEnv()
    s = env.reset()
    path = [env.state]
    for _ in range(max_steps):
        a = int(Q[s].argmax())
        s, _, done = env.step(a)
        path.append(env.state)
        if done:
            break
    return path


ARROWS = ["^", ">", "v", "<"]


def draw_policy(ax, Q, title):
    rows, cols = CliffWalkingEnv.ROWS, CliffWalkingEnv.COLS
    pi = greedy_policy(Q)

    for r in range(rows + 1):
        ax.axhline(r, color="black", lw=0.8)
    for c in range(cols + 1):
        ax.axvline(c, color="black", lw=0.8)
    for c in range(1, 11):
        ax.add_patch(plt.Rectangle((c, 0), 1, 1, color="#b3d9ff"))
    ax.text(0.5, 0.5, "S", ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(11.5, 0.5, "G", ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(5.5, 0.5, "Cliff", ha="center", va="center", fontsize=10)

    for s in range(rows * cols):
        r, c = CliffWalkingEnv.to_rc(s)
        if (r, c) == CliffWalkingEnv.GOAL:
            continue
        if r == 3 and 1 <= c <= 10:
            continue
        y = rows - 1 - r
        ax.text(c + 0.5, y + 0.5, ARROWS[pi[s]], ha="center", va="center", fontsize=12)

    path = trace_greedy_path(Q)
    xs = [c + 0.5 for (_, c) in path]
    ys = [rows - 1 - r + 0.5 for (r, _) in path]
    ax.plot(xs, ys, color="#1f77b4", lw=2.0, linestyle="--", alpha=0.8)

    ax.set_xlim(0, cols); ax.set_ylim(0, rows)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_title(title)


# ---------- main area ----------
if not go:
    st.info(
        "Adjust the sliders in the sidebar and click **Train** to run the "
        "comparison live. The default settings reproduce the textbook figure."
    )
    st.markdown(
        "**What to expect** — under ε > 0, Q-learning learns the *optimal* "
        "but risky path that hugs the cliff edge, while SARSA learns a *safer* "
        "path along the top row. SARSA's online reward is therefore higher."
    )
    st.stop()

if not (show_sarsa or show_q):
    st.error("Select at least one algorithm in the sidebar.")
    st.stop()

progress = st.progress(0.0, text="Starting training…")

active = [n for n, flag in [("SARSA", show_sarsa), ("Q-learning", show_q)] if flag]
slot = 1 / len(active)

results = {}
offset = 0.0
for name in active:
    algo_fn = run_sarsa if name == "SARSA" else run_qlearning
    def cb(done, total_this_algo, _off=offset, _name=name):
        frac = _off + slot * (done / total_this_algo)
        progress.progress(min(1.0, frac), text=f"{_name}: run {done}/{total_this_algo}")
    base = int(seed) + (0 if name == "SARSA" else 50_000)
    all_returns, Q = train_many(algo_fn, runs, episodes, alpha, gamma, epsilon, base, cb)
    results[name] = {"returns": all_returns, "Q": Q}
    offset += slot

progress.progress(1.0, text="Done.")
progress.empty()

# ---------- plots ----------
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Learning curves")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    colors = {"SARSA": "#17becf", "Q-learning": "#d62728"}
    for name, data in results.items():
        mean = data["returns"].mean(axis=0)
        ax.plot(moving_average(mean, smooth), color=colors[name], lw=2, label=name)
    ax.set_ylim(-100, 0)
    ax.set_xlabel("Episodes")
    ax.set_ylabel("Sum of rewards per episode")
    ax.set_title(f"α={alpha}, γ={gamma}, ε={epsilon}  ({runs} runs averaged)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

with col2:
    st.subheader("Summary")
    rows = []
    for name, data in results.items():
        last100 = data["returns"][:, -min(100, episodes):].mean()
        path_len = len(trace_greedy_path(data["Q"])) - 1
        rows.append({"Algorithm": name,
                     "Last-100 mean reward": f"{last100:+.2f}",
                     "Greedy path length": path_len})
    st.table(rows)
    st.caption(
        "**Higher** last-100 mean = better online performance. "
        "**Shorter** greedy path ⇒ more optimal under greedy execution "
        "(but risky in the presence of exploration)."
    )

st.subheader("Final greedy policies")
n_policies = len(results)
fig, axes = plt.subplots(n_policies, 1, figsize=(10, 1.8 * n_policies + 0.4))
if n_policies == 1:
    axes = [axes]
for ax, (name, data) in zip(axes, results.items()):
    draw_policy(ax, data["Q"], f"{name} policy")
fig.tight_layout()
st.pyplot(fig, clear_figure=True)

with st.expander("How this maps to theory"):
    st.markdown(
        """
        - **Q-learning (off-policy)** updates toward `max_a' Q(s', a')`. It
          learns the greedy-policy value, ignoring the exploration that actually
          happens — so it converges to the optimal path along the cliff edge,
          even though that path is catastrophic when ε > 0.
        - **SARSA (on-policy)** updates toward `Q(s', a')` where `a'` is the
          action actually chosen under ε-greedy. The risk of random cliff falls
          is therefore baked into its value estimates, pushing the policy away
          from the cliff.
        """
    )
