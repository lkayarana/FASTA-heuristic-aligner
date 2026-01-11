# Algorithm

This project follows a FASTA-like heuristic:

## 1) k-tuple hits
For each k-mer in the target, if it exists in the query index, record hits (i, j).

## 2) Diagonal / shift
Each hit belongs to a diagonal defined by:

shift = j - i

We count hits per shift and choose the **most populated diagonal**.

## 3) Ungapped "normal solution"
Once the best shift is chosen, we consider the entire diagonal overlap and score each aligned pair.
We then choose the best *contiguous* scoring segment along that diagonal using a maximum-subarray approach.
This gives:
- shift
- ungapped alignment strings
- score
- match count

## 4) Gapped "gap solution"
We refine using local alignment (Smith–Waterman), but only inside a band around the best diagonal:

|(j - i) - shift| <= band

This allows gaps and can increase the number of matches.
