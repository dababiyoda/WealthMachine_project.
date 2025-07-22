import pytest

from src.core.security import sanitize_input, sign_graph_query, verify_graph_query


def test_sanitize_input():
    dirty = "<script>alert('x')</script>Hello <b>world</b>"
    cleaned = sanitize_input(dirty)
    # Ensure that HTML tags are removed but inner text remains
    assert "<script>" not in cleaned
    assert "<b>" not in cleaned
    assert "alert('x')" in cleaned
    assert "Hello" in cleaned and "world" in cleaned


def test_sign_and_verify():
    secret = b'secret-key'
    query = "MATCH (n) RETURN n"
    signature = sign_graph_query(query, secret)
    assert isinstance(signature, str)
    # Verify signature matches original query and secret
    assert verify_graph_query(query, signature, secret)
