import pytest

from src.core.langchain_graph import LangchainGraphConfig, LangchainGraph


def test_langchain_graph_config_instantiation():
    # Instantiate config and ensure fields are set correctly
    config = LangchainGraphConfig(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="test",
        openai_api_key="dummy-key"
    )
    assert config.uri == "bolt://localhost:7687"
    assert config.user == "neo4j"
    assert config.password == "test"
    assert config.openai_api_key == "dummy-key"


def test_langchain_graph_initialization(monkeypatch):
    # Monkeypatch LangChain components to avoid actual initialization
    class FakeNeo4jGraph:
        def __init__(self, *args, **kwargs):
            pass

    class FakeQAChain:
        def __init__(self, *args, **kwargs):
            pass

    class FakeChatOpenAI:
        def __init__(self, *args, **kwargs):
            pass

    # Monkeypatch the imported classes
    monkeypatch.setattr("langchain.graphs.Neo4jGraph", FakeNeo4jGraph, raising=False)
    monkeypatch.setattr("langchain.chains.GraphCypherQAChain", FakeQAChain, raising=False)
    monkeypatch.setattr("langchain_openai.ChatOpenAI", FakeChatOpenAI, raising=False)

    config = LangchainGraphConfig(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="test",
        openai_api_key="dummy-key"
    )
    # Initialize the LangchainGraph; should not raise exceptions with monkeypatched dependencies
    graph = LangchainGraph(config)
    assert graph.config.uri == config.uri
