import csv, json, re, random, pathlib, collections, html
BASE=pathlib.Path(__file__).resolve().parent
PROC=BASE/'legal_law_collector'/'processed'
SRC=PROC/'rag_chunks.jsonl'
OUT=PROC/'rag_source_first_review.csv'
HTML=PROC/'rag_source_first_review.html'
PAT=re.compile(r'(?im)(?:^|\n)\s*(?:section\s+)?(\d{1,3})\s*[.\-:]\s*([^\n]{15,130})')
BAD=re.compile(r'(?i)\b(contents|table of contents|index of sections|printed in india|price\s*:|government central press)\b')
QUESTION={
'rental':'Under {law}, what does section {sec} provide concerning {topic}?',
'employment':'What does section {sec} of {law} provide concerning {topic}?',
'property':'What does section {sec} of {law} provide concerning {topic}?',
'divorce':'What does section {sec} of {law} provide concerning {topic}?'}
LAW={
'RENT_001':'the Maharashtra Rent Control Act', 'RENT_002':'the Transfer of Property Act', 'RENT_003':'the Registration Act', 'RENT_004':'the Maharashtra Stamp Act',
'DIV_001':'the Hindu Marriage Act','DIV_002':'the Special Marriage Act','DIV_003':'the Family Courts Act','DIV_004':'the Hindu Adoptions and Maintenance Act',
'PROP_001':'the Real Estate (Regulation and Development) Act','PROP_002':'the Maharashtra Ownership Flats Act','PROP_003':'the Maharashtra Land Revenue Code','PROP_004':'the Maharashtra Apartment Ownership Act',
'EMP_001':'the Code on Wages','EMP_002':'the Industrial Relations Code','EMP_003':'the Code on Social Security','EMP_004':'the Occupational Safety, Health and Working Conditions Code'}
if not SRC.exists(): raise SystemExit('Missing '+str(SRC)+'; place this script in the project root.')
bydoc=collections.defaultdict(list)
with SRC.open(encoding='utf-8') as f:
 for line in f:
  if not line.strip():continue
  row=json.loads(line); t=' '.join(row.get('text','').split())
  if len(t)<250 or BAD.search(t[:350]) or row.get('page',0)<3:continue
  matches=list(PAT.finditer(row.get('text','')))
  if not matches:continue
  for m in matches:
   sec, topic=m.group(1), ' '.join(m.group(2).split())
   if len(topic)<20 or len(topic)>115 or topic.lower().startswith(('the following','provided that','notwithstanding')):continue
   if re.search(r'\.{3,}|\bpages\b',topic,re.I):continue
   bydoc[row['document_id']].append((row,sec,topic))
random.seed(20261020)
selected=[]
for doc in sorted(bydoc):
 candidates=bydoc[doc]; random.shuffle(candidates)
 used=set()
 for row,sec,topic in candidates:
  if sec in used:continue
  used.add(sec);selected.append((row,sec,topic))
  if len(used)==3:break
# 3 per document = up to 48; balance down to 10 per domain
bydomain=collections.defaultdict(list)
for x in selected:bydomain[x[0]['domain']].append(x)
selected=[]
for domain in ['rental','employment','property','divorce']:
 items=bydomain[domain];random.shuffle(items);selected.extend(items[:10])
rows=[]
for i,(r,sec,topic) in enumerate(selected,1):
 question=QUESTION[r['domain']].format(law=LAW.get(r['document_id'],r['document_id']),sec=sec,topic=topic.rstrip('.:;'))
 rows.append({'question':question,'domain':r['domain'],'reviewed':'no','relevant_chunk_ids':'','candidate_chunk_id':r['chunk_id'],'document_id':r['document_id'],'pdf_page':r['page'],'section_candidate':sec,'source_excerpt':r['text'][:1400],'review_instruction':'Verify that this passage really states section '+sec+' and answers the question; then copy candidate_chunk_id into relevant_chunk_ids and set reviewed=yes.'})
fields=list(rows[0]) if rows else []
if not rows:raise SystemExit('No suitable section headings found; inspect extraction quality and adjust heading regex.')
with OUT.open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
with HTML.open('w',encoding='utf-8') as f:
 f.write('<!doctype html><meta charset="utf-8"><title>RAG Source-first Review</title><style>body{font:16px Arial;max-width:1000px;margin:25px auto}article{padding:16px;margin:14px 0;border:1px solid #ccc;border-radius:9px}pre{white-space:pre-wrap;background:#f5f5f5;padding:12px}small{color:#555}</style><h1>40 Source-First RAG Candidate Questions</h1><p>Review the complete passage and section in the source PDF before approving. Candidate IDs are NOT validated labels. Edit the CSV in a spreadsheet, setting reviewed=yes and copying candidate_chunk_id to relevant_chunk_ids only when supported.</p>')
 for i,r in enumerate(rows,1):
  f.write(f'<article><h3>{i}. {html.escape(r["question"])}</h3><small>{html.escape(r["domain"])} | {html.escape(r["candidate_chunk_id"])} | PDF page {r["pdf_page"]}</small><pre>{html.escape(r["source_excerpt"])}</pre></article>')
print('Created',OUT,'and',HTML)
print('Candidate counts:',dict(collections.Counter(r['domain'] for r in rows)))
print('IMPORTANT: These are automatically generated candidates; approve manually before scoring.')
