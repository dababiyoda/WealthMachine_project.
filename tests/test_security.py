import pytest

from src.core.security import sanitize_input, sign_graph_query, verify_graph_query


def test_sanitize_input_strips_tags():
    dirty = "<script>alert('x')</script>Hello <b>world</b>"
    cleaned = sanitize_input(dirty)
    assert "<script>" not in cleaned
    assert "<b>" not in cleaned
    # inner text should remain
    assert "alert('x')" in cleaned
    assert "Hello" in cleaned and "world" in cleaned


def test_sign_graph_query_consistency():
    query = "MATCH (n) RETURN n"
    sig1 = sign_graph_query(query)
    sig2 = sign_graph_query(query)
    assert sig1 == sig2


def test_verify_graph_query():
    query = "MATCH (n) RETURN n"
    signature = sign_graph_query(query)
    assert verify_graph_query(query, signature)

    tampered = signature[:-1] + ("0" if signature[-1] != "0" else "1")
    assert not verify_graph_query(query, tampered)
