from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FastaRecord:
    header: str
    sequence: str


def read_fasta(path: str) -> list[FastaRecord]:
    records: list[FastaRecord] = []
    header: str | None = None
    seq_parts: list[str] = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                # finalize previous
                if header is not None:
                    seq = "".join(seq_parts).replace(" ", "").upper()
                    records.append(FastaRecord(header=header, sequence=seq))
                header = line[1:].strip() or f"record_{len(records)+1}"
                seq_parts = []
            else:
                seq_parts.append(line)

    if header is not None:
        seq = "".join(seq_parts).replace(" ", "").upper()
        records.append(FastaRecord(header=header, sequence=seq))

    return records
