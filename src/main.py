from fastapi import FastAPI, BackgroundTasks

from .core.config import BaseConfig
from .core.knowledge_graph import KnowledgeGraph, KnowledgeGraphConfig
from .agents import MarketIntelligenceAgent, MarketIntelligenceConfig

app = FastAPI()


@app.on_event("startup")
def startup_event() -> None:
    # Load configuration files
    graph_conf = KnowledgeGraphConfig.load("config", name="graph")  # expects config/graph.yaml
    agent_conf = MarketIntelligenceConfig.load("config", name="market_intelligence")
    # Initialize global objects and store on app state
    app.state.graph = KnowledgeGraph(graph_conf)
    app.state.market_agent = MarketIntelligenceAgent(app.state.graph, agent_conf)


@app.on_event("shutdown")
def shutdown_event() -> None:
    app.state.graph.close()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/run/market_intelligence")
async def run_market_agent(background_tasks: BackgroundTasks) -> dict[str, str]:
    """
    Trigger the market intelligence agent as a background task.
    """
    background_tasks.add_task(app.state.market_agent.run)
    return {"status": "submitted"}
