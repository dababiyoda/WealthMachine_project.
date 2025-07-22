            """
Celery application for orchestrating background tasks in the Wealth Machine project.

This module defines Celery tasks that wrap the asynchronous agents, allowing
scheduled or event-driven execution via a Redis broker.
"""
from __future__ import annotations

import os
import asyncio
from celery import Celery

# Import agents and context
from .agents.market_intelligence import MarketIntelligenceAgent
from .agents.data_processing import DataProcessingAgent
from .agents.compliance import ComplianceAgent
from .agents.base import AgentContext
from .core.knowledge_graph import KnowledgeGraph, KnowledgeGraphConfig
from .agents.financial import FinancialAgent, FinancialAgentConfig

from .agents.growth import GrowthAgent, GrowthAgentConfig
from .agents.meta_agent import MetaAgent, MetaAgentConfig  # noqa: F401


# Instantiate Celery with broker and backend from environment variables
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)
celery_app = Celery("wealth_machine", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


def _get_default_context() -> AgentContext:
    """Create a default AgentContext using environment variables for the knowledge graph."""
    kg_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    kg_user = os.getenv("NEO4J_USER", "neo4j")
    kg_password = os.getenv("NEO4J_PASSWORD", "password")
    kg_config = KnowledgeGraphConfig(uri=kg_uri, user=kg_user, password=kg_password)
    kg = KnowledgeGraph(kg_config)
    return AgentContext(knowledge_graph=kg)


@celery_app.task(name="agents.run_market_intelligence")
def run_market_intelligence_agent() -> None:
    """Celery task to run the market intelligence agent once."""
    context = _get_default_context()
    agent = MarketIntelligenceAgent(context)
    asyncio.run(agent.run())


@celery_app.task(name="agents.run_data_processing")
def run_data_processing_agent() -> None:
    """Celery task to run the data processing agent once."""
    context = _get_default_context()
    agent = DataProcessingAgent(context)
    asyncio.run(agent.run())


@celery_app.task(name="agents.run_compliance")
def run_compliance_agent() -> None:
    """Celery task to run the compliance agent once."""
    context = _get_default_context()
    agent = ComplianceAgent(context)
    asyncio.run(agent.run())
@celery_app.task(name="agents.run_financial")
def run_financial_agent() -> None:
    """Celery task to run the financial agent once."""
    context = _get_default_context()
    agent = FinancialAgent(context)
    asyncio.run(agent.run())

@celery_app.task(name="agents.run_growth")
def run_growth_agent() -> None:
    """Celery task to run the growth agent once."""
    context = _get_default_context()
    agent = GrowthAgent(context)
    asyncio.run(agent.run())

            
@celery_app.task(name="agents.run_meta")
def run_meta_agent() -> None:
    """Celery task to run the meta agent once."""
    context = _get_default_context()
    agent = MetaAgent(context)
    asyncio.run(agent.run())



@celery_app.task(name="agents.run_all")
def run_all_agents() -> None:
    """Run all agents sequentially. Useful for periodic scheduling."""
    run_market_intelligence_agent.delay()
    run_data_processing_agent.delay()
    run_financial_agent.delay()
    run_growth_agent.delay()
    run_compliance_agent.delay()
    run_meta_agent.delay()


