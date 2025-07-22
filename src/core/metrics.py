from pydantic import BaseModel
from pathlib import Path
from typing import Union
import yaml

class SuccessMetrics(BaseModel):
    """
    Data model for success metrics configuration.

    Attributes:
        opportunities_per_week: Expected number of opportunities discovered per week.
        reasoning_accuracy: Desired accuracy of agent reasoning (0-1 scale).
        failure_probability_threshold: Threshold for probability of failure (0-1 scale).
    """

    opportunities_per_week: float
    reasoning_accuracy: float
    failure_probability_threshold: float


def load_success_metrics(file_path: Union[str, Path]) -> SuccessMetrics:
    """
    Load success metrics configuration from a YAML file.

    Args:
        file_path: Path to the YAML file containing success metrics.

    Returns:
        SuccessMetrics: Loaded success metrics model.
    """
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return SuccessMetrics(**data)
