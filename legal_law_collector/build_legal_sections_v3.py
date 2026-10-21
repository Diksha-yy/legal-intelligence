"""Experimental legal section candidate extractor V3. Python standard library only.
Run: python build_legal_sections_v3.py
Keeps original page text, never claims authoritative section boundaries.
"""
import csv, json, re
from pathlib import Path
from collections import defaultdict, Counter
BASE=Path(__file__).resolve().parent
OUT=BASE/'processed'
NUM=re.compile(r'^\s*(\d{1,3}(?:[A-Za-z]{1,2})?)\s*[.．]\s*(.*)$')
SUB=re.compile(r'^\(\s*1\s*\)\s*\S')
TITLE=re.compile(r'^(.{3,140}?)\s*[.。]?\s*[—–―]\s*(.*)$')
NOTES=re.compile(r'^(?:subs\.?|ins\.?|omitted|substituted|inserted|the words?|the expression|cl\.?|vide|see|for |act \d+ of \d{4}|these words|this indicates|the amendment)',re.I)
TOC=re.compile(r'\b(?:ARRANGEMENT OF SECTIONS|TABLE OF CONTENTS|CONTENTS|SECTIONS)\b',re.I)
START=re.compile(r'\b(?:short\s+title|definitions?|extent|application|this\s+act\s+may\s+be\s+called)\b',re.I)
END=re.compile(r'^\s*(?:THE\s+)?(?:FIRST|SECOND|THIRD|FOURTH|FIFTH)?\s*(?:SCHEDULE|ANNEXURE|APPENDIX)\b',re.I)

def key(n):
 m=re.fullmatch(r'(\d+)([A-Za-z]{0,2})',n)
 return (int(m.group(1)),m.group(2).upper()) if m else (9999,'')

def classify(line, nextline):
 m=NUM.match(line)
 if not m:return None
 num,rest=m.groups();rest=' '.join(rest.split())
 if not rest or len(rest)>320 or NOTES.match(rest):return None
 if SUB.match(rest):return (num,None,'subsection',0.88)
 t=TITLE.match(rest)
 if t and len(t.group(1))>2 and not NOTES.match(t.group(1)):
  return (num,t.group(1).strip(' .—–―'), 'title_dash',0.94)
 # '3. Definitions.―In this Act' can contain unusual PDF dash; handled above.
 if len(rest)<140 and SUB.match(nextline.strip()):return (num,rest.strip(' .—–―'),'title_nextline',0.76)
 # Plain headings with body, e.g. "1. Short title and extent. (1) ..."
 if START.search(rest[:80]) and ('.' in rest or len(rest)<100):return (num,rest.split('.')[0][:110],'opening_heading',0.65)
 return None

def is_toc(text):
 lines=[s.strip() for s in text.splitlines() if s.strip()]
 head=' '.join(lines[:16])
 if not TOC.search(head):return False
 if re.search(r'\b(?:it is hereby enacted|this act may be called)\b',head,re.I):return False
 numbered=sum(bool(NUM.match(s)) for s in lines)
 return numbered>=4 or bool(re.search(r'\b(?:CONTENTS|ARRANGEMENT OF SECTIONS)\b',head,re.I))

