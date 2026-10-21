"""Collect CURRENT collector/RAG/M9 evidence for an IEEE audit, without uploading model weights or legal text."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from collections import Counter
import csv, json, sys, hashlib

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
out = Path.home() / 'IEEE_CURRENT_COLLECTOR_RAG_M9.zip'
patterns = [
    'legal_law_collector/**/*.py', 'legal_law_collector/*report.csv',
    'legal_law_collector/**/*report.csv', 'legal_law_collector/*updated.xlsx',
    'legal_law_collector/sources.xlsx',
    'app/modules/m8_rag/**/*.py', 'app/modules/m9_comparison/**/*.py',
    'evaluation/evaluate_m8.py', 'evaluation/evaluate_m9.py',
    'evaluation/run_all_evaluations.py',
]
exclude_parts = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'target', 'dist', 'build'}
found = {}
for pat in patterns:
    for p in root.glob(pat):
        if p.is_file() and not any(x in exclude_parts for x in p.relative_to(root).parts):
            if p.stat().st_size <= 3_000_000:
                found[str(p.relative_to(root)).replace('\\','/')] = p

report = {'project_root': str(root), 'included_files': sorted(found), 'evidence': {}, 'warnings': []}
# Count JSONL rows, IDs and domains without copying potentially copyrighted full legal text.
for p in root.glob('**/pages.jsonl'):
    if any(x in exclude_parts for x in p.relative_to(root).parts): continue
    counts, domains, n, malformed = Counter(), Counter(), 0, 0
    with p.open(encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if not line.strip(): continue
            n += 1
            try:
                rec = json.loads(line)
                counts[str(rec.get('document_id') or rec.get('law_id') or 'UNKNOWN')] += 1
                domains[str(rec.get('domain') or 'UNKNOWN')] += 1
            except (ValueError, TypeError): malformed += 1
    report['evidence'][str(p.relative_to(root))] = {'rows':n, 'by_document_id':dict(counts), 'by_domain':dict(domains), 'malformed_lines':malformed}

for p in root.glob('**/*.faiss'):
    if any(x in exclude_parts for x in p.relative_to(root).parts): continue
    info={'bytes':p.stat().st_size, 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    try:
        import faiss
        idx=faiss.read_index(str(p))
        info.update({'ntotal':int(idx.ntotal), 'dimension':int(idx.d), 'is_trained':bool(idx.is_trained)})
    except Exception as e:
        info['index_inspection']='Unavailable: '+str(e)[:200]
    report['evidence'][str(p.relative_to(root))]=info

for p in root.glob('**/legal_records.json'):
    if any(x in exclude_parts for x in p.relative_to(root).parts): continue
    try:
        obj=json.loads(p.read_text(encoding='utf-8'))
        records = obj if isinstance(obj,list) else next((v for v in obj.values() if isinstance(v,list)), [])
        report['evidence'][str(p.relative_to(root))]={'record_count':len(records), 'first_record_keys':sorted(records[0].keys()) if records and isinstance(records[0],dict) else []}
    except Exception as e: report['warnings'].append(f'{p}: {e}')

if not found: report['warnings'].append('No expected source files found; verify project root.')
with ZipFile(out,'w',ZIP_DEFLATED) as z:
    for rel,p in sorted(found.items()): z.write(p,rel)
    z.writestr('CURRENT_EVIDENCE_AUDIT.json', json.dumps(report,indent=2,ensure_ascii=False))
print('CREATED:',out)
print('SIZE_MB:',round(out.stat().st_size/1048576,2))
print('SOURCE_FILES:',len(found))
print('INDEX_OR_JSONL_RECORDS:',len(report['evidence']))
print('Review the ZIP before uploading: source files and manifests can contain private data or credentials.')
