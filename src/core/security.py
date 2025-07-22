import os
import re
import hmac
import hashlib
from typing import Any, Dict, Union

SECRET_KEY = os.environ.get("SIGNING_SECRET", "default-secret")


def sanitize_input(data: Union[str, Dict[str, Any]]) -> Union[str, Dict[str, Any]]:
    """
    Sanitizes input data by removing potentially harmful HTML or script tags.
    Handles strings and dictionaries recursively.
    """
    if isinstance(data, str):
        # Strip <script> tags while preserving their inner text
        without_scripts = re.sub(
            r"<script.*?>(.*?)</script>",
            r"\1",
            data,
            flags=re.IGNORECASE | re.DOTALL,
        )

        # Remove any remaining HTML tags
        cleaned = re.sub(r"<[^>]*>", "", without_scripts)
        return cleaned
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    else:
        return data


def sign_query(query: str) -> str:
    """
    Generates a HMAC signature for a Cypher query using a secret key.
    """
    signature = hmac.new(SECRET_KEY.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature


def verify_query(query: str, signature: str) -> bool:
    """
    Verifies that the provided signature matches the query signature.
    """
    expected_signature = sign_query(query)
    return hmac.compare_digest(expected_signature, signature)


def sign_graph_query(query: str) -> str:
    """Wrapper for signing graph (Cypher) queries."""
    return sign_query(query)


def verify_graph_query(query: str, signature: str) -> bool:
    """Wrapper for verifying graph query signatures."""
    return verify_query(query, signature)
