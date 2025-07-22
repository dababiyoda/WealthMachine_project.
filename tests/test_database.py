"""
Tests for the Database module which wraps SQLAlchemy for relational storage.
"""

from src.core.database import Database, DatabaseConfig, Transaction


def test_add_transaction() -> None:
    """Test that a transaction can be created and persisted using an in-memory SQLite DB."""
    # Use in-memory SQLite for testing
    db = Database(DatabaseConfig(uri="sqlite:///:memory:"))
    db.create_tables()
    tx = db.add_transaction(entity_id="entity1", action="create", data={"amount": 42})
    assert tx.id is not None
    assert tx.entity_id == "entity1"
    assert tx.action == "create"
    assert tx.data == {"amount": 42}
