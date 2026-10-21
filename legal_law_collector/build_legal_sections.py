"""Conservative section candidate extractor for Legal Intelligence.
Run: python build_legal_sections.py
Inputs: processed/pages.jsonl, sources.csv or sources.xlsx (optional)
Outputs: processed/sections.jsonl, processed/section_report.csv, processed/review_candidates.csv

NOT a legal-text verifier. Ambiguous pages remain review-required.
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
PAGES = BASE / 'processed' / 'pages.jsonl'
OUT = BASE / 'processed'

# Require a title followed by a legal-style dash and provision text. This deliberately
# misses some real sections, but avoids many contents entries and numbered footnotes.
START = re.compile(r'^\s*(\d{1,3}[A-Z]?)\s*[.．]\s+(.{3,180}?)\s*[.\u2014\u2013-]\s*\u2014?\s*(\(\s*1\s*\)|This\s|The\s|In\s|Notwithstanding\s|Subject\s|For\s|Where\s|Every\s|No\s|Any\s|Save\s|It\s|There\s|Except\s|On\s|A\s|An\s|\[|\w+)', re.I)
# More permissive pattern, only used to report potentially missed headings.
POSSIBLE = re.compile(r'^\s*(\d{1,3}[A-Z]?)\s*[.]\s+[A-Z][^\n]{5,160}')
FOOTNOTE = re.compile(r'\b(Subs\.|Ins\.|Omitted|w\.e\.f\.|vide notification|Act \d+ of \d{4}|Sch\.|ibid\.)', re.I)
TOC = re.compile(r'\b(CONTENTS|ARRANGEMENT OF SECTIONS|LIST OF AMENDING ACTS|LIST OF ABBREVIATIONS|SECTIONS\.)\b', re.I)


def load_titles():
    titles = {}
    p = BASE / 'sources.csv'
    if p.exists():
        with p.open(encoding='utf-8-sig', newline='') as f:
            for r in csv.DictReader(f):
                titles[r.get('document_id', '')] = r.get('title', '')
    return titles


def looks_like_toc(page_text):
    top = '\n'.join(page_text.splitlines()[:22])
    return bool(TOC.search(top)) and ('CONTENTS' in top.upper() or 'ARRANGEMENT OF SECTIONS' in top.upper() or 'LIST OF AMENDING ACTS' in top.upper() or 'LIST OF ABBREVIATIONS' in top.upper())


def candidate(line):
    s = ' '.join(line.strip().split())
    if not s or len(s) > 270 or FOOTNOTE.search(s):
        return None
    m = START.match(s)
    if not m:
        return None
    num, heading = m.group(1), m.group(2).strip(' .-—–')
    if len(heading) > 105 or heading.lower().startswith(('the act has', 'subs', 'ins', 'omitted')):
        return None
    return num, heading


def main():
    if not PAGES.exists():
        raise SystemExit(f'Missing {PAGES}. Run: python collector.py --input sources.xlsx --extract')
    docs = defaultdict(list)
    with PAGES.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                docs[r['document_id']].append(r)
    titles = load_titles()
    OUT.mkdir(exist_ok=True)
    sections, reports, review = [], [], []
    for doc_id, pages in sorted(docs.items()):
        pages.sort(key=lambda r: int(r['page']))
        # Detect section starts only after the first substantive heading; avoid TOC pages.
        hits = []
        skipped_toc = 0
        possible_count = 0
        for p in pages:
            txt = p.get('text') or ''
            if looks_like_toc(txt):
                skipped_toc += 1
                continue
            for idx, line in enumerate(txt.splitlines()):
                if POSSIBLE.match(line):
                    possible_count += 1
                match = candidate(line)
                if match:
                    hits.append((int(p['page']), idx, match[0], match[1]))
        # Avoid picking numbered footnotes before the real first section.
        first_one = next((i for i, h in enumerate(hits) if h[2] == '1' and h[3].lower().startswith(('short title', 'definitions', 'application'))), None)
        if first_one is None:
            first_one = next((i for i, h in enumerate(hits) if h[2] == '1'), None)
        if first_one is not None:
            hits = hits[first_one:]
        else:
            hits = []
        # Keep increasing section numbers; repeated numbering / out-of-order starts
        # are ambiguous and are NOT silently treated as trusted section boundaries.
        accepted = []
        last = 0
        for h in hits:
            number = int(re.match(r'\d+', h[2]).group())
            if number < last or (number == last and not re.search('[A-Z]', h[2])):
                review.append({'document_id': doc_id, 'page': h[0], 'section_number': h[2], 'reason': 'non_increasing_number', 'heading_sample': h[3]})
                continue
            if number > last + 2 and last != 0:
                review.append({'document_id': doc_id, 'page': h[0], 'section_number': h[2], 'reason': 'number_gap', 'heading_sample': h[3]})
            accepted.append(h)
            last = max(last, number)
        # To prevent accidental mixing of footnotes with section text, store all
        # page text as an UNVERIFIED candidate; don't claim precise boundary text.
        page_map = {int(p['page']): p for p in pages}
        for i, (start_page, line_idx, number, heading) in enumerate(accepted):
            end_page = accepted[i+1][0] if i + 1 < len(accepted) else max(page_map)
            # When two sections share a page, page range overlaps intentionally.
            # The extracted text is limited to a page-level excerpt for manual review.
            source = page_map[start_page]
            lines = (source.get('text') or '').splitlines()
            excerpt = '\n'.join(lines[line_idx:line_idx+12])[:1500]
            sections.append({
                'document_id': doc_id, 'law_id': source.get('law_id'),
                'domain': source.get('domain'), 'jurisdiction': source.get('jurisdiction'),
                'title': titles.get(doc_id, ''), 'section_number': number,
                'section_title_candidate': heading, 'start_page': start_page,
                'end_page_candidate': end_page, 'start_line': line_idx,
                'preview_only': excerpt, 'full_section_text_extracted': False,
                'source_page_url': source.get('source_page_url'), 'sha256': source.get('sha256'),
                'legal_status': source.get('legal_status', 'unknown'),
                'verification_status': 'needs_review',
                'note': 'Candidate heading only. Page boundaries and full section text NOT verified.'
            })
        reports.append({
            'document_id': doc_id, 'pages': len(pages), 'toc_pages_skipped': skipped_toc,
            'possible_numbered_lines': possible_count, 'section_candidates': len(accepted),
            'flagged_candidates': sum(1 for r in review if r['document_id'] == doc_id),
            'first_section_page': accepted[0][0] if accepted else '',
            'last_section_candidate': accepted[-1][2] if accepted else '',
            'status': 'needs_review' if accepted else 'no_sections_detected'
        })
    with (OUT / 'sections.jsonl').open('w', encoding='utf-8') as f:
        for row in sections:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
    for filename, rows, columns in [
        ('section_report.csv', reports, ['document_id','pages','toc_pages_skipped','possible_numbered_lines','section_candidates','flagged_candidates','first_section_page','last_section_candidate','status']),
        ('review_candidates.csv', review, ['document_id','page','section_number','reason','heading_sample'])
    ]:
        with (OUT / filename).open('w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
    print('Documents:', len(reports), '| Candidate headings:', len(sections), '| Review flags:', len(review))
    print('Report:', OUT / 'section_report.csv')
    print('Candidates:', OUT / 'sections.jsonl')
    print('Review:', OUT / 'review_candidates.csv')
    print('IMPORTANT: These are unverified heading candidates, NOT complete legal sections.')

if __name__ == '__main__':
    main()
