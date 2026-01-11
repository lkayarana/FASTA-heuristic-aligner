from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

from .diagonals import DiagonalSummary
from .gapped import GappedResult
from .ungapped import UngappedResult


@dataclass(frozen=True)
class AlignmentReport:
    query_header: str
    target_header: str
    query_length: int
    target_length: int
    k: int
    diagonal: DiagonalSummary
    ungapped: UngappedResult
    gapped: GappedResult

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_header": self.query_header,
            "target_header": self.target_header,
            "query_length": self.query_length,
            "target_length": self.target_length,
            "k": self.k,
            "diagonal": asdict(self.diagonal),
            "ungapped": asdict(self.ungapped),
            "gapped": asdict(self.gapped),
            "matches_increased_by_gaps": self.gapped.matches - self.ungapped.matches,
            "score_increased_by_gaps": self.gapped.score - self.ungapped.score,
        }

    def to_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    def to_pretty_text(self) -> str:
        inc_m = self.gapped.matches - self.ungapped.matches
        inc_s = self.gapped.score - self.ungapped.score

        lines = []
        lines.append(f"Query : {self.query_header} (len={self.query_length})")
        lines.append(f"Target: {self.target_header} (len={self.target_length})")
        lines.append("")
        lines.append(f"k={self.k}")
        lines.append(f"Most populated diagonal shift = {self.diagonal.shift}  (hits={self.diagonal.hit_count})")
        lines.append("")
        lines.append("UNGAPPED (normal solution)")
        lines.append(f"  score={self.ungapped.score}  matches={self.ungapped.matches}")
        lines.append(f"  q[{self.ungapped.q_start}:{self.ungapped.q_end + 1}] vs t[{self.ungapped.t_start}:{self.ungapped.t_end + 1}]")
        lines.append(f"  Q: {self.ungapped.aligned_query}")
        lines.append(f"  T: {self.ungapped.aligned_target}")
        lines.append("")
        lines.append("GAPPED (gap solution, banded Smith–Waterman)")
        lines.append(f"  band={self.gapped.band}  score={self.gapped.score}  matches={self.gapped.matches}")
        lines.append(f"  Q: {self.gapped.aligned_query}")
        lines.append(f"  T: {self.gapped.aligned_target}")
        lines.append("")
        lines.append(f"Delta: matches {self.ungapped.matches} -> {self.gapped.matches}  (Δ={inc_m})")
        lines.append(f"Delta: score   {self.ungapped.score} -> {self.gapped.score}  (Δ={inc_s})")
        return "\n".join(lines)
