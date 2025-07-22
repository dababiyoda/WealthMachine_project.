"""
Prefect workflow for training a reinforcement learning agent.

This workflow defines tasks and flows that train the ReinforcementAgent
using a simple simulated environment. The goal is to demonstrate how
multi‑agent reinforcement learning can be orchestrated within the wealth
machine project.
"""

from __future__ import annotations

import random
from typing import List

from prefect import flow, task

from src.agents.reinforcement_agent import ReinforcementAgent


@task
def run_episode(agent: ReinforcementAgent, max_steps: int = 10) -> float:
    """
    Run a single episode in a dummy environment and update the agent.

    The environment here is highly simplified: at each step the agent
    receives a random reward between 0 and 1. The state is represented
    by a simple string and doesn't influence the reward. This function
    demonstrates the update loop of a reinforcement learning agent.

    Args:
        agent: The reinforcement learning agent.
        max_steps: Maximum number of steps per episode.

    Returns:
        Total accumulated reward for the episode.
    """
    total_reward = 0.0
    state = "start"
    for _ in range(max_steps):
        action = agent.choose_action(state)
        reward = random.random()
        next_state = "end" if random.random() > 0.8 else "start"
        agent.update(state, action, reward, next_state)
        total_reward += reward
        state = next_state
    return total_reward


@flow
def reinforcement_training_flow(episodes: int = 100, actions: List[str] | None = None) -> ReinforcementAgent:
    """
    Prefect flow to train a reinforcement learning agent over a number of episodes.

    Args:
        episodes: Number of episodes to train.
        actions: Optional list of possible actions. Defaults to ["buy", "hold", "sell"].

    Returns:
        The trained reinforcement learning agent.
    """
    if actions is None:
        actions = ["buy", "hold", "sell"]

    agent = ReinforcementAgent(actions=actions)
    for _ in range(episodes):
        run_episode(agent)
    return agent


__all__ = ["reinforcement_training_flow"]
