"""Live four-domain API smoke test and latency report; NOT a classification benchmark."""
import argparse, csv, json, statistics, time
from pathlib import Path
import requests

DOMAINS = ('employment','rental','property','divorce')
ALIASES = {'divorce_family':'divorce', 'job_offer':'employment'}

def norm(x):
    return ALIASES.get(str(x or '').strip().lower(), str(x or '').strip().lower())

def run(base, paths, mode, language, timeout):
    out = Path('evaluation/results/four_pdf_review')
    out.mkdir(parents=True, exist_ok=True)
    rows=[]
    endpoint = '/api/analyze-pdf' if mode == 'fast' else '/api/analyze-complete'
    for expected, path in zip(DOMAINS, paths):
        record={'expected_domain':expected,'file':str(path),'mode':mode,'language':language}
        start=time.perf_counter()
        try:
            if not path.is_file():
                raise FileNotFoundError(f'PDF not found: {path}')
            with path.open('rb') as f:
                kw={'files':{'file':(path.name,f,'application/pdf')}, 'timeout':timeout}
                if mode == 'full':
                    kw['params']={'target_language':language, 'document_type':expected}
                response=requests.post(base.rstrip('/')+endpoint,**kw)
            record['http_status']=response.status_code
            response.raise_for_status()
            result=response.json()
            (out/f'{expected}_{mode}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
            detected=norm(result.get('document_type') or result.get('classification',{}).get('domain'))
            record.update(detected_domain=detected,domain_match=(detected==expected),
                          page_count=(result.get('ocr') or {}).get('page_count'),
                          text_length=(result.get('ocr') or {}).get('text_length'),
                          has_summary=bool(result.get('summary')),
                          has_translation=bool(result.get('translated_summary')),
                          status='ok')
        except Exception as e:
            record.update(status='error',error=str(e)[:400])
        record['seconds']=round(time.perf_counter()-start,3)
        rows.append(record)
        print(f"{expected:11} {record['status']:5} {record['seconds']:7.2f}s detected={record.get('detected_domain','-')} http={record.get('http_status','-')}")
    columns=['expected_domain','file','mode','language','status','http_status','detected_domain','domain_match','page_count','text_length','has_summary','has_translation','seconds','error']
    with (out/f'{mode}_results.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader();writer.writerows(rows)
    passed=[r for r in rows if r['status']=='ok']
    print(f'Completed: {len(passed)}/4. Raw records: {out.resolve()}')
    print('Domain match on these 4 documents:',sum(r.get('domain_match',False) for r in passed),'/4 (smoke test, NOT model accuracy)')
    if passed: print('Mean latency of successful requests:',round(statistics.mean(r['seconds'] for r in passed),2),'s')
    if mode=='full': print('NOTE: The provided domain is a hint; full-mode domain_match does not independently validate automatic domain detection.')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for domain in DOMAINS: p.add_argument('--'+domain,required=True,type=Path)
    p.add_argument('--mode',choices=['fast','full'],default='fast')
    p.add_argument('--language',choices=['Hindi','Marathi','English'],default='Hindi')
    p.add_argument('--base',default='http://127.0.0.1:8000')
    p.add_argument('--timeout',type=int,default=240)
    a=p.parse_args()
    run(a.base,[getattr(a,d) for d in DOMAINS],a.mode,a.language,a.timeout)
