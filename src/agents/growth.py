"""
GrowthAgent plans and monitors the scaling of opportunities.

This agent analyzes metrics from the knowledge graph, such as adoption
rate and revenue growth, and suggests strategies to accelerate growth.
"""

from __future__ import annotations

import logging
from typing import Optional

from pydantic import BaseModel, Field

from .base import BaseAgent, AgentContext


class GrowthAgentConfig(BaseModel):
    """Configuration for GrowthAgent."""

    growth_rate_target: float = Field(
        0.1,
        description="Desired weekly growth rate for opportunities (e.g. 0.1 for 10%).",
    )
    monitoring_interval_days: int = Field(
        7,
        description="Frequency (in days) to evaluate growth metrics and adjust strategy.",
    )


class GrowthAgent(BaseAgent):
    """
    Agent responsible for planning and monitoring opportunity scaling.

    The GrowthAgent reviews adoption metrics and revenue trajectories to
    identify whether opportunities meet growth targets and proposes
    interventions when growth lags. In this skeleton, the logic is
    simplified to demonstrate structure.
    """

    def __init__(self, context: AgentContext, config: Optional[GrowthAgentConfig] = None) -> None:
        super().__init__(context)
        self.config = config or GrowthAgentConfig()
        self.logger = logging.getLogger(self.__class__.__name__)

    async def run(self) -> None:
        """Evaluate growth metrics and log recommendations."""
        # Placeholder: retrieve metrics for opportunities
        try:
            metrics = await self.context.graph.get_growth_metrics()  # type: ignore[attr-defined]
        except Exception:
            metrics = []  # fallback

        for metric in metrics:
            growth_rate = metric.get("growth_rate", 0.0)
            opp_id = metric.get("id", "unknown")
            if growth_rate < self.config.growth_rate_target:
                self.logger.info(
                    f"Opportunity {opp_id}: growth {growth_rate:.2%} below target. Consider marketing push."
                )
            else:
                self.logger.info(
                    f"Opportunity {opp_id}: growth {growth_rate:.2%} meets or exceeds target."
                )
