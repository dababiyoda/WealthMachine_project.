"""
Workflow engine for orchestrating agents in the Wealth Machine project.

This module provides a simple Prefect-based workflow to coordinate the
execution of multiple agents across different phases (opportunity discovery,
data processing, compliance checking). It can be extended to use Temporal or
other workflow engines as needed.
"""
from __future__ import annotations

from typing import Any

try:
    from prefect import flow, task
except ImportError:
    # Prefect is optional. Define no-op decorators if not installed.
    def flow(func: Any = None, *, name: str | None = None):
        def decorator(f):
            return f
        return decorator if func is None else decorator(func)
    def task(func: Any = None, *, name: str | None = None):
        def decorator(f):
            return f
        return decorator if func is None else decorator(func)


@task
async def run_agent(agent: Any) -> None:
    """Run an asynchronous agent once."""
    await agent.run()

@flow(name="wealth-machine-workflow")
async def wealth_machine_flow(market_agent: Any, data_agent: Any, compliance_agent: Any) -> None:
    """Execute the agents in sequence to complete a full opportunity cycle."""
    await run_agent(market_agent)
    await run_agent(data_agent)
    await run_agent(compliance_agent)


def start_workflow(market_agent: Any, data_agent: Any, compliance_agent: Any) -> None:
    """Entry point to start the workflow. This can be scheduled periodically."""
    # If Prefect is installed, we can run the flow. Otherwise, run agents directly.
    try:
        import asyncio
        asyncio.run(wealth_machine_flow(market_agent, data_agent, compliance_agent))
    except Exception:
        # Fallback: run agents sequentially without Prefect
        import asyncio
        async def _run_all():
            await market_agent.run()
            await data_agent.run()
            await compliance_agent.run()
        asyncio.run(_run_all())
