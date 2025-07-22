"""Tests for configuration loading using Pydantic BaseConfig."""
import os
from pathlib import Path

from src.core.config import BaseConfig


def test_load_graph_config() -> None:
    # Compute path to graph.yaml relative to project root
    project_root = Path(__file__).resolve().parents[1]
    config_file = project_root / "config" / "graph.yaml"
    # Ensure file exists
    assert config_file.exists(), f"Missing config file: {config_file}"
    # Load the YAML using BaseConfig
    class GraphSettings(BaseConfig):
        uri: str
        user: str
        password: str
    settings = GraphSettings.from_yaml_or_json(str(config_file))
    assert settings.uri.startswith("bolt"), "URI should start with bolt or neo4j protocol"
    assert settings.user, "User should not be empty"
    assert settings.password, "Password should not be empty"
