from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .ktup import Hit


@dataclass(frozen=True)
class DiagonalSummary:
    shift: int
    hit_count: int


def diagonal_counts(hits: list[Hit]) -> dict[int, int]:
    counts: dict[int, int] = defaultdict(int)
    for h in hits:
        counts[h.shift] += 1
    return dict(counts)


def best_diagonal(counts: dict[int, int]) -> DiagonalSummary:
    if not counts:
        return DiagonalSummary(shift=0, hit_count=0)

    shift = max(counts, key=lambda s: (counts[s], -abs(s), -s))
    return DiagonalSummary(shift=shift, hit_count=counts[shift])
