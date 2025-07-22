from typing import Any, Dict, List, Optional

from neo4j import GraphDatabase
from pydantic import BaseModel


class KnowledgeGraphConfig(BaseModel):
    """Configuration for connecting to the Neo4j graph database."""

    uri: str
    user: str
    password: str


class KnowledgeGraph:
    """
    Wrapper around Neo4j for CRUD operations and retrieval-augmented generation (RAG).

    This class encapsulates connection management and basic operations for storing and
    retrieving nodes and relationships.  It also provides a simple graph-RAG
    implementation that retrieves context subgraphs for LLM prompts.
    """

    def __init__(self, config: KnowledgeGraphConfig) -> None:
        self._driver = GraphDatabase.driver(config.uri, auth=(config.user, config.password))

    def close(self) -> None:
        """Close the underlying database driver."""
        if self._driver:
            self._driver.close()

    def create_node(self, label: str, properties: Dict[str, Any]) -> None:
        query = "CREATE (n:{label} $props)".format(label=label)
        with self._driver.session() as session:
            session.run(query, props=properties)

    def create_relationship(
        self,
        start_label: str,
        start_key: str,
        end_label: str,
        end_key: str,
        rel_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Create a relationship of type `rel_type` between two nodes identified by
        their unique keys (assumed to be stored in the `id` property).
        """
        properties = properties or {}
        query = (
            "MATCH (a:{start} {{id: $start_key}}), (b:{end} {{id: $end_key}}) "
            "CREATE (a)-[r:{rel_type} $props]->(b)"
        ).format(start=start_label, end=end_label, rel_type=rel_type)
        with self._driver.session() as session:
            session.run(query, start_key=start_key, end_key=end_key, props=properties)

    def query(self, cypher: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Run an arbitrary Cypher query and return the results."""
        with self._driver.session() as session:
            result = session.run(cypher, parameters or {})
            return [record.data() for record in result]

    def get_context_subgraph(self, entity_id: str, hops: int = 2, max_nodes: int = 50) -> Dict[str, Any]:
        """
        Retrieve a subgraph around a given entity up to a certain number of hops.
        This can be used as context for retrieval augmented generation.
        """
        query = (
            "MATCH (n {id: $entity_id})"
            " CALL apoc.path.subgraphNodes(n, {maxLevel: $hops, limit: $max_nodes}) YIELD node"
            " RETURN collect(DISTINCT node) AS nodes"
        )
        nodes = []
        with self._driver.session() as session:
            result = session.run(query, entity_id=entity_id, hops=hops, max_nodes=max_nodes)
            record = result.single()
            if record:
                nodes = record["nodes"]
        # For simplicity, return a list of node property dictionaries
        return [dict(n) for n in nodes]


    def subgraph_to_text(self, entity_id: str, hops: int = 2, max_nodes: int = 50) -> str:
        """
        Convert a context subgraph around an entity into a text representation.

        The returned string can be used as context for language model prompts.
        """
        nodes = self.get_context_subgraph(entity_id, hops, max_nodes)
        lines: list[str] = []
        for node in nodes:
            # Each node is a dictionary-like structure from Neo4j driver
            labels = node.get('labels') if isinstance(node, dict) else []
            props = {k: v for k, v in node.items() if k != 'labels'} if isinstance(node, dict) else {}
            label_str = ":".join(labels) if labels else ''
            prop_parts = []
            for k, v in props.items():
                prop_parts.append(f"{k}={v}")
            prop_str = ", ".join(prop_parts)
            lines.append(f"{label_str}({prop_str})")
        # Join lines with semicolons for brevity
        return "; ".join(lines)
