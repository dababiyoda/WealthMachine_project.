from pathlib import Path
import pytest

from src.core.metrics import load_success_metrics, SuccessMetrics


def test_load_success_metrics(tmp_path: Path) -> None:
    """Test loading success metrics from a temporary YAML file."""
    content = """
    opportunities_per_week: 5
    reasoning_accuracy: 0.9
    failure_probability_threshold: 0.01
    """
    file_path = tmp_path / "metrics.yaml"
    file_path.write_text(content.strip())

    metrics = load_success_metrics(file_path)

    assert isinstance(metrics, SuccessMetrics)
    assert metrics.opportunities_per_week == 5
    assert abs(metrics.reasoning_accuracy - 0.9) < 1e-6
    assert abs(metrics.failure_probability_threshold - 0.01) < 1e-6
