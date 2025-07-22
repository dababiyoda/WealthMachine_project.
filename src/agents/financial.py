"""
FinancialAgent evaluates financial viability of opportunities within the wealth machine.

This agent uses simple ROI calculations and configurable thresholds to categorize
opportunities as viable or non‑viable. In a full implementation this would
pull data from the knowledge graph and external financial sources.
"""

from __future__ import annotations

import logging
from typing import Optional

from pydantic import BaseModel, Field

from .base import BaseAgent, AgentContext


class FinancialAgentConfig(BaseModel):
    """Configuration for FinancialAgent."""

    target_roi: float = Field(
        0.2,
        description="Desired minimum return on investment (e.g. 0.2 for 20%).",
    )
    max_investment: float = Field(
        1_000_000.0,
        description="Maximum capital the agent is allowed to allocate to a single opportunity.",
    )


class FinancialAgent(BaseAgent):
    """
    Agent responsible for assessing the financial viability of opportunities.

    The FinancialAgent inspects opportunity nodes, estimates ROI based on
    projected revenue and cost (if available), and applies labels to mark
    opportunities as viable or non‑viable according to the configured
    thresholds.
    """

    def __init__(self, context: AgentContext, config: Optional[FinancialAgentConfig] = None) -> None:
        super().__init__(context)
        self.config = config or FinancialAgentConfig()
        self.logger = logging.getLogger(self.__class__.__name__)

    async def run(self) -> None:
        """Execute financial assessment across all opportunities in the graph."""
        # Placeholder: retrieve opportunity entities from the knowledge graph
        try:
            opportunities = await self.context.graph.get_entities("Opportunity")  # type: ignore[attr-defined]
        except Exception:
            opportunities = []  # fallback if method not implemented

        for opp in opportunities:
            roi = self._estimate_roi(opp)
            opp_id = opp.get("id") or opp.get("uid") or "unknown"
            self.logger.info(f"Opportunity {opp_id}: estimated ROI={roi:.2f}")
            if roi >= self.config.target_roi:
                label = "ViableOpportunity"
            else:
                label = "NonViableOpportunity"
            # Update the knowledge graph with the viability classification if method exists
            if hasattr(self.context.graph, "update_entity_label"):
                await self.context.graph.update_entity_label(opp_id, label)  # type: ignore[attr-defined]

    def _estimate_roi(self, opportunity: dict) -> float:
        """Estimate return on investment for an opportunity dict."""
        revenue = float(opportunity.get("projected_revenue", 0.0))
        cost = float(opportunity.get("projected_cost", 1.0))
        if cost == 0:
            return 0.0
        return (revenue - cost) / cost
