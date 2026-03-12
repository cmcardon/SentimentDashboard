from __future__ import annotations

from typing import Optional


def clamp_score(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def compute_composite_score(
    attention: float,
    discoverability: float,
    engagement: float,
    sentiment: float,
    crossover: float,
) -> float:
    return clamp_score(
        (attention * 0.30)
        + (discoverability * 0.20)
        + (engagement * 0.20)
        + (sentiment * 0.15)
        + (crossover * 0.15)
    )


def compute_momentum(series: list[float], window: int) -> Optional[float]:
    if len(series) <= window:
        return None
    previous = series[-(window + 1)]
    current = series[-1]
    if previous == 0:
        return None
    return round(((current - previous) / previous) * 100.0, 2)


def normalize_rank(rank: float) -> float:
    return clamp_score((110.0 - (rank * 6.0)) * 0.9)
