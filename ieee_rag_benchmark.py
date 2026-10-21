"""Non-destructive evaluation of the current collector FAISS index.
Run from project root: python ieee_rag_benchmark.py
Optional reviewed gold CSV: legal_law_collector/processed/rag_gold_questions.csv
Columns: question,domain,relevant_chunk_ids (pipe-separated),reviewed
Only reviewed=yes/true/1 rows contribute to Recall@K and MRR.
"""
import csv, hashlib, json, statistics, time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'legal_law_collector' / 'processed'
CHUNKS = BASE / 'rag_chunks.jsonl'
INDEX = BASE / 'rag_index' / 'legal_pages.faiss'
META = BASE / 'rag_index' / 'metadata.json'
GOLD = BASE / 'rag_gold_questions.csv'
OUT = ROOT / 'IEEE_EVIDENCE' / 'current_rag'
OUT.mkdir(parents=True, exist_ok=True)

# Questions for retrieval demonstrations; NOT ground truth.
QUERIES = [
    ('rental','What are tenant rights concerning essential services under Maharashtra rental law?'),
    ('rental','Is registration required for a leave and licence agreement in Maharashtra?'),
    ('employment','What legal provisions govern payment of wages to employees?'),
    ('employment','What rules relate to occupational safety and working conditions?'),
    ('property','What duties does a promoter have under the Real Estate Regulation Act?'),
    ('property','What are the rules governing apartment ownership in Maharashtra?'),
    ('divorce','What are grounds for divorce under the Hindu Marriage Act?'),
    ('divorce','What is the jurisdiction of family courts in matrimonial matters?'),
]

