"""Cliff Walking environment (Sutton & Barto, Example 6.6).

4 x 12 grid.
    - Start: bottom-left  (row=3, col=0)
    - Goal : bottom-right (row=3, col=11)
    - Cliff: (row=3, col=1..10)  -> reward -100, agent is teleported back to Start
    - Every other transition gives reward -1.
    - Actions: 0=up, 1=right, 2=down, 3=left.
    - Episode terminates when agent reaches Goal.
"""

import numpy as np


class CliffWalkingEnv:
    ROWS = 4
    COLS = 12
    N_STATES = ROWS * COLS
    N_ACTIONS = 4

    # (dr, dc) for up, right, down, left
    _MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    START = (3, 0)
    GOAL = (3, 11)

    def __init__(self):
        self.state = self.START

    @classmethod
    def to_index(cls, rc):
        r, c = rc
        return r * cls.COLS + c

    @classmethod
    def to_rc(cls, s):
        return divmod(s, cls.COLS)

    def reset(self):
        self.state = self.START
        return self.to_index(self.state)

    def _is_cliff(self, rc):
        r, c = rc
        return r == 3 and 1 <= c <= 10

    def step(self, action):
        r, c = self.state
        dr, dc = self._MOVES[action]
        nr = min(max(r + dr, 0), self.ROWS - 1)
        nc = min(max(c + dc, 0), self.COLS - 1)
        next_rc = (nr, nc)

        if self._is_cliff(next_rc):
            reward = -100.0
            self.state = self.START
            done = False
        elif next_rc == self.GOAL:
            reward = -1.0
            self.state = next_rc
            done = True
        else:
            reward = -1.0
            self.state = next_rc
            done = False

        return self.to_index(self.state), reward, done


def epsilon_greedy(Q, s, epsilon, n_actions, rng):
    if rng.random() < epsilon:
        return rng.integers(n_actions)
    qs = Q[s]
    # random tie-break among argmax
    max_q = qs.max()
    candidates = np.flatnonzero(qs == max_q)
    return rng.choice(candidates)
