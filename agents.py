"""Q-learning (off-policy) and SARSA (on-policy) tabular TD-control agents."""

import numpy as np

from cliff_walking import CliffWalkingEnv, epsilon_greedy


def run_sarsa(env, num_episodes, alpha, gamma, epsilon, seed, max_steps=10_000):
    """SARSA (on-policy TD control). Returns (Q, rewards_per_episode)."""
    rng = np.random.default_rng(seed)
    Q = np.zeros((env.N_STATES, env.N_ACTIONS))
    returns = np.zeros(num_episodes)

    for ep in range(num_episodes):
        s = env.reset()
        a = epsilon_greedy(Q, s, epsilon, env.N_ACTIONS, rng)
        G = 0.0
        for _ in range(max_steps):
            s_next, r, done = env.step(a)
            a_next = epsilon_greedy(Q, s_next, epsilon, env.N_ACTIONS, rng)
            target = r + (0.0 if done else gamma * Q[s_next, a_next])
            Q[s, a] += alpha * (target - Q[s, a])
            G += r
            s, a = s_next, a_next
            if done:
                break
        returns[ep] = G
    return Q, returns


def run_qlearning(env, num_episodes, alpha, gamma, epsilon, seed, max_steps=10_000):
    """Q-learning (off-policy TD control). Returns (Q, rewards_per_episode)."""
    rng = np.random.default_rng(seed)
    Q = np.zeros((env.N_STATES, env.N_ACTIONS))
    returns = np.zeros(num_episodes)

    for ep in range(num_episodes):
        s = env.reset()
        G = 0.0
        for _ in range(max_steps):
            a = epsilon_greedy(Q, s, epsilon, env.N_ACTIONS, rng)
            s_next, r, done = env.step(a)
            target = r + (0.0 if done else gamma * Q[s_next].max())
            Q[s, a] += alpha * (target - Q[s, a])
            G += r
            s = s_next
            if done:
                break
        returns[ep] = G
    return Q, returns


def average_runs(algo, env_factory, num_runs, num_episodes, alpha, gamma, epsilon,
                 base_seed=0):
    """Run algo `num_runs` times with different seeds, return mean reward per episode."""
    all_returns = np.zeros((num_runs, num_episodes))
    for i in range(num_runs):
        env = env_factory()
        _, returns = algo(env, num_episodes, alpha, gamma, epsilon, seed=base_seed + i)
        all_returns[i] = returns
    return all_returns


def greedy_policy(Q):
    """Return greedy action per state (ties broken by lowest index)."""
    return Q.argmax(axis=1)
