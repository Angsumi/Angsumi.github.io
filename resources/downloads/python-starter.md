# Python for researchers: a small, reproducible start

## Set up an isolated environment
```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
```
On Windows, use `.venv\Scripts\activate` in an appropriate shell.
Keep `.venv/`, raw confidential data and credentials out of Git.

## Validate a CSV header with the standard library
Save as `check_table.py` and run with `python check_table.py example.csv`.
```python
import csv
import sys
from pathlib import Path

path = Path(sys.argv[1])
with path.open(newline='', encoding='utf-8') as handle:
    reader = csv.DictReader(handle)
    required = {'sample_id', 'condition'}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError('Expected sample_id and condition columns')
    seen = set()
    for line_number, row in enumerate(reader, 2):
        sample = (row.get('sample_id') or '').strip()
        condition = (row.get('condition') or '').strip()
        if not sample or not condition or sample in seen:
            raise ValueError(f'Missing or repeated identifier at line {line_number}')
        seen.add(sample)
print(f'Validated {len(seen)} unique sample rows')
```

Example, non-sensitive input:
```csv
sample_id,condition
EXAMPLE_A,control
EXAMPLE_B,treatment
```

This checks structure only. It does not validate study design or establish sufficient replication.
Add your data dictionary, input checksum, Python version and command to a README.

Primary reference: [Python environment tutorial](https://docs.python.org/3/tutorial/venv.html)

Training interest: https://angsumi.online/inquiry/?category=training


ANGSUMI · Version 2026-11-08 · Adapt this checklist to your project.
