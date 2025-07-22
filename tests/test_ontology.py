"""Tests for ontology loading and schema generation."""
from pathlib import Path
from src.core.ontology import Ontology


def test_load_ontology() -> None:
    root = Path(__file__).resolve().parents[1]
    ontology_file = root / "config" / "ontology-schema.yaml"
    assert ontology_file.exists(), f"Ontology file not found: {ontology_file}"
    ontology = Ontology.from_yaml(ontology_file)
    assert "Opportunity" in ontology.entities, "Ontology should contain Opportunity entity"
    constraints = ontology.generate_neo4j_schema()
    # There should be at least one constraint (primary keys)
    assert constraints, "No constraints generated from ontology"
