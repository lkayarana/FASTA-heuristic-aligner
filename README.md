# FASTA Heuristic Aligner

This project implements a **FASTA-like heuristic sequence alignment algorithm** developed for a bioinformatics assignment.  
The objective is to efficiently identify high-scoring alignments between a query sequence and one or more database sequences by combining **k-tuple matching**, **diagonal analysis**, and **local alignment refinement**.

The implementation follows the classical FASTA workflow:
1. k-tuple hit detection  
2. Selection of the most populated diagonal  
3. Ungapped local alignment (normal solution)  
4. Gapped alignment using banded Smith–Waterman (gap solution)

---

## Features

- FASTA file parsing (multi-line, multiple records)
- k-tuple (k-mer) indexing and hit detection
- Diagonal (shift) counting to identify the most promising alignment region
- Ungapped local alignment along the best diagonal
- Banded Smith–Waterman local alignment allowing gaps
- Comparison of ungapped vs gapped solutions
- Command-line interface (CLI)
- Optional JSON output
- Unit tests for core components

---

## Algorithm Overview

### 1. k-tuple Matching
The query sequence is indexed into overlapping k-mers.  
Each k-mer in the target sequence is matched against this index to identify **k-tuple hits**.

Each hit defines a diagonal using the formula:
shift = target_position − query_position


---

### 2. Most Populated Diagonal
All hits are grouped by their diagonal shift.  
The diagonal with the **highest number of hits** is selected as the most likely alignment region (the *most populated diagonal*).

---

### 3. Ungapped Alignment (Normal Solution)
Along the selected diagonal, a **local ungapped alignment** is computed.

- Only matches and mismatches are allowed
- No gaps are introduced
- The best-scoring contiguous segment is found using a Kadane-style maximum subarray approach

This represents the **normal FASTA solution**.

---

### 4. Gapped Alignment (Gap Solution)
To refine the alignment, a **banded Smith–Waterman** local alignment is performed:

- The dynamic programming matrix is restricted to a band around the selected diagonal
- Gaps are allowed with a linear gap penalty
- This step can increase the number of matches compared to the ungapped solution

This represents the **gap solution**.

---

## Installation

From the project root directory:

```bash
pip install -e .[dev]
```

---

## Usage

Command-line interface

```bash
fasta-align --query QUERY.fasta --db DATABASE.fasta
```

---

## Command Options

```bash
--k K               k-tuple size (default: 2)
--band BAND         Band half-width for banded Smith–Waterman
--match MATCH       Match score
--mismatch MISMATCH Mismatch score
--gap GAP           Linear gap penalty
--top TOP           Number of best targets to display
--json OUTPUT.json  Save results as JSON (best target only)
```

---

## Example

```bash
fasta-align \
  --query examples/query.fasta \
  --db examples/database.fasta \
  --k 2 \
  --band 8
```

## Output

For each selected target sequence, the program reports:

- Query and target identifiers

- Most populated diagonal and hit count

Ungapped alignment:

- Alignment strings

- Score

- Number of matches

Gapped alignment:

- Alignment strings with gaps

- Score

- Number of matches

- Difference in score and match count between ungapped and gapped solutions

---

## Complexity

Let:

- n = length of the query sequence

- m = length of the target sequence

- k-tuple matching: O(n + m) (excluding hit multiplicity)

- Diagonal scoring: O(L), where L is the diagonal overlap length

- Banded Smith–Waterman: O(n × band)
(significantly faster than full O(n × m) dynamic programming)

---

## Educational Purpose

This project is intended for educational use and demonstrates:

- Heuristic sequence alignment principles

- The role of diagonals in FASTA-like algorithms

- The difference between ungapped and gapped alignments

- Practical use of banded dynamic programming for efficiency