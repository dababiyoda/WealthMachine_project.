"""
Database module for storing transactional data using PostgreSQL.

This module defines SQLAlchemy models and a database wrapper for
interacting with a relational database. It complements the Neo4j
knowledge graph by persisting transactional data that doesn’t naturally
fit into a graph structure.
"""

from __future__ import annotations

from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Base class for declarative models
Base = declarative_base()

class DatabaseConfig(BaseModel):
    """Configuration for connecting to the Postgres database."""
    uri: str  # e.g., "postgresql+psycopg2://user:password@host:port/dbname"

class Transaction(Base):
    """Simple transaction/event record stored in Postgres."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(String, index=True)
    action = Column(String, index=True)
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Database:
    """Wrapper around SQLAlchemy engine and session for database operations."""

    def __init__(self, config: DatabaseConfig) -> None:
        self.engine = create_engine(config.uri)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self) -> None:
        """Create database tables based on defined models."""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Obtain a new SQLAlchemy session."""
        return self.SessionLocal()

    def add_transaction(self, entity_id: str, action: str, data: Optional[Any] = None) -> Transaction:
        """Create and persist a transaction/event record."""
        session: Session = self.get_session()
        try:
            tx = Transaction(entity_id=entity_id, action=action, data=data)
            session.add(tx)
            session.commit()
            session.refresh(tx)
            return tx
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
