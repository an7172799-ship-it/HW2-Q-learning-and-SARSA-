"""Train Q-learning vs SARSA on Cliff Walking and save comparison plots.

Reproduces Figure 6.4 (Sutton & Barto, 2nd ed.): alpha=0.5, epsilon=0.1,
500 episodes, averaged over 50 independent runs.

Outputs in the current directory:
    learning_curves.png   - reward-per-episode curves
    policies.png          - greedy policies for both methods
    stability.png         - per-run spread (std band) around the mean
    metrics.txt           - summary statistics
"""

import numpy as np
import matplotlib.pyplot as plt

from cliff_walking import CliffWalkingEnv
from agents import run_sarsa, run_qlearning, average_runs, greedy_policy

# ---------- hyperparameters (match Sutton & Barto Fig. 6.4) ----------
ALPHA = 0.5
GAMMA = 1.0          # undiscounted, as in the textbook example
EPSILON = 0.1
NUM_EPISODES = 500
NUM_RUNS = 50
SMOOTH_WINDOW = 10   # moving-average window for the reward curves


def moving_average(x, w):
    if w <= 1:
        return x
    kernel = np.ones(w) / w
    pad = np.full(w - 1, x[:w].mean())
    return np.concatenate([pad, np.convolve(x, kernel, mode="valid")])


def env_factory():
    return CliffWalkingEnv()


