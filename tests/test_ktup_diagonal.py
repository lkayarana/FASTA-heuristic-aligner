from fasta_align.ktup import ktup_hits
from fasta_align.diagonals import diagonal_counts, best_diagonal


def test_best_diagonal_simple():
    q = "AACCATCATA"
    t = "CCGAACCATCA"
    hits = ktup_hits(q, t, k=2)
    counts = diagonal_counts(hits)
    diag = best_diagonal(counts)
    assert isinstance(diag.shift, int)
    assert diag.hit_count >= 1
