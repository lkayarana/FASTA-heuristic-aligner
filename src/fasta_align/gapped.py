from __future__ import annotations

from dataclasses import dataclass

from .scoring import Scoring


@dataclass(frozen=True)
class GappedResult:
    shift: int
    band: int
    score: int
    matches: int
    aligned_query: str
    aligned_target: str


def banded_smith_waterman(
    query: str,
    target: str,
    shift: int,
    band: int,
    scoring: Scoring,
) -> GappedResult:
    n, m = len(query), len(target)
    if n == 0 or m == 0:
        return GappedResult(shift=shift, band=band, score=0, matches=0, aligned_query="", aligned_target="")

    # DP score matrix but sparse by band: store rows as dict j->score
    # traceback pointers: 0=stop, 1=diag, 2=up (gap in target), 3=left (gap in query)
    H: list[dict[int, int]] = [dict() for _ in range(n + 1)]
    T: list[dict[int, int]] = [dict() for _ in range(n + 1)]

    best_score = 0
    best_pos = (0, 0)

    for i in range(1, n + 1):
        # allowed j range based on band around shift
        j_center = i + shift
        j_min = max(1, j_center - band)
        j_max = min(m, j_center + band)

        for j in range(j_min, j_max + 1):
            diag = H[i - 1].get(j - 1, 0) + scoring.score_pair(query[i - 1], target[j - 1])
            up = H[i - 1].get(j, 0) + scoring.gap
            left = H[i].get(j - 1, 0) + scoring.gap
            val = max(0, diag, up, left)

            if val == 0:
                tb = 0
            elif val == diag:
                tb = 1
            elif val == up:
                tb = 2
            else:
                tb = 3

            H[i][j] = val
            T[i][j] = tb

            if val > best_score:
                best_score = val
                best_pos = (i, j)

    # Traceback from best_pos until stop (0)
    i, j = best_pos
    aln_q: list[str] = []
    aln_t: list[str] = []
    while i > 0 and j > 0:
        tb = T[i].get(j, 0)
        if tb == 0:
            break
        if tb == 1:
            aln_q.append(query[i - 1])
            aln_t.append(target[j - 1])
            i -= 1
            j -= 1
        elif tb == 2:
            aln_q.append(query[i - 1])
            aln_t.append("-")
            i -= 1
        else:  # tb == 3
            aln_q.append("-")
            aln_t.append(target[j - 1])
            j -= 1

    aln_q.reverse()
    aln_t.reverse()
    aq = "".join(aln_q)
    at = "".join(aln_t)
    matches = sum(1 for x, y in zip(aq, at) if x == y and x != "-" and y != "-")

    return GappedResult(
        shift=shift,
        band=band,
        score=best_score,
        matches=matches,
        aligned_query=aq,
        aligned_target=at,
    )
