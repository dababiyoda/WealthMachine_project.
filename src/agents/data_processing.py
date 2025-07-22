"""
Data Processing agent for the Wealth Machine project.

This agent is responsible for transforming raw data collected by other agents
(e.g. market intelligence) into structured insights, performing feature
extraction, normalisation and enrichment. It writes processed data back into
our knowledge graph so that other agents can consume it.
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict

from .base import BaseAgent, AgentContext

class DataProcessingAgent(BaseAgent):
    """Agent that processes raw data and enriches it for downstream agents."""

    async def run(self, *args: Any, **kwargs: Any) -> None:
        # Retrieve raw data from the knowledge graph or other data sources.
        kg = self.context.knowledge_graph
        if not kg:
            self.logger.warning("DataProcessingAgent: No knowledge graph available")
            return
        # Example: query nodes with a property `processed=false`
        raw_nodes = await kg.execute_cypher_async(
            "MATCH (n) WHERE n.processed = false RETURN n LIMIT 10"
        ) if hasattr(kg, 'execute_cypher_async') else []
        if not raw_nodes:
            self.logger.debug("DataProcessingAgent: No unprocessed nodes found")
            return
        for record in raw_nodes:
            node = record[0]
            # Perform a simple processing operation, e.g. lowercasing text fields
            updated_properties: Dict[str, Any] = {}
            for key, value in node.items():
                if isinstance(value, str):
                    updated_properties[key] = value.strip().lower()
            updated_properties['processed'] = True
            # Update the node in the knowledge graph
            if hasattr(kg, 'update_node'):
                await kg.update_node(node.get('id'), updated_properties)  # type: ignore
            self.logger.info("DataProcessingAgent: processed node %s", node.get('id'))
        # Sleep briefly to yield control
        await asyncio.sleep(0)
