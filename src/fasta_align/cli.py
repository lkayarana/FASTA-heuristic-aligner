from __future__ import annotations

import argparse
import sys

from .diagonals import best_diagonal, diagonal_counts
from .gapped import banded_smith_waterman
from .io_fasta import read_fasta
from .ktup import ktup_hits
from .report import AlignmentReport
from .scoring import Scoring
from .ungapped import best_ungapped_on_diagonal


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="fasta-align",
        description="FASTA-like heuristic aligner: k-tuple diagonals, ungapped best segment, banded gapped refinement.",
    )
    ap.add_argument("--query", required=True, help="Query FASTA file (single record recommended).")
    ap.add_argument("--db", required=True, help="Database FASTA file (one or more records).")
    ap.add_argument("--k", type=int, default=2, help="k-tuple size.")
    ap.add_argument("--band", type=int, default=8, help="Band half-width for banded Smith–Waterman.")
    ap.add_argument("--match", type=int, default=2, help="Match score.")
    ap.add_argument("--mismatch", type=int, default=-1, help="Mismatch score.")
    ap.add_argument("--gap", type=int, default=-2, help="Linear gap penalty.")
    ap.add_argument("--json", default=None, help="Optional JSON output path (for the best target only).")
    ap.add_argument("--top", type=int, default=1, help="How many best targets to show (by gapped score).")
    return ap


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    q_records = read_fasta(args.query)
    if not q_records:
        print("ERROR: Query FASTA is empty.", file=sys.stderr)
        raise SystemExit(2)
    if len(q_records) > 1:
        print("NOTE: Query FASTA has multiple records; using the first one.", file=sys.stderr)

    query = q_records[0]
    db_records = read_fasta(args.db)
    if not db_records:
        print("ERROR: Database FASTA is empty.", file=sys.stderr)
        raise SystemExit(2)

    scoring = Scoring(match=args.match, mismatch=args.mismatch, gap=args.gap)

    reports: list[AlignmentReport] = []
    for target in db_records:
        hits = ktup_hits(query.sequence, target.sequence, args.k)
        counts = diagonal_counts(hits)
        diag = best_diagonal(counts)

        ung = best_ungapped_on_diagonal(query.sequence, target.sequence, diag.shift, scoring)
        gap = banded_smith_waterman(query.sequence, target.sequence, diag.shift, args.band, scoring)

        reports.append(
            AlignmentReport(
                query_header=query.header,
                target_header=target.header,
                query_length=len(query.sequence),
                target_length=len(target.sequence),
                k=args.k,
                diagonal=diag,
                ungapped=ung,
                gapped=gap,
            )
        )

    reports.sort(key=lambda r: r.gapped.score, reverse=True)

    top_n = max(1, min(args.top, len(reports)))
    for i in range(top_n):
        print("=" * 72)
        print(reports[i].to_pretty_text())

    if args.json:
        reports[0].to_json(args.json)
        print("\nWrote JSON:", args.json)
