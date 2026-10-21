import csv
from collections import Counter, defaultdict
from pathlib import Path

p = Path('processed/review_candidates_v2.csv')
if not p.exists():
    raise SystemExit(f'Missing {p}; run from legal_law_collector directory')
with p.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
print(f'TOTAL FLAGS: {len(rows)}')
print('\nREASONS (all laws):')
for reason, count in Counter(r['reason'] for r in rows).most_common():
    print(f'{count:>5}  {reason}')
print('\nBY LAW AND REASON:')
by_law = defaultdict(list)
for r in rows:
    by_law[r['document_id']].append(r)
for law in sorted(by_law):
    print(f'\n{law}: {len(by_law[law])} flags')
    for reason, count in Counter(r['reason'] for r in by_law[law]).most_common():
        print(f'  {count:>4} {reason}')
print('\nSAMPLES FROM PROBLEM LAWS (up to 3 per reason):')
for law in ['DIV_002','DIV_004','RENT_001','PROP_002','PROP_003','PROP_004','RENT_004']:
    group = by_law.get(law, [])
    if not group:
        continue
    print(f'\n=== {law} ===')
    seen = Counter()
    for r in group:
        if seen[r['reason']] >= 3:
            continue
        seen[r['reason']] += 1
        sample = ' '.join(r['sample'].split())[:150]
        print(f"p{r['page']} sec={r['section_number']!r} {r['reason']}: {sample}")
