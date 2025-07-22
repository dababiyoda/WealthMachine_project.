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
    """Initialize LangchainGraph with patched dependencies."""

    class FakeNeo4jGraph:
        def __init__(self, *args, **kwargs):
            pass

    class FakeQAChain:
        def __init__(self, *args, **kwargs):
            pass

    class FakeChatOpenAI:
        def __init__(self, *args, **kwargs):
            pass

    # Provide stub modules so importing langchain components does not fail
    import types, sys
    fake_graphs = types.ModuleType("langchain.graphs")
    fake_chains = types.ModuleType("langchain.chains")
    fake_prompts = types.ModuleType("langchain.prompts")
    fake_openai = types.ModuleType("langchain_openai")
    sys.modules.setdefault("langchain.graphs", fake_graphs)
    sys.modules.setdefault("langchain.chains", fake_chains)
    sys.modules.setdefault("langchain.prompts", fake_prompts)
    sys.modules.setdefault("langchain_openai", fake_openai)

    monkeypatch.setattr(fake_graphs, "Neo4jGraph", FakeNeo4jGraph, raising=False)
    monkeypatch.setattr(fake_chains, "GraphCypherQAChain", FakeQAChain, raising=False)
    monkeypatch.setattr(fake_prompts, "PromptTemplate", lambda **kwargs: None, raising=False)
    monkeypatch.setattr(fake_openai, "ChatOpenAI", FakeChatOpenAI, raising=False)

    config = LangchainGraphConfig(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="test",
        openai_api_key="dummy-key"
    )
    # Initialize the LangchainGraph; should not raise exceptions with monkeypatched dependencies
    graph = LangchainGraph(config)
    assert graph.config.uri == config.uri
