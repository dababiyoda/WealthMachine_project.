from prometheus_client import start_http_server, Summary, Counter, Gauge
from typing import Any, Callable, TypeVar, cast

# Prometheus metrics definitions
REQUEST_TIME = Summary('app_request_processing_seconds', 'Time spent processing requests')
OPPORTUNITIES_FOUND = Counter('opportunities_found_total', 'Number of opportunities identified by agents')
AGENT_ERRORS = Counter('agent_errors_total', 'Number of errors encountered by agents')
GRAPH_NODES = Gauge('knowledge_graph_nodes', 'Current number of nodes in the knowledge graph')

F = TypeVar('F', bound=Callable[..., Any])

def start_metrics_server(port: int = 8001) -> None:
    """
    Starts a Prometheus metrics HTTP server on the specified port.

    Args:
        port: The port number on which to expose the metrics endpoint. Defaults to 8001.
    """
    start_http_server(port)


def update_graph_nodes(count: int) -> None:
    """
    Updates the gauge for knowledge graph node count.

    Args:
        count: The current number of nodes in the knowledge graph.
    """
    GRAPH_NODES.set(count)


def track_request_time(func: F) -> F:
    """
    Decorator that measures the execution time of a function and records it in the REQUEST_TIME metric.

    Args:
        func: The function to be wrapped.

    Returns:
        A wrapped function that records its execution time.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with REQUEST_TIME.time():
            return func(*args, **kwargs)
    return cast(F, wrapper)
