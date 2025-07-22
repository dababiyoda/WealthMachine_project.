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
