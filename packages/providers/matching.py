from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Optional


def normalize_alias(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    return re.sub(r"\s+", " ", normalized)


@dataclass
class MatchResult:
    host_slug: str
    matched_alias: str
    confidence: float


def match_host_alias(text: str, alias_map: dict[str, Iterable[str]]) -> Optional[MatchResult]:
    normalized_text = normalize_alias(text)
    best: Optional[MatchResult] = None
    for host_slug, aliases in alias_map.items():
        for alias in aliases:
            normalized_alias = normalize_alias(alias)
            if not normalized_alias:
                continue
            if normalized_alias in normalized_text:
                confidence = min(1.0, 0.55 + (len(normalized_alias) / max(len(normalized_text), 1)))
                if best is None or confidence > best.confidence:
                    best = MatchResult(host_slug=host_slug, matched_alias=normalized_alias, confidence=round(confidence, 4))
    return best
