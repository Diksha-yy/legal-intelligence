"""Add to existing Streamlit app: from app.legal_updates.streamlit_panel import render_legal_updates; render_legal_updates()"""
import streamlit as st
from .core import reviews,search_approved

def render_legal_updates():
    st.subheader('Official Legal Updates · Review-Gated')
    st.caption('Content changes are NOT automatically legal amendments. Only approved versions enter the separate legal-update index.')
    records=reviews()
    if not records:
        st.info('No monitored versions yet. Register and fetch a source using the CLI.');return
    for r in records[:30]:
        with st.expander(f"{r['source_id']} · {r['status']} · {r['detected_at'][:10]}"):
            st.write('Title:',r['title']);st.write('Official URL:',r['url'])
            st.write('Domain:',r['domain'],'| Jurisdiction:',r['jurisdiction'])
            st.write('Law status:',r['law_status'] or 'Not verified')
            st.write('Effective date:',r['effective_date'] or 'Not verified')
            st.write('Reviewer:',r['reviewer'] or 'Pending')
            if r['diff_path']:
                from pathlib import Path
                p=Path(r['diff_path'])
                if p.exists(): st.code(p.read_text(encoding='utf-8')[:5000],language='diff')
    q=st.text_input('Search approved legal updates')
    if q and st.button('Search approved index'):
        try:
            for hit in search_approved(q):
                st.markdown(f"**{hit['source_title']}** — {hit['source_url']} · score {hit['score']:.3f}")
                st.write(hit['text'][:1000])
        except Exception as e:st.error(str(e))