def write_csv(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def main():
    import numpy as np
    import faiss
    from sentence_transformers import SentenceTransformer
    for path in (CHUNKS, INDEX, META):
        if not path.exists(): raise SystemExit(f'Missing {path}; no index will be rebuilt.')
    metadata=json.loads(META.read_text(encoding='utf-8'))
    actual_hash=hashlib.sha256(CHUNKS.read_bytes()).hexdigest()
    if actual_hash != metadata.get('chunks_sha256'):
        raise SystemExit('Chunk/index hash mismatch. Stopping without modifying files.')
    chunks=[json.loads(s) for s in CHUNKS.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
    index=faiss.read_index(str(INDEX))
    if index.ntotal != len(chunks): raise SystemExit('Index/chunk count mismatch; stopping.')
    chunk_ids={c['chunk_id'] for c in chunks}
    domain_counts=Counter(str(c.get('domain') or 'unknown').lower() for c in chunks)
    doc_counts=Counter(str(c.get('document_id') or 'unknown') for c in chunks)
    print('Loading embedding model once:', metadata['model'])
    model=SentenceTransformer(metadata['model'])
    questions=[{'question':q,'domain':d,'reviewed':'no','relevant_chunk_ids':''} for d,q in QUERIES]
    if not GOLD.exists():
        write_csv(GOLD, questions, ['question','domain','reviewed','relevant_chunk_ids'])
        print('Created question review template:', GOLD)
    else:
        with GOLD.open(encoding='utf-8-sig',newline='') as f: questions=list(csv.DictReader(f))
    rows=[]; retrievals=[]; scored=[]
    for n,q in enumerate(questions,1):
        question=(q.get('question') or '').strip()
        if not question: continue
        start=time.perf_counter()
        vec=np.asarray(model.encode([question],normalize_embeddings=True),dtype='float32')
        scores,indices=index.search(vec,min(5,index.ntotal))
        elapsed_ms=(time.perf_counter()-start)*1000
        domain=(q.get('domain') or '').strip().lower()
        ranked=[]
        for rank,(score,idx) in enumerate(zip(scores[0],indices[0]),1):
            if idx<0: continue
            c=chunks[int(idx)]; ranked.append(c['chunk_id'])
            retrievals.append({'question_id':n,'question':question,'requested_domain':domain,'rank':rank,'similarity':round(float(score),5),'retrieved_domain':c.get('domain'),'document_id':c.get('document_id'),'page':c.get('page'),'chunk_id':c['chunk_id'],'text_excerpt':c.get('text','')[:250], 'latency_ms':round(elapsed_ms,2)})
        reviewed=str(q.get('reviewed','')).strip().lower() in ('yes','true','1','y')
        gold=set(x.strip() for x in (q.get('relevant_chunk_ids') or '').replace(';','|').split('|') if x.strip())
        if reviewed and not gold: print(f'Warning: reviewed question {n} has no gold chunk IDs; excluded from scoring.')
        valid=reviewed and bool(gold) and gold.issubset(chunk_ids)
        if reviewed and gold and not gold.issubset(chunk_ids): print(f'Warning: unknown gold IDs for question {n}; excluded.')
        record={'question_id':n,'domain':domain,'question':question,'latency_ms':round(elapsed_ms,2),'top1_domain':chunks[int(indices[0][0])].get('domain') if indices[0][0]>=0 else '', 'reviewed_gold':valid, 'recall_at_1':'','recall_at_3':'','recall_at_5':'','reciprocal_rank':''}
        if valid:
            # Hit rate / query recall: any relevant chunk in top K.
            for k in (1,3,5): record[f'recall_at_{k}']=int(bool(set(ranked[:k]) & gold))
            record['reciprocal_rank']=next((1/rank for rank,cid in enumerate(ranked,1) if cid in gold),0.0)
            scored.append(record)
        rows.append(record)
    write_csv(OUT/'query_results.csv',rows,['question_id','domain','question','latency_ms','top1_domain','reviewed_gold','recall_at_1','recall_at_3','recall_at_5','reciprocal_rank'])
    write_csv(OUT/'retrieved_passages.csv',retrievals,['question_id','question','requested_domain','rank','similarity','retrieved_domain','document_id','page','chunk_id','text_excerpt','latency_ms'])
    domain_rows=[]
    for domain in sorted(set(r['domain'] for r in rows)):
        subset=[r for r in rows if r['domain']==domain]; valid=[r for r in scored if r['domain']==domain]
        domain_rows.append({'domain':domain,'questions_run':len(subset),'reviewed_questions':len(valid),'mean_latency_ms':round(statistics.mean(r['latency_ms'] for r in subset),2),'recall_at_1':round(statistics.mean(r['recall_at_1'] for r in valid),4) if valid else 'NOT_EVALUATED','recall_at_3':round(statistics.mean(r['recall_at_3'] for r in valid),4) if valid else 'NOT_EVALUATED','recall_at_5':round(statistics.mean(r['recall_at_5'] for r in valid),4) if valid else 'NOT_EVALUATED','mrr':round(statistics.mean(r['reciprocal_rank'] for r in valid),4) if valid else 'NOT_EVALUATED'})
    write_csv(OUT/'domain_metrics.csv',domain_rows,['domain','questions_run','reviewed_questions','mean_latency_ms','recall_at_1','recall_at_3','recall_at_5','mrr'])
    write_csv(OUT/'corpus_domain_counts.csv',[{'domain':d,'indexed_chunks':n} for d,n in sorted(domain_counts.items())],['domain','indexed_chunks'])
    write_csv(OUT/'corpus_document_counts.csv',[{'document_id':d,'indexed_chunks':n} for d,n in sorted(doc_counts.items())],['document_id','indexed_chunks'])
    summary={'index_vectors':int(index.ntotal),'embedding_dimensions':int(index.d),'model':metadata['model'],'documents':len(doc_counts),'domain_chunks':dict(domain_counts),'queries_run':len(rows),'reviewed_gold_queries':len(scored),'mean_latency_ms':round(statistics.mean(r['latency_ms'] for r in rows),2) if rows else None,'latency_includes_query_embedding':True,'legal_sources_verified':False,'metric_note':'Recall@K here means query-level hit rate (at least one gold passage in top K); only human-reviewed gold rows are scored.'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print('Saved:',OUT)
    print(json.dumps(summary,indent=2))
    if not scored: print('RECALL AND MRR NOT CALCULATED: review gold questions in',GOLD)
if __name__=='__main__': main()
