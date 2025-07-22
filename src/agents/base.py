"""
Base agent definitions for the Wealth Machine project.

This module defines an asynchronous base class for agents that perform
periodic tasks such as data collection, processing, or compliance checks.
Agents can be specialized by overriding the `run` coroutine.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional

from pydantic import BaseModel

# Import KnowledgeGraph and BaseConfig lazily to avoid circular imports
try:
    from ..core.knowledge_graph import KnowledgeGraph
except ImportError:
    KnowledgeGraph = Any  # type: ignore
try:
    from ..core.config import BaseConfig
except ImportError:
    BaseConfig = Any  # type: ignore

class AgentContext(BaseModel):
    """Context passed to agents containing shared resources."""
    knowledge_graph: Optional[KnowledgeGraph] = None
    config: Optional[BaseConfig] = None
    logger: logging.Logger = logging.getLogger("Agent")

class BaseAgent:
    """Abstract base class for asynchronous agents."""

    def __init__(self, context: AgentContext) -> None:
        self.context = context
        self.logger = context.logger

    async def setup(self) -> None:
        """Optional setup method to initialize resources before the agent runs."""
        pass

    async def run(self, *args: Any, **kwargs: Any) -> None:
        """The main coroutine executed by the agent. Must be overridden."""
        raise NotImplementedError("run must be implemented by subclasses")

    async def teardown(self) -> None:
        """Optional teardown method called when the agent is stopping."""
        pass

    async def start(self) -> None:
        """Start the agent's execution loop, handling errors and scheduling intervals."""
        if self.context.config and hasattr(self.context.config, "interval"):
            interval = getattr(self.context.config, "interval")
        else:
            interval = 60  # default interval in seconds
        await self.setup()
        self.logger.info("Starting agent %s with interval %s seconds", self.__class__.__name__, interval)
        try:
            while True:
                try:
                    await self.run()
                except Exception as exc:
                    self.logger.error("Error in agent %s: %s", self.__class__.__name__, exc, exc_info=True)
                await asyncio.sleep(interval)
        finally:
            await self.teardown()