def main():
    print(f"Training: {NUM_RUNS} runs x {NUM_EPISODES} episodes "
          f"(alpha={ALPHA}, gamma={GAMMA}, epsilon={EPSILON})")

    sarsa_all = average_runs(run_sarsa, env_factory, NUM_RUNS, NUM_EPISODES,
                             ALPHA, GAMMA, EPSILON, base_seed=1000)
    qlearn_all = average_runs(run_qlearning, env_factory, NUM_RUNS, NUM_EPISODES,
                              ALPHA, GAMMA, EPSILON, base_seed=2000)

    sarsa_mean = sarsa_all.mean(axis=0)
    qlearn_mean = qlearn_all.mean(axis=0)

    # -------- learning curves --------
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.plot(moving_average(sarsa_mean, SMOOTH_WINDOW),
            color="#17becf", lw=2, label="Sarsa")
    ax.plot(moving_average(qlearn_mean, SMOOTH_WINDOW),
            color="#d62728", lw=2, label="Q-learning")
    ax.set_ylim(-100, 0)
    ax.set_xlabel("Episodes")
    ax.set_ylabel("Sum of rewards per episode")
    ax.set_title(f"Sarsa vs. Q-learning on Cliff Walking\n"
                 f"alpha={ALPHA}, epsilon={EPSILON} (averaged over {NUM_RUNS} runs)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig("learning_curves.png", dpi=130)
    plt.close(fig)

    # -------- stability (std band) --------
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ep = np.arange(NUM_EPISODES)
    for data, color, name in [(sarsa_all, "#17becf", "Sarsa"),
                              (qlearn_all, "#d62728", "Q-learning")]:
        mean = data.mean(axis=0)
        std = data.std(axis=0)
        ax.plot(ep, moving_average(mean, SMOOTH_WINDOW), color=color, lw=2, label=name)
        ax.fill_between(ep,
                        moving_average(mean - std, SMOOTH_WINDOW),
                        moving_average(mean + std, SMOOTH_WINDOW),
                        color=color, alpha=0.15)
    ax.set_ylim(-150, 0)
    ax.set_xlabel("Episodes")
    ax.set_ylabel("Sum of rewards per episode")
    ax.set_title("Stability: mean +/- 1 std across runs")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig("stability.png", dpi=130)
    plt.close(fig)

    # -------- final greedy policies (trained once, long, no exploration noise in display) --------
    env = CliffWalkingEnv()
    Q_sarsa, _ = run_sarsa(env, NUM_EPISODES, ALPHA, GAMMA, EPSILON, seed=42)
    env = CliffWalkingEnv()
    Q_q, _ = run_qlearning(env, NUM_EPISODES, ALPHA, GAMMA, EPSILON, seed=42)
    plot_policies(Q_q, Q_sarsa, "policies.png")

    # -------- summary metrics --------
    last = slice(-100, None)  # last 100 episodes
    with open("metrics.txt", "w", encoding="utf-8") as f:
        f.write(f"Parameters: alpha={ALPHA}, gamma={GAMMA}, epsilon={EPSILON}, "
                f"episodes={NUM_EPISODES}, runs={NUM_RUNS}\n\n")
        f.write("Average reward over LAST 100 episodes (higher = better):\n")
        f.write(f"  Sarsa      : mean={sarsa_all[:, last].mean():+7.2f} "
                f"std={sarsa_all[:, last].mean(axis=1).std():.2f} (across runs)\n")
        f.write(f"  Q-learning : mean={qlearn_all[:, last].mean():+7.2f} "
                f"std={qlearn_all[:, last].mean(axis=1).std():.2f} (across runs)\n\n")
        f.write("Average reward over ALL episodes:\n")
        f.write(f"  Sarsa      : mean={sarsa_all.mean():+7.2f}\n")
        f.write(f"  Q-learning : mean={qlearn_all.mean():+7.2f}\n\n")
        f.write("Per-episode standard deviation across runs "
                "(mean over all episodes, smaller = more stable):\n")
        f.write(f"  Sarsa      : {sarsa_all.std(axis=0).mean():.2f}\n")
        f.write(f"  Q-learning : {qlearn_all.std(axis=0).mean():.2f}\n\n")
        f.write("Greedy path length from Start (s=36) under final Q:\n")
        f.write(f"  Sarsa path length      : {trace_greedy_len(Q_sarsa)}\n")
        f.write(f"  Q-learning path length : {trace_greedy_len(Q_q)}\n")

    with open("metrics.txt", "r", encoding="utf-8") as f:
        print(f.read())

    print("Saved: learning_curves.png, stability.png, policies.png, metrics.txt")


# ---------- policy visualization ----------
ARROWS = ["^", ">", "v", "<"]  # up, right, down, left


def plot_policies(Q_q, Q_sarsa, path):
    fig, axes = plt.subplots(2, 1, figsize=(10, 5.5))
    for ax, Q, title in zip(axes, [Q_q, Q_sarsa],
                            ["Q-learning policy", "SARSA policy"]):
        draw_gridworld_policy(ax, Q)
        ax.set_title(title, fontsize=13)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def draw_gridworld_policy(ax, Q):
    rows, cols = CliffWalkingEnv.ROWS, CliffWalkingEnv.COLS
    pi = greedy_policy(Q)

    # grid
    for r in range(rows + 1):
        ax.axhline(r, color="black", lw=1)
    for c in range(cols + 1):
        ax.axvline(c, color="black", lw=1)

    # cliff tiles
    for c in range(1, 11):
        ax.add_patch(plt.Rectangle((c, 0), 1, 1, color="#b3d9ff"))
    # start / goal
    ax.text(0.5, 0.5, "S", ha="center", va="center",
            fontsize=11, fontweight="bold")
    ax.text(11.5, 0.5, "G", ha="center", va="center",
            fontsize=11, fontweight="bold")
    ax.text(5.5, 0.5, "Cliff", ha="center", va="center", fontsize=11)

    # arrows on non-terminal, non-cliff cells
    for s in range(rows * cols):
        r, c = CliffWalkingEnv.to_rc(s)
        if (r, c) == CliffWalkingEnv.GOAL:
            continue
        if r == 3 and 1 <= c <= 10:
            continue
        # note: axis y is flipped so row 0 is top -> plot at y = rows-1-r
        y = rows - 1 - r
        ax.text(c + 0.5, y + 0.5, ARROWS[pi[s]],
                ha="center", va="center", fontsize=14)

    # draw greedy path from Start
    path = trace_greedy_path(Q)
    xs = [c + 0.5 for (_, c) in path]
    ys = [rows - 1 - r + 0.5 for (r, _) in path]
    ax.plot(xs, ys, color="#1f77b4", lw=2.5, linestyle="--", alpha=0.8)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")


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


def trace_greedy_len(Q):
    return len(trace_greedy_path(Q)) - 1


if __name__ == "__main__":
    main()