def main():
 inp=OUT/'pages.jsonl'
 if not inp.exists():raise SystemExit('Missing processed/pages.jsonl')
 docs=defaultdict(list)
 for line in inp.open(encoding='utf-8'):
  if line.strip():
   r=json.loads(line);docs[r['document_id']].append(r)
 sections=[];reports=[];reviews=[]
 for doc,pages in sorted(docs.items()):
  pages.sort(key=lambda x:int(x['page'])); flat=[]; skipped=0
  for p in pages:
   if is_toc(p.get('text') or ''):skipped+=1;continue
   for ln,s in enumerate((p.get('text') or '').splitlines(),1):
    flat.append({'page':int(p['page']),'line':ln,'text':s,'src':p})
  hits=[]
  for i,row in enumerate(flat):
   nxt=flat[i+1]['text'] if i+1<len(flat) and flat[i+1]['page']==row['page'] else ''
   h=classify(row['text'],nxt)
   if h:hits.append((i,*h))
  start=next((j for j,h in enumerate(hits) if key(h[1])[0]==1 and (h[3]=='subsection' or START.search(h[2] or ''))),None)
  if start is None:
   # Keep evidence of other candidate headings; do not silently discard.
   reviews.append(dict(document_id=doc,page='',section_number='',reason='section_one_not_found',sample='; '.join(flat[h[0]]['text'][:70] for h in hits[:3])))
   reports.append(dict(document_id=doc,pages=len(pages),toc_pages_skipped=skipped,raw_candidates=len(hits),accepted_sections=0,review_flags=1,first_section_page='',last_section_number='',status='needs_format_review'))
   continue
  hits=hits[start:];accepted=[];prev=(0,'');rejected=0
  for i,n,title,kind,score in hits:
   k=key(n)
   if k<=prev:
    rejected+=1
    continue
   gap=k[0]-prev[0]
   # Unlike V2, do not permanently reject genuine headings solely due to a numbering gap.
   # A huge gap still requires review and can be a footnote; retain it as candidate.
   if gap>1:
    reviews.append(dict(document_id=doc,page=flat[i]['page'],section_number=n,reason='number_gap_needs_review',sample=flat[i]['text'][:180]))
    score=min(score,0.65)
   accepted.append((i,n,title,kind,score));prev=k
  for j,(i,n,title,kind,score) in enumerate(accepted):
   end=accepted[j+1][0] if j+1<len(accepted) else len(flat)
   # Stop before explicit schedule heading in the final segment, if found.
   if j==len(accepted)-1:
    for z in range(i+1,end):
     if END.match(flat[z]['text']):end=z;break
   seg=flat[i:end]
   if not seg:continue
   content='\n'.join(r['text'] for r in seg).strip()
   flags=[]
   if score<0.75:flags.append('uncertain_heading_or_gap')
   if len(content)<70:flags.append('short_section')
   if len(content)>25000:flags.append('long_section_or_missed_boundary')
   if j==len(accepted)-1:flags.append('last_section_boundary_needs_review')
   # Amendment notes are metadata for review, not evidence of invalid sections.
   if re.search(r'\b(?:substituted by|inserted by|omitted by|amended by|subs\. by|ins\. by)\b',content,re.I):flags.append('editorial_amendment_notes_present')
   for reason in flags:
    reviews.append(dict(document_id=doc,page=flat[i]['page'],section_number=n,reason=reason,sample=flat[i]['text'][:180]))
   src=flat[i]['src']
   sections.append(dict(document_id=doc,law_id=src.get('law_id'),domain=src.get('domain'),jurisdiction=src.get('jurisdiction'),section_number=n,section_title_candidate=title,start_page=flat[i]['page'],end_page=seg[-1]['page'],start_line=flat[i]['line'],text=content,characters=len(content),heading_pattern=kind,confidence_score_heuristic=score,review_flags=flags,source_page_url=src.get('source_page_url'),sha256=src.get('sha256'),legal_status=src.get('legal_status','unknown'),verification_status='needs_review',full_section_text_verified=False,extraction_note='Unverified candidate: footnotes, headers and missed boundaries may remain.'))
  count=sum(r['document_id']==doc for r in reviews)
  reports.append(dict(document_id=doc,pages=len(pages),toc_pages_skipped=skipped,raw_candidates=len(hits),accepted_sections=len(accepted),review_flags=count,first_section_page=flat[accepted[0][0]]['page'] if accepted else '',last_section_number=accepted[-1][1] if accepted else '',status='needs_review',rejected_backward_or_duplicate=rejected))
 OUT.mkdir(exist_ok=True)
 with (OUT/'sections_v3.jsonl').open('w',encoding='utf-8') as f:
  for r in sections:f.write(json.dumps(r,ensure_ascii=False)+'\n')
 for name,rows,cols in [('section_report_v3.csv',reports,['document_id','pages','toc_pages_skipped','raw_candidates','accepted_sections','review_flags','first_section_page','last_section_number','status','rejected_backward_or_duplicate']),('review_candidates_v3.csv',reviews,['document_id','page','section_number','reason','sample'])]:
  with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)
 print('Documents:',len(reports),'| Candidates:',len(sections),'| Flags:',len(reviews))
 for r in reports:print(f"{r['document_id']}: {r['accepted_sections']} candidates, {r['review_flags']} flags, {r['status']}")
 print('Output: processed/sections_v3.jsonl, section_report_v3.csv, review_candidates_v3.csv')
 print('WARNING: candidate sections are not legally verified. Do not use as authoritative citations.')
if __name__=='__main__':main()
