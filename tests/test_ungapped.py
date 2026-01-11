from fasta_align.scoring import Scoring
from fasta_align.ungapped import best_ungapped_on_diagonal


def test_ungapped_finds_segment():
    scoring = Scoring(match=2, mismatch=-1, gap=-2)
    q = "AAAAACCCCC"
    t = "GGGGACCCCC"
    res = best_ungapped_on_diagonal(q, t, shift=0, scoring=scoring)
    assert res.score >= 2  
    assert res.matches >= 1
    assert len(res.aligned_query) == len(res.aligned_target)
