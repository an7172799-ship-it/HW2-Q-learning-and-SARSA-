"""Train Q-learning vs SARSA on Cliff Walking under two parameter configs.

Config A ("sutton"): alpha=0.5, gamma=1.0, epsilon=0.1  -> matches Sutton & Barto Fig. 6.4.
Config B ("hw"    ): alpha=0.1, gamma=0.9, epsilon=0.1  -> matches the course HW spec.

Both configs run 500 episodes x 50 independent runs and emit:
    learning_curves_<suffix>.png
    stability_<suffix>.png
    policies_<suffix>.png
and a single combined `metrics.txt`.
"""

from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt

from cliff_walking import CliffWalkingEnv
from agents import run_sarsa, run_qlearning, average_runs, greedy_policy

NUM_EPISODES = 500
NUM_RUNS = 50
SMOOTH_WINDOW = 10


@dataclass
class Config:
    suffix: str
    label: str
    alpha: float
    gamma: float
    epsilon: float


CONFIGS = [
    Config("sutton", "Sutton & Barto Fig. 6.4", alpha=0.5, gamma=1.0, epsilon=0.1),
    Config("hw",     "HW spec",                 alpha=0.1, gamma=0.9, epsilon=0.1),
]


def moving_average(x, w):
    w = max(1, min(int(w), len(x)))
    if w <= 1:
        return x
    kernel = np.ones(w) / w
    pad = np.full(w - 1, x[:w].mean())
    return np.concatenate([pad, np.convolve(x, kernel, mode="valid")])


def env_factory():
    return CliffWalkingEnv()


def run_config(cfg: Config):
    print(f"\n[{cfg.suffix}] {cfg.label}: alpha={cfg.alpha}, gamma={cfg.gamma}, "
          f"epsilon={cfg.epsilon}, {NUM_RUNS} runs x {NUM_EPISODES} episodes")

    sarsa_all = average_runs(run_sarsa, env_factory, NUM_RUNS, NUM_EPISODES,
                             cfg.alpha, cfg.gamma, cfg.epsilon, base_seed=1000)
    qlearn_all = average_runs(run_qlearning, env_factory, NUM_RUNS, NUM_EPISODES,
                              cfg.alpha, cfg.gamma, cfg.epsilon, base_seed=2000)

    # learning curves
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.plot(moving_average(sarsa_all.mean(axis=0), SMOOTH_WINDOW),
            color="#17becf", lw=2, label="Sarsa")
    ax.plot(moving_average(qlearn_all.mean(axis=0), SMOOTH_WINDOW),
            color="#d62728", lw=2, label="Q-learning")
    ax.set_ylim(-100, 0)
    ax.set_xlabel("Episodes")
    ax.set_ylabel("Sum of rewards per episode")
    ax.set_title(f"Sarsa vs. Q-learning — {cfg.label}\n"
                 f"alpha={cfg.alpha}, gamma={cfg.gamma}, epsilon={cfg.epsilon} "
                 f"(averaged over {NUM_RUNS} runs)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(f"learning_curves_{cfg.suffix}.png", dpi=130)
    plt.close(fig)

    # stability
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
    ax.set_title(f"Stability — {cfg.label}: mean +/- 1 std across runs")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(f"stability_{cfg.suffix}.png", dpi=130)
    plt.close(fig)

    # policies
    env = CliffWalkingEnv()
    Q_sarsa, _ = run_sarsa(env, NUM_EPISODES, cfg.alpha, cfg.gamma, cfg.epsilon, seed=42)
    env = CliffWalkingEnv()
    Q_q, _ = run_qlearning(env, NUM_EPISODES, cfg.alpha, cfg.gamma, cfg.epsilon, seed=42)
    plot_policies(Q_q, Q_sarsa, f"policies_{cfg.suffix}.png", cfg.label)

    return {
        "cfg": cfg,
        "sarsa_all": sarsa_all,
        "qlearn_all": qlearn_all,
        "Q_sarsa": Q_sarsa,
        "Q_q": Q_q,
    }


def write_metrics(results):
    last = slice(-100, None)
    with open("metrics.txt", "w", encoding="utf-8") as f:
        for r in results:
            cfg = r["cfg"]
            f.write(f"============================================================\n")
            f.write(f"[{cfg.suffix}] {cfg.label}\n")
            f.write(f"Parameters: alpha={cfg.alpha}, gamma={cfg.gamma}, "
                    f"epsilon={cfg.epsilon}, episodes={NUM_EPISODES}, runs={NUM_RUNS}\n")
            f.write(f"============================================================\n")
            sarsa_all = r["sarsa_all"]
            qlearn_all = r["qlearn_all"]
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
            f.write("Greedy path length from Start under final Q:\n")
            f.write(f"  Sarsa path length      : {trace_greedy_len(r['Q_sarsa'])}\n")
            f.write(f"  Q-learning path length : {trace_greedy_len(r['Q_q'])}\n\n")
    with open("metrics.txt", "r", encoding="utf-8") as f:
        print(f.read())


def main():
    results = [run_config(cfg) for cfg in CONFIGS]
    write_metrics(results)
    print("Saved: learning_curves_{sutton,hw}.png, stability_{sutton,hw}.png, "
          "policies_{sutton,hw}.png, metrics.txt")


# ---------- policy visualization ----------
ARROWS = ["^", ">", "v", "<"]  # up, right, down, left


def plot_policies(Q_q, Q_sarsa, path, label):
    fig, axes = plt.subplots(2, 1, figsize=(10, 5.8))
    for ax, Q, title in zip(axes, [Q_q, Q_sarsa],
                            ["Q-learning policy", "SARSA policy"]):
        draw_gridworld_policy(ax, Q)
        ax.set_title(title, fontsize=13)
    fig.suptitle(label, fontsize=11, y=1.00)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def draw_gridworld_policy(ax, Q):
    rows, cols = CliffWalkingEnv.ROWS, CliffWalkingEnv.COLS
    pi = greedy_policy(Q)

    for r in range(rows + 1):
        ax.axhline(r, color="black", lw=1)
    for c in range(cols + 1):
        ax.axvline(c, color="black", lw=1)

    for c in range(1, 11):
        ax.add_patch(plt.Rectangle((c, 0), 1, 1, color="#b3d9ff"))
    ax.text(0.5, 0.5, "S", ha="center", va="center",
            fontsize=11, fontweight="bold")
    ax.text(11.5, 0.5, "G", ha="center", va="center",
            fontsize=11, fontweight="bold")
    ax.text(5.5, 0.5, "Cliff", ha="center", va="center", fontsize=11)

    for s in range(rows * cols):
        r, c = CliffWalkingEnv.to_rc(s)
        if (r, c) == CliffWalkingEnv.GOAL:
            continue
        if r == 3 and 1 <= c <= 10:
            continue
        y = rows - 1 - r
        ax.text(c + 0.5, y + 0.5, ARROWS[pi[s]],
                ha="center", va="center", fontsize=14)

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
