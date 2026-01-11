from __future__ import annotations

from dataclasses import dataclass

from .scoring import Scoring


@dataclass(frozen=True)
class UngappedResult:
    shift: int
    score: int
    matches: int
    q_start: int
    q_end: int  # inclusive
    t_start: int
    t_end: int  # inclusive
    aligned_query: str
    aligned_target: str


def _diag_start_positions(q_len: int, t_len: int, shift: int) -> tuple[int, int]:
    if shift >= 0:
        q0 = 0
        t0 = shift
    else:
        q0 = -shift
        t0 = 0
    # ensure in bounds
    if q0 >= q_len or t0 >= t_len:
        return (q_len, t_len)
    return (q0, t0)


def best_ungapped_on_diagonal(query: str, target: str, shift: int, scoring: Scoring) -> UngappedResult:
    q_len, t_len = len(query), len(target)
    q0, t0 = _diag_start_positions(q_len, t_len, shift)
    if q0 >= q_len or t0 >= t_len:
        return UngappedResult(
            shift=shift,
            score=0,
            matches=0,
            q_start=0,
            q_end=-1,
            t_start=0,
            t_end=-1,
            aligned_query="",
            aligned_target="",
        )

    L = min(q_len - q0, t_len - t0)

    best_score = 0
    best_start = 0
    best_end = -1

    cur_score = 0
    cur_start = 0

    for i in range(L):
        a = query[q0 + i]
        b = target[t0 + i]
        s = scoring.score_pair(a, b)

        if cur_score + s <= 0:
            cur_score = 0
            cur_start = i + 1
        else:
            cur_score += s
            if cur_score > best_score:
                best_score = cur_score
                best_start = cur_start
                best_end = i

    if best_end < best_start:
        return UngappedResult(
            shift=shift,
            score=0,
            matches=0,
            q_start=0,
            q_end=-1,
            t_start=0,
            t_end=-1,
            aligned_query="",
            aligned_target="",
        )

    q_start = q0 + best_start
    q_end = q0 + best_end
    t_start = t0 + best_start
    t_end = t0 + best_end

    aq = query[q_start : q_end + 1]
    at = target[t_start : t_end + 1]
    matches = sum(1 for x, y in zip(aq, at) if x == y)

    return UngappedResult(
        shift=shift,
        score=best_score,
        matches=matches,
        q_start=q_start,
        q_end=q_end,
        t_start=t_start,
        t_end=t_end,
        aligned_query=aq,
        aligned_target=at,
    )
