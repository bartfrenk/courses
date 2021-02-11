from __future__ import annotations
from copy import deepcopy
from decimal import Decimal
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *  # pylint: disable=wildcard-import, unused-wildcard-import
import random

X = TypeVar("X")
S = TypeVar("S")
A = TypeVar("A")
R = TypeVar("R", float, Decimal)


class Dist(Generic[X]):
    pass


Policy = Mapping[S, Dist[A]]

Pred = Callable[[X], bool]


@dataclass
class Step(Generic[S, A, R]):
    state: S
    action: A
    reward: Optional[R]


class MDP(Generic[S, A, R], ABC):
    @abstractmethod
    def iterate(self, state: S, action: A, policy: Policy[S, A]) -> Iterator[Step[S, A, R]]:
        pass

    def episode(
        self,
        state: S,
        action: A,
        policy: Policy[S, A],
    ) -> Iterator[Step[S, A, R]]:
        steps = self.iterate(state, action, policy)
        while True:
            try:
                step = next(steps)
            except StopIteration:
                break
            yield step
            if self.terminal(step.state) is None:
                raise RuntimeError("Not an episodic MDP")
            if self.terminal(step.state) is True:
                break

    @abstractmethod
    @property
    def states(self) -> Sequence[S]:
        pass

    @abstractmethod
    def actions(self, state: S) -> Sequence[A]:
        pass

    def terminal(self, state: S) -> Optional[bool]:
        return None


def monte_carlo_es(mdp: MDP[S, A, R], initial: Policy[S, A], discount: R):
    state = random.choice(mdp.states)
    action = random.choice(mdp.actions(state))
    returns: Dict[Tuple[S, A], List[R]]
    policy = deepcopy(dict(initial))

    cumulative_reward: int = 0
    while True:
        episode = list(mdp.episode(state, action, policy))
        for t in range(len(episode) - 1, 0):
            reward = episode[t + 1].reward
            if reward is None:
                break
            cumulative_reward = discount * cumulative_reward + reward  # type: ignore

            if not visited(episode[:t], episode[t].state, episode[t].action):
                returns.setdefault((state, action), []).append(cumulative_reward)  # type: ignore
            optimal = greedy(returns, episode[t].state)
            if optimal is None:
                raise RuntimeError("Failed to compute greedy action")
            policy[state] = deterministic(optimal)


def on_policy_first_visit_mc_control():
    pass


def greedy(returns: Dict[Tuple[S, A], List[R]], state: S) -> Optional[A]:
    pass


def deterministic(a: A) -> Dist[A]:
    pass


def visited(episode: Sequence[Step[S, A, R]], state: S, action: A) -> bool:
    pass
