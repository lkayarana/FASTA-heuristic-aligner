set -euo pipefail

fasta-align \
  --query examples/query.fasta \
  --db examples/database.fasta \
  --k 2 \
  --band 8 \
  --match 2 --mismatch -1 --gap -2 \
  --top 2 \
  --json examples/out.json
