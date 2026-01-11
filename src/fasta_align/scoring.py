from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scoring:
    match: int = 2
    mismatch: int = -1
    gap: int = -2  # linear gap penalty

    def score_pair(self, a: str, b: str) -> int:
        return self.match if a == b else self.mismatch
