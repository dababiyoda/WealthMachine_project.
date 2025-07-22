from typing import List, Dict, Tuple
from collections import defaultdict


def audit_bias(scores: List[float], categories: List[str]) -> Tuple[Dict[str, float], float]:
    """
    Audits scoring bias by computing average score per category and the fairness gap.
    :param scores: Numeric scores from evaluations.
    :param categories: Category label for each score (e.g., sector or geography).
    :return: A tuple containing category averages and the difference between max and min averages.
    """
    if len(scores) != len(categories):
        raise ValueError("Scores and categories must have the same length")
    distribution: Dict[str, List[float]] = defaultdict(list)
    for score, cat in zip(scores, categories):
        distribution[cat].append(score)
    averages: Dict[str, float] = {cat: (sum(vals) / len(vals)) if vals else 0.0 for cat, vals in distribution.items()}
    if averages:
        fairness_gap = max(averages.values()) - min(averages.values())
    else:
        fairness_gap = 0.0
    return averages, fairness_gap
