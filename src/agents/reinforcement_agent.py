"""
Reinforcement learning agent skeleton for integrating agent-based economics.
This agent implements a simple tabular Q-learning algorithm that can be used to
learn optimal policies in a discrete environment. It can be extended to more
complex scenarios or connected with a knowledge graph to inform rewards.
"""

from dataclasses import dataclass
import random
from typing import Dict, Tuple, Any, List


@dataclass
class StateActionValue:
    """Structure to keep track of Q-value and visit count for a state-action pair."""
    value: float = 0.0
    count: int = 0


class ReinforcementAgent:
    """A simple reinforcement learning agent using Q-learning.

    The agent maintains a Q-table mapping (state, action) pairs to state-action
    values. It uses an epsilon-greedy policy for action selection and updates
    the Q-values based on observed rewards and estimated future returns.
    """

    def __init__(self, actions: List[Any], alpha: float = 0.1, gamma: float = 0.95, epsilon: float = 0.1) -> None:
        """
        Initialize the reinforcement learning agent.

        :param actions: List of possible actions the agent can take.
        :param alpha: Learning rate determining how quickly the agent updates values.
        :param gamma: Discount factor for future rewards.
        :param epsilon: Exploration rate for epsilon-greedy policy.
        """
        self.q_table: Dict[Tuple[Any, Any], StateActionValue] = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state: Any) -> Any:
        """
        Choose an action for the given state using an epsilon-greedy policy.

        :param state: The current environment state.
        :return: An action from the list of possible actions.
        """
        # Explore with probability epsilon
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        # Exploit best known action
        values = [self.q_table.get((state, a), StateActionValue()).value for a in self.actions]
        max_value = max(values)
        # Break ties randomly among the best actions
        best_actions = [a for a, v in zip(self.actions, values) if v == max_value]
        return random.choice(best_actions)

    def update(self, state: Any, action: Any, reward: float, next_state: Any) -> None:
        """
        Update the Q-value for the given state-action pair based on the observed
        reward and the estimated value of the next state.

        :param state: The previous state.
        :param action: The action taken in the previous state.
        :param reward: The immediate reward received after taking the action.
        :param next_state: The state resulting from the action.
        """
        key = (state, action)
        sa_value = self.q_table.get(key, StateActionValue())
        # Estimate future return from next state
        future_returns = [self.q_table.get((next_state, a), StateActionValue()).value for a in self.actions]
        max_future = max(future_returns) if future_returns else 0.0
        target = reward + self.gamma * max_future
        # Update Q-value towards the target
        sa_value.value += self.alpha * (target - sa_value.value)
        sa_value.count += 1
        self.q_table[key] = sa_value

    def reset(self) -> None:
        """Reset the agent's learned Q-table."""
        self.q_table.clear()
