from fasta_align.io_fasta import read_fasta


def test_read_fasta_single(tmp_path):
    p = tmp_path / "a.fasta"
    p.write_text(">seq1\nACGT\nAACC\n", encoding="utf-8")
    recs = read_fasta(str(p))
    assert len(recs) == 1
    assert recs[0].header == "seq1"
    assert recs[0].sequence == "ACGTAACC"


def test_read_fasta_multi(tmp_path):
    p = tmp_path / "b.fasta"
    p.write_text(">s1\nAAA\n>s2\nTTT\n", encoding="utf-8")
    recs = read_fasta(str(p))
    assert [r.header for r in recs] == ["s1", "s2"]
    assert [r.sequence for r in recs] == ["AAA", "TTT"]
