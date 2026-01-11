from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Hit:
    q_pos: int
    t_pos: int
    shift: int  # t_pos - q_pos


def build_kmer_index(seq: str, k: int) -> dict[str, list[int]]:
    idx: dict[str, list[int]] = defaultdict(list)
    if k <= 0:
        raise ValueError("k must be >= 1")
    if len(seq) < k:
        return dict(idx)

    for i in range(0, len(seq) - k + 1):
        idx[seq[i : i + k]].append(i)
    return dict(idx)


def ktup_hits(query: str, target: str, k: int) -> list[Hit]:
    q_idx = build_kmer_index(query, k)
    hits: list[Hit] = []
    if len(target) < k:
        return hits

    for j in range(0, len(target) - k + 1):
        kmer = target[j : j + k]
        for i in q_idx.get(kmer, []):
            hits.append(Hit(q_pos=i, t_pos=j, shift=j - i))
    return hits
