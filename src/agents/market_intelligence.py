import asyncio
from typing import Any, Dict, List

import aiohttp
from pydantic import BaseModel

from ..core.knowledge_graph import KnowledgeGraph


class MarketIntelligenceConfig(BaseModel):
    """Configuration for the Market Intelligence Agent."""

    news_api_url: str
    sentiment_endpoint: str


class MarketIntelligenceAgent:
    """
    A simple agent that gathers market data, performs sentiment analysis and
    updates the knowledge graph with findings.
    """

    def __init__(self, graph: KnowledgeGraph, config: MarketIntelligenceConfig) -> None:
        self.graph = graph
        self.config = config

    async def fetch_news(self, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        async with session.get(self.config.news_api_url) as resp:
            return await resp.json()

    async def analyze_sentiment(self, session: aiohttp.ClientSession, text: str) -> float:
        payload = {"text": text}
        async with session.post(self.config.sentiment_endpoint, json=payload) as resp:
            data = await resp.json()
            return data.get("sentiment", 0.0)

    async def process_article(self, article: Dict[str, Any], session: aiohttp.ClientSession) -> None:
        title = article.get("title", "")
        content = article.get("content", "")
        sentiment = await self.analyze_sentiment(session, content)
        node_props = {
            "id": article.get("id"),
            "title": title,
            "sentiment": sentiment,
        }
        self.graph.create_node("Article", node_props)

    async def run(self) -> None:
        async with aiohttp.ClientSession() as session:
            articles = await self.fetch_news(session)
            tasks = [self.process_article(article, session) for article in articles]
            await asyncio.gather(*tasks)
