# Complexity

Let n = len(query), m = len(target).

## k-tuple hits
Index build: O(n)
Scan target: O(m) lookups; total hits depend on repeats.

## Diagonal counting
O(#hits)

## Ungapped diagonal scoring
Diagonal overlap length L <= min(n, m)
Kadane scan: O(L)

## Banded Smith–Waterman
Cells computed: O(n * (2*band+1)) instead of O(n*m)
Traceback is at most the alignment length.
