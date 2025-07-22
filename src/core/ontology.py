"""
Ontology definitions and schema generation for the Wealth Machine project.

This module loads the ontology defined in a YAML file and exposes Pydantic models
for entities and relationships. It also provides helper functions to generate
Cypher statements for Neo4j constraints based on the ontology.
"""
from __future__ import annotations

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class Property(BaseModel):
    type: str = Field(..., description="Data type of the property, e.g. string, integer, uuid")
    primary: bool = Field(default=False, description="Whether this property is the primary key")

class RelationshipDef(BaseModel):
    type: str = Field(..., description="Relationship type (edge label)")
    target: str = Field(..., description="Target entity name")

class EntityDef(BaseModel):
    description: Optional[str]
    properties: Dict[str, Property]
    relationships: Optional[List[RelationshipDef]] = None

class Ontology(BaseModel):
    entities: Dict[str, EntityDef]
    relationships: Dict[str, Dict[str, str]]

    @classmethod
    def from_yaml(cls, filepath: str | Path) -> "Ontology":
        """Load ontology from a YAML file and parse into Pydantic models."""
        path = Path(filepath)
        with path.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def generate_neo4j_constraints(self) -> List[str]:
        """Generate Cypher statements to enforce unique constraints on primary keys."""
        statements: List[str] = []
        for entity_name, entity in self.entities.items():
            for prop_name, prop in entity.properties.items():
                if prop.primary:
                    constraint = (
                        f"CREATE CONSTRAINT IF NOT EXISTS ON (n:{entity_name}) "
                        f"ASSERT n.{prop_name} IS UNIQUE"
                    )
                    statements.append(constraint)
        return statements

    def generate_neo4j_schema(self) -> List[str]:
        """Generate a list of Cypher statements to create indexes and constraints."""
        return self.generate_neo4j_constraints()

# Utility function for direct usage

def load_ontology_and_generate_schema(path: str | Path) -> List[str]:
    """Load ontology from YAML and return Neo4j schema statements."""
    ontology = Ontology.from_yaml(path)
    return ontology.generate_neo4j_schema()
