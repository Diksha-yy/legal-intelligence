"""Measure real API wall-clock latency on PDFs; no invented speed claims.
Run: python -m evaluation.benchmark_api --pdf path/to/test.pdf --mode fast --runs 3
"""
import argparse,csv,time,statistics,hashlib
from pathlib import Path
import requests
p=argparse.ArgumentParser()
p.add_argument('--pdf',required=True);p.add_argument('--mode',choices=['fast','full'],default='fast')
p.add_argument('--runs',type=int,default=3);p.add_argument('--url',default='http://127.0.0.1:8000')
a=p.parse_args();pdf=Path(a.pdf).read_bytes()
if not pdf.startswith(b'%PDF-'):raise SystemExit('Not a PDF')
results=[]
for i in range(a.runs):
    start=time.perf_counter()
    if a.mode=='fast':
        r=requests.post(a.url+'/api/analyze-pdf',files={'file':(Path(a.pdf).name,pdf,'application/pdf')},timeout=300)
    else:
        r=requests.post(a.url+'/api/analyze-complete',params={'target_language':'Hindi'},files={'file':(Path(a.pdf).name,pdf,'application/pdf')},timeout=600)
    elapsed=time.perf_counter()-start
    r.raise_for_status();results.append({'run':i+1,'seconds':round(elapsed,3),'status':r.status_code})
    print(results[-1])
root=Path('evaluation/results');root.mkdir(parents=True,exist_ok=True)
out=root/f'api_benchmark_{a.mode}.csv'
with out.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['run','seconds','status']);w.writeheader();w.writerows(results)
print('Mean:',round(statistics.mean(x['seconds'] for x in results),3),'s; saved:',out)
print('Note: fast mode tests OCR+M2 endpoint, not M5-M7; full mode tests M1-M7. Run first request separately to isolate model cold start.')
