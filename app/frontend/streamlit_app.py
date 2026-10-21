"""Legal Intelligence review dashboard: fast on-demand analysis and opt-in local history.
Run: python -m streamlit run app/frontend/streamlit_app.py
"""
import hashlib
import html
import re
import json
import os
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import requests
import streamlit as st

API = os.getenv('LEGAL_AI_API', 'http://127.0.0.1:8000').rstrip('/')
DB = Path('data/review_dashboard/history.sqlite3')
DOMAIN_OPTIONS = ['Auto detect', 'employment', 'rental', 'property', 'divorce']

st.set_page_config(page_title='Legal Saathi | Legal Intelligence', page_icon='⚖️', layout='wide', initial_sidebar_state='expanded')
st.markdown("""<style>
.block-container{padding-top:1.4rem;max-width:1320px}
[data-testid="stMetric"]{background:#f5f8ff;border:1px solid #dbe5f5;padding:16px;border-radius:15px}
.hero{background:linear-gradient(120deg,#0d2546,#164c78 65%,#147c86);color:white;padding:32px;border-radius:20px;margin-bottom:20px;box-shadow:0 12px 30px #0c345020}
.hero h1{color:white;margin:0;font-size:2.3rem}.hero p{margin:8px 0 0;color:#e1f1fc}
.note{background:#eef8ff;border-left:4px solid #1a7fba;border-radius:8px;padding:12px;margin:12px 0}
.small{font-size:.9rem;color:#516477}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>⚖️ Legal Saathi <span style="font-size:1.1rem;opacity:.8">| Legal Intelligence</span></h1><p>Understand your legal documents without reading every page. Short summaries • Possible missing clauses • Risk flags • English / हिंदी / मराठी</p></div>',unsafe_allow_html=True)


def request_json(method, route, **kwargs):
    response = requests.request(method, f'{API}{route}', timeout=kwargs.pop('timeout', 90), **kwargs)
    response.raise_for_status()
    return response.json()


def db_connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB, timeout=10)
    con.execute('''CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL, filename TEXT NOT NULL, file_hash TEXT NOT NULL,
        mode TEXT NOT NULL, domain TEXT NOT NULL, duration REAL NOT NULL,
        result_json TEXT NOT NULL)''')
    con.commit()
    return con


def save_history(filename, digest, mode, result, seconds):
    with db_connect() as con:
        con.execute('''INSERT INTO analyses (created_at, filename, file_hash, mode, domain, duration, result_json)
            VALUES (?,?,?,?,?,?,?)''', (datetime.now(timezone.utc).isoformat(timespec='seconds'), filename,
            digest, mode, str(result.get('document_type','unknown')), round(seconds,2),
            json.dumps(result, ensure_ascii=False, default=str)))
        con.commit()


def load_history():
    with db_connect() as con:
        return con.execute('''SELECT id,created_at,filename,mode,domain,duration
                              FROM analyses ORDER BY id DESC LIMIT 100''').fetchall()


def show_error(error):
    st.error(f'Unable to complete request: {error}')
    if isinstance(error, requests.HTTPError) and error.response is not None:
        st.code(error.response.text[:1600])


def fast_analysis(pdf_bytes, filename, chosen_domain):
    ocr = request_json('POST','/api/ai/extract', files={'file':(filename,pdf_bytes,'application/pdf')}, timeout=150)
    text = ocr.get('full_text','')
    if not text.strip():
        raise ValueError('No readable text found. Try a text-based PDF or check OCR setup.')
    selected = None if chosen_domain == 'Auto detect' else chosen_domain
    classification = request_json('POST','/api/m2/analyze', json={'text':text,'domain':selected},timeout=150)
    classification = classification.get('result',classification)
    domain = classification.get('domain') or selected or 'unknown'
    result = {'status':'success','mode':'Fast review','document_type':domain,
              'ocr':{'filename':filename,'page_count':ocr.get('page_count'), 'text_length':len(text)},
              'classification':classification}
    # Rule-based screening runs in parallel; errors are shown rather than hiding the entire result.
    if domain in ('employment','rental','property','divorce'):
        routes = {'missing_clauses':'/api/ai/missing-clauses','risk_analysis':'/api/ai/risk','fairness_analysis':'/api/ai/fairness'}
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {key:pool.submit(request_json,'POST',route,json={'text':text,'document_type':domain},timeout=45)
                       for key,route in routes.items()}
            for key,future in futures.items():
                try: result[key] = future.result()
                except Exception as exc: result[key] = {'warning':str(exc)}
    else:
        result['warning'] = 'Unsupported or uncertain category: manual review needed.'
    return result


def detailed_analysis(pdf_bytes, filename, chosen_domain, language):
    params = {'target_language':language}
    if chosen_domain != 'Auto detect': params['document_type'] = chosen_domain
    result = request_json('POST','/api/analyze-complete', params=params,
                          files={'file':(filename,pdf_bytes,'application/pdf')},timeout=360)
    result['mode']='Full analysis'
    return result


def plain_summary(data):
    "Fallback extractive overview; does not pretend to be an abstractive AI summary."
    val=data.get('summary')
    if isinstance(val,dict):
        val=val.get('summary') or val.get('summary_text') or val.get('text')
    if isinstance(val,str) and val.strip(): return val.strip(), 'AI-generated summary'
    cls=data.get('classification') or {}
    if isinstance(cls,dict): cls=cls.get('result',cls)
    clauses=cls.get('clauses',[]) if isinstance(cls,dict) else []
    snippets=[]
    for c in clauses:
        if not isinstance(c,dict):continue
        t=c.get('text') or c.get('clause') or c.get('clause_text') or ''
        if t:
            t=re.sub(r'\s+',' ',str(t)).strip()
            if len(t)>220:t=t[:217]+'…'
            if t not in snippets:snippets.append(t)
        if len(snippets)>=4:break
    return (' '.join(snippets) if snippets else 'No short summary is available in Fast Review. Choose Full Analysis for an AI-generated summary.'), 'Quick clause preview (not an AI summary)'


def format_findings(value):
    if value is None:return ['Not available for this analysis.']
    if isinstance(value,str):return [value]
    if isinstance(value,list):return [str(x) if not isinstance(x,dict) else '; '.join(f'{k}: {v}' for k,v in x.items()) for x in value[:25]]
    if isinstance(value,dict):
        lines=[]
        for key,v in value.items():
            if key in ('text','full_text','raw_text'):continue
            if isinstance(v,list):
                if v:
                    lines.append(key.replace('_',' ').title()+':')
                    lines.extend('• '+str(x)[:350] for x in v[:15])
            elif isinstance(v,(str,int,float,bool)):
                lines.append(key.replace('_',' ').title()+': '+str(v)[:300])
        return lines or ['No findings returned.']
    return [str(value)]


def html_report(data):
    "Self-contained printable HTML report, with Unicode supported by browser fonts."
    esc=lambda x:html.escape(str(x),quote=True)
    summ,kind=plain_summary(data)
    fields=[('Plain-language overview',kind+'\n'+summ),('Translated overview',data.get('translated_summary') or 'Not generated'),
            ('Potential missing clauses',data.get('missing_clauses')),('Risk screening',data.get('risk_analysis')),
            ('Fairness indicators',data.get('fairness_analysis'))]
    sections=''.join('<section><h2>'+esc(title)+'</h2><pre>'+esc('\n'.join(format_findings(value)) if isinstance(value,(dict,list)) else value)+'</pre></section>' for title,value in fields)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Legal Saathi Analysis Report</title>
    <style>body{{font:15px/1.6 Arial,sans-serif;max-width:850px;margin:35px auto;color:#18344c;padding:0 20px}}
    h1{{color:#14577d}}h2{{color:#236b91;font-size:19px}}section{{padding:12px 18px;border:1px solid #dae5ec;border-radius:12px;margin:15px 0}}
    pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}}.disclaimer{{background:#fff6df;padding:14px;border-radius:8px}}</style></head><body>
    <h1>⚖️ Legal Saathi — Document Review</h1><p><b>Document:</b> {esc((data.get('ocr') or {}).get('filename','Uploaded PDF'))}<br>
    <b>Category:</b> {esc(data.get('document_type','Unknown'))}<br><b>Analysis mode:</b> {esc(data.get('mode',''))}</p>
    {sections}<p class="disclaimer"><b>Important:</b> Automated preliminary screening, not legal advice. Missing-clause and law-compliance flags are not verified legal conclusions. Check current official law and consult a qualified professional for important decisions.</p>
    <p>Open this HTML file in a browser and select Print → Save as PDF to create a PDF report.</p></body></html>'''


def cached_result(digest,mode,domain,language):
    "Reuse a previous opt-in saved analysis of the same PDF and settings."
    with db_connect() as con:
        for (blob,) in con.execute('SELECT result_json FROM analyses WHERE file_hash=? ORDER BY id DESC LIMIT 20',(digest,)):
            try:
                item=json.loads(blob)
                if item.get('mode')==mode and item.get('_selected_domain')==domain and item.get('_language')==language:
                    return item
            except (ValueError,TypeError):pass
    return None


def show_result(data):
    ocr = data.get('ocr') or {}
    cls = data.get('classification') or {}
    if 'result' in cls and isinstance(cls['result'],dict): cls=cls['result']
    a,b,c,d=st.columns(4)
    a.metric('Category',str(data.get('document_type','Unknown')).title())
    b.metric('Pages',ocr.get('page_count','—'))
    c.metric('Clauses',cls.get('total_clauses','—'))
    d.metric('Processing time',f"{data.get('_seconds',0):.1f} s" if '_seconds' in data else '—')
    st.caption('Automated screening only. Review the source PDF and applicable law before relying on findings.')
    if data.get('warning'): st.warning(data['warning'])
    overview,overview_kind=plain_summary(data)
    st.subheader('✨ Understand your document in a minute')
    st.caption(overview_kind)
    st.info(overview)
    translated=data.get('translated_summary')
    if isinstance(translated,dict):translated=translated.get('translated_text') or translated.get('translation') or str(translated)
    if translated:
        st.subheader('🌐 आपकी भाषा में / तुमच्या भाषेत')
        st.success(str(translated))
    else:
        st.caption('For Hindi or Marathi summary, select Full Analysis and the target language.')
    st.markdown('<div class="note">🧭 <b>What next?</b> Read the potential missing clauses and risk flags below. They are screening suggestions, not a legal-compliance certificate. Verify current applicable law and seek professional review for important decisions.</div>',unsafe_allow_html=True)
    with st.expander('📌 Classified clauses',expanded=True):
        clauses=cls.get('clauses',[])
        if clauses:
            st.caption(f'{len(clauses)} clauses identified. Labels are automated predictions.')
            for idx,item in enumerate(clauses[:40],1):
                if isinstance(item,dict):
                    label=item.get('category') or item.get('label') or item.get('classification') or 'Unclassified'
                    content=item.get('clause') or item.get('text') or item.get('clause_text') or ''
                    st.markdown(f'**{idx}. {label}**')
                    if content: st.write(str(content)[:700])
                    else: st.json(item)
                else: st.write(f'{idx}. {item}')
            if len(clauses)>40: st.caption(f'Showing first 40 of {len(clauses)} clauses.')
        else: st.json(cls)
    left,right=st.columns(2)
    with left:
        with st.expander('⚠️ Risk screening',expanded=True):
            for line in format_findings(data.get('risk_analysis')): st.write(line)
        with st.expander('🧩 Potential missing clauses',expanded=True):
            for line in format_findings(data.get('missing_clauses')): st.write(line)
    with right:
        with st.expander('⚖️ Fairness indicators',expanded=True):
            for line in format_findings(data.get('fairness_analysis')): st.write(line)
        with st.expander('🔬 Full machine-readable output'): st.json(data)
    st.download_button('📄 Download readable report (HTML → Print to PDF)',html_report(data),
                       file_name='legal_saathi_report.html',mime='text/html',use_container_width=True)
    st.download_button('⬇️ Download analysis report (JSON)',json.dumps(data,indent=2,ensure_ascii=False,default=str),
                       file_name='legal_intelligence_analysis.json',mime='application/json',use_container_width=True)


with st.sidebar:
    st.header('Review controls')
    try:
        request_json('GET','/health',timeout=3)
        st.success('AI API connected')
    except Exception:
        st.error('AI API offline. Start FastAPI on port 8000.')
    st.caption('Fast Review: quick clause preview, missing-clause, risk and fairness screening. Full Analysis: BART summary + Hindi/Marathi translation. Saved history can be reopened without reprocessing.')
    st.info('M8 legal search and M9 comparison are separate on-demand tools; they are not run for every uploaded PDF.')

t1,t2,t3,t4,t5=st.tabs(['📄 Understand my PDF','🗂️ My document history','📚 Current-law references (M8)','🔄 Compare two PDFs (M9)','📊 Research results'])
with t1:
    c1,c2=st.columns([2,1])
    with c1: pdf=st.file_uploader('Upload a PDF document',type=['pdf'],key='pdf')
    with c2: domain=st.selectbox('Document category',DOMAIN_OPTIONS)
    st.caption('Step 1: Upload PDF  →  Step 2: Select category and language  →  Step 3: Read summary, warnings and download report')
    mode=st.radio('Analysis mode',['⚡ Fast review (M1, M2, M5–M7)','🧠 Full analysis (M1–M7)'],horizontal=True)
    language=st.selectbox('Translation language for full analysis',['Hindi','Marathi','English']) if 'Full' in mode else 'English'
    store=st.checkbox('Save analysis to local history (includes extracted findings; do not use for confidential PDFs without permission)',value=False)
    reuse=st.checkbox('⚡ Reuse saved result for identical PDF and settings (if available)',value=True)
    if st.button('▶ Analyze document',type='primary',disabled=pdf is None,use_container_width=True):
        raw=pdf.getvalue()
        if len(raw)>20*1024*1024: st.error('File too large. Use a PDF under 20 MB.')
        else:
            start=time.perf_counter()
            with st.spinner('Analyzing… first run may take longer while models load'):
                try:
                    digest=hashlib.sha256(raw).hexdigest()
                    mode_name='Fast review' if 'Fast' in mode else 'Full analysis'
                    result=cached_result(digest,mode_name,domain,language) if reuse else None
                    reused=result is not None
                    if result is None:
                        if 'Fast' in mode: result=fast_analysis(raw,pdf.name,domain)
                        else: result=detailed_analysis(raw,pdf.name,domain,language)
                        result['_seconds']=round(time.perf_counter()-start,2)
                        result['_file_sha256']=digest
                        result['_selected_domain']=domain
                        result['_language']=language
                    st.session_state['last_result']=result
                    if store and not reused: save_history(pdf.name,digest,result['mode'],result,result['_seconds'])
                    st.success('Loaded saved result instantly' if reused else 'Analysis completed')
                except Exception as exc: show_error(exc)
    if st.session_state.get('last_result'): show_result(st.session_state['last_result'])

with t2:
    st.subheader('Saved analyses (local SQLite)')
    st.caption('History is opt-in. Database: data/review_dashboard/history.sqlite3. No cloud account or external database required.')
    try:
        rows=load_history()
        if rows:
            import pandas as pd
            st.dataframe(pd.DataFrame(rows,columns=['ID','UTC timestamp','PDF filename','Mode','Category','Seconds']),hide_index=True,use_container_width=True)
            selected=st.selectbox('View saved result',[r[0] for r in rows])
            with db_connect() as con:
                record=con.execute('SELECT result_json FROM analyses WHERE id=?',(selected,)).fetchone()
            if record: show_result(json.loads(record[0]))
            if st.button('Delete ALL saved history',type='secondary'):
                with db_connect() as con:
                    con.execute('DELETE FROM analyses');con.commit()
                st.success('History deleted. Refresh the page.')
        else: st.info('No saved analyses yet. Check “Save analysis” during upload to store a record.')
    except Exception as exc: show_error(exc)

with t3:
    st.subheader('Search indexed legal knowledge')
    st.warning('Law search retrieves previously indexed passages. It does NOT guarantee the latest law or verify compliance. Check source date, official text and jurisdiction.')
    st.caption('Retrieves evidence passages, not a verified legal opinion. Indexed sources and effective dates must be reviewed.')
    query=st.text_input('Question','What are the duties of a promoter under Section 11?')
    kb_domain=st.selectbox('Filter by category',['property','employment','rental','divorce','All'],key='kb_domain')
    if st.button('🔎 Search knowledge'):
        try:
            payload={'question':query,'top_k':5,'jurisdiction':'India'}
            if kb_domain!='All':payload['domain']=kb_domain
            out=request_json('POST','/api/legal-knowledge/search',json=payload,timeout=90)
            results=out.get('results',[]) if isinstance(out,dict) else []
            st.metric('Retrieved passages',len(results))
            for i,item in enumerate(results,1):
                with st.expander(f"{i}. {item.get('title','Legal source')} | score: {item.get('similarity',item.get('score','—'))}",expanded=i==1):
                    st.write(item.get('text',''))
                    st.caption(f"Source: {item.get('source_url','not recorded')} | Verification: {item.get('verification_status','not confirmed')}")
            if not results: st.info('No matching passages. Index official legal PDFs first.')
        except Exception as exc:show_error(exc)

with t4:
    st.subheader('Compare original and revised agreements')
    a,b=st.columns(2)
    with a: first=st.file_uploader('Original agreement',type=['pdf'],key='original')
    with b: second=st.file_uploader('Revised agreement',type=['pdf'],key='revised')
    if st.button('🔄 Detect changes',disabled=not(first and second),type='primary'):
        with st.spinner('Comparing agreements…'):
            try:
                out=request_json('POST','/api/ai/compare',files={'file1':(first.name,first.getvalue(),'application/pdf'),
                    'file2':(second.name,second.getvalue(),'application/pdf')},timeout=180)
                x,y,z=st.columns(3)
                x.metric('Changed',len(out.get('changed_clauses',[])))
                y.metric('Removed',len(out.get('missing_from_document2',[])))
                z.metric('Added',len(out.get('missing_from_document1',[])))
                st.subheader('Changed clauses')
                for i,change in enumerate(out.get('changed_clauses',[]),1):
                    with st.expander(f'Change {i}',expanded=i<=2):
                        st.markdown('**Original**');st.write(change.get('document1_clause',''))
                        st.markdown('**Revised**');st.write(change.get('document2_clause',''))
                with st.expander('Full comparison output'):st.json(out)
            except Exception as exc:show_error(exc)

with t5:
    st.subheader('Research evaluation — measured results only')
    st.warning('These metrics are from limited development tests, not verified real-world accuracy or a comparison with commercial websites.')
    import pandas as pd
    metrics=[
        {'Module':'M1 OCR','Metric':'CER / WER','Reported result':'0 / 0','Test scope':'1 synthetic PDF'},
        {'Module':'M2 keyword classifier','Metric':'Accuracy / Macro-F1','Reported result':'82.50% / 84.05%','Test scope':'40 synthetic employment clauses'},
        {'Module':'M3 BART','Metric':'ROUGE-1 / ROUGE-L F1','Reported result':'52.63% / 35.09%','Test scope':'1 reference summary'},
        {'Module':'M4 NLLB Hindi','Metric':'BLEU / chrF++','Reported result':'8.70 / 48.32','Test scope':'1 illustrative translation'},
        {'Module':'M4 NLLB Marathi','Metric':'BLEU / chrF++','Reported result':'12.40 / 56.69','Test scope':'1 illustrative translation'},
        {'Module':'M5 Missing clauses','Metric':'F1','Reported result':'100%','Test scope':'1 rule-based test'},
        {'Module':'M6 Risk','Metric':'Reference score','Reported result':'25 / 25','Test scope':'1 rule-based test'},
        {'Module':'M7 Fairness','Metric':'F1','Reported result':'100% (audit needed)','Test scope':'Inconsistent indicator counts'},
        {'Module':'M8 QA','Metric':'Answer support','Reported result':'5 / 5','Test scope':'5 questions, 1 chunk'},
        {'Module':'M9 Comparison','Metric':'Expected changes detected','Reported result':'0 / 2 (before patch)','Test scope':'1 development comparison'},
    ]
    st.dataframe(pd.DataFrame(metrics),hide_index=True,use_container_width=True)
    matrix=Path('evaluation/m2_confusion_matrix.csv')
    if matrix.exists():
        try:
            cm=pd.read_csv(matrix,index_col=0)
            st.subheader('M2 confusion matrix (keyword baseline)')
            st.dataframe(cm,use_container_width=True)
            st.caption('Use the same held-out labelled dataset to evaluate hybrid M2 before claiming improvement.')
        except Exception as exc:st.warning(f'Could not load confusion matrix: {exc}')
    st.download_button('⬇️ Download paper metrics (CSV)',pd.DataFrame(metrics).to_csv(index=False),
                       'legal_intelligence_reported_metrics.csv','text/csv')
