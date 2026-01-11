from fasta_align.scoring import Scoring
from fasta_align.gapped import banded_smith_waterman


def test_gapped_alignment_runs():
    scoring = Scoring(match=2, mismatch=-1, gap=-2)
    q = "ACGTACGT"
    t = "ACG---".replace("-", "") + "TACGT"
    res = banded_smith_waterman(q, t, shift=0, band=5, scoring=scoring)
    assert res.score >= 0
    assert len(res.aligned_query) == len(res.aligned_target)
