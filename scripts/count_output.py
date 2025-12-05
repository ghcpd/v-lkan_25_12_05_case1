#!/usr/bin/env python3
from pathlib import Path
out_dir = Path(__file__).resolve().parents[0] / '..' / 'output'
out_dir = out_dir.resolve()
results = []
for p in sorted(out_dir.glob('*.jsonl')):
    results.append((p.name, sum(1 for _ in p.open(encoding='utf-8'))))
for name, count in results:
    print(f"{name}: {count}")
