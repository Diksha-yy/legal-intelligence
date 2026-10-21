"""Compare keyword, semantic, hybrid M2 on identical test clauses.
Run from project root: python -m evaluation.evaluate_m2_comparison
Data: evaluation/m2_test.csv columns clause,actual_label, optional domain.
NOTE: Existing 40 examples are synthetic, employment-only, and not independently verified.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import csv
import json
import time
from collections import Counter
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from app.modules.m2_classification.classifier import classify_clause
from app.modules.m2_classification.semantic_classifier import classify_clause_semantic
from app.modules.m2_classification.hybrid_classifier import classify_clause_hybrid

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'evaluation' / 'm2_test.csv'
OUT = ROOT / 'evaluation' / 'results'
OUT.mkdir(parents=True, exist_ok=True)
with DATA.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
rows = [r for r in rows if r.get('clause','').strip() and r.get('actual_label','').strip()]
if not rows: raise SystemExit('No labelled test clauses found.')
labels = sorted({r['actual_label'].strip() for r in rows})
true = [r['actual_label'].strip() for r in rows]
methods = {
    'keyword': lambda s,d: classify_clause(s),
    'semantic': lambda s,d: classify_clause_semantic(s, domain=d),
    'hybrid': lambda s,d: classify_clause_hybrid(s, domain=d),
}
summary=[]
prediction_rows=[]
for name, fn in methods.items():
    preds=[]; failures=0
    start=time.perf_counter()
    for row in rows:
        domain = (row.get('domain') or 'employment').strip().lower()
        if name=='keyword' and domain!='employment':
            preds.append('NOT_SUPPORTED'); failures+=1; continue
        try:
            prediction=fn(row['clause'],domain)
            preds.append(str(prediction.get('category','Unclassified')))
        except Exception as e:
            preds.append('ERROR');failures+=1
            print(f'{name} failed on row {len(preds)}: {type(e).__name__}: {e}')
    seconds=time.perf_counter()-start
    p,r,f1,_=precision_recall_fscore_support(true,preds,labels=labels,average='macro',zero_division=0)
    record={'model':name,'samples':len(rows),'accuracy':round(accuracy_score(true,preds),4),
            'macro_precision':round(float(p),4),'macro_recall':round(float(r),4),
            'macro_f1':round(float(f1),4),'total_seconds':round(seconds,3),
            'mean_ms_per_clause':round(seconds*1000/len(rows),2),'errors_or_unsupported':failures,
            'test_scope':'synthetic employment-only unless CSV independently expanded/reviewed'}
    summary.append(record)
    all_labels=labels+sorted(set(preds)-set(labels))
    matrix=confusion_matrix(true,preds,labels=all_labels)
    with (OUT/f'm2_{name}_confusion.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['gold\\pred']+all_labels)
        for label,values in zip(all_labels,matrix):w.writerow([label]+list(values))
    for row,pred in zip(rows,preds):
        prediction_rows.append({'model':name,'domain':row.get('domain','employment'),
                                'clause':row['clause'],'actual_label':row['actual_label'],
                                'predicted_label':pred,'correct':int(row['actual_label']==pred)})
with (OUT/'m2_model_comparison.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
with (OUT/'m2_model_predictions.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(prediction_rows[0]));w.writeheader();w.writerows(prediction_rows)
print(json.dumps(summary,indent=2,ensure_ascii=False))
print('Saved:',OUT/'m2_model_comparison.csv')
print('WARNING: Synthetic employment-only scores are not four-domain or production accuracy.')
