"""Legal Intelligence: conservative multi-format section extraction (V2).
Run in the same directory as processed/pages.jsonl: python build_legal_sections_v2.py
Outputs are CANDIDATES, not legally verified sections. No third-party packages.
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / 'processed'
INPUT = OUT / 'pages.jsonl'
# Actual legal provisions: numbered title + dash; numbered subsection; or no-space title.
NUM = re.compile(r'^\s*(\d{1,3}(?:[A-Za-z]{1,2})?)\s*[.．]\s*(.*)$')
SUB = re.compile(r'^\s*\(\s*1\s*\)\s*\S')
TITLE_BODY = re.compile(r'^(?P<title>.{3,115}?)\s*[.。]\s*[—–-]\s*(?P<body>\S.*)$')
DASH_BODY = re.compile(r'^(?P<title>.{3,115}?)\s*[—–]\s*(?P<body>\S.*)$')
TOC = re.compile(r'\b(CONTENTS|ARRANGEMENT OF SECTIONS|LIST OF AMENDING ACTS|LIST OF ABBREVIATIONS)\b', re.I)
NOTE = re.compile(r'^(?:Subs\.?|Ins\.?|Omitted|Cl\.?|The words|The word|The Act has|Inserted|Substituted|For |See |Vide |Act \d+ of \d{4}|The Jan Viswas|The Hindu Marriage \(Amendment\))\b', re.I)
NOTE_DETAIL = re.compile(r'\b(?:w\.?e\.?f\.?|ibid\.?|vide notification|substituted by|omitted by|inserted by|Act \d+ of \d{4})\b', re.I)
HEADING = re.compile(r'^(?:CHAPTER|PART|SCHEDULE|PREAMBLE|SECTIONS|INDIACODE)\b', re.I)
FIRST = re.compile(r'^(?:short\s+title|definitions?|application|extent|preliminary|this\s+act\s+may\s+be\s+called)', re.I)


def load_titles():
    p = BASE / 'sources.csv'
    if p.exists():
        with p.open(encoding='utf-8-sig', newline='') as f:
            return {r['document_id']: r.get('title', '') for r in csv.DictReader(f)}
    p = BASE / 'sources.xlsx'
    if p.exists():
        try:
            from openpyxl import load_workbook
            ws = load_workbook(p, read_only=True, data_only=True).active
            rows = ws.iter_rows(values_only=True)
            cols = [str(c or '') for c in next(rows)]
            return {str(dict(zip(cols, row)).get('document_id')): str(dict(zip(cols, row)).get('title') or '') for row in rows}
        except ImportError:
            pass
    return {}


def toc_page(text):
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    head = ' '.join(lines[:18])
    # Only skip explicit front matter, not all pages containing the word 'sections'.
    return bool(TOC.search(head)) and not bool(re.search(r'\b(?:it is hereby enacted|as follows|this act may be called)\b', head, re.I))


def parse_start(line, next_line):
    m = NUM.match(line)
    if not m:
        return None
    number, rest = m.groups()
    rest = ' '.join(rest.split())
    if not rest or len(rest) > 350 or NOTE.match(rest) or HEADING.match(rest):
        return None
    if SUB.match(rest):
        return number, None, 'subsection_start', 0.85
    for pattern in (TITLE_BODY, DASH_BODY):
        t = pattern.match(rest)
        if t and not NOTE_DETAIL.search(t.group('title')):
            return number, t.group('title').strip(), 'title_and_body', 0.92
    # A section heading followed by a subsection on the next line.
    if len(rest) < 110 and SUB.match(next_line.strip()):
        return number, rest.strip(' .—–-'), 'title_next_line', 0.72
    # Numbered bare line followed by heading is especially ambiguous.
    if not rest and next_line:
        return number, None, 'bare_number', 0.3
    return None


def section_key(num):
    m = re.fullmatch(r'(\d+)([A-Za-z]{0,2})', num)
    return (int(m.group(1)), m.group(2).upper()) if m else (0, '')


def main():
    if not INPUT.exists():
        raise SystemExit('Missing processed/pages.jsonl; run collector.py --input sources.xlsx --extract first.')
    docs = defaultdict(list)
    with INPUT.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                docs[row['document_id']].append(row)
    titles = load_titles()
    sections, reports, reviews = [], [], []
    for doc_id, pages in sorted(docs.items()):
        pages.sort(key=lambda p: int(p['page']))
        flat, skipped = [], 0
        for page in pages:
            text = page.get('text') or ''
            if toc_page(text):
                skipped += 1
                continue
            for i, line in enumerate(text.splitlines()):
                flat.append({'page': int(page['page']), 'line': i + 1, 'text': line, 'source': page})
        hits = []
        for i, row in enumerate(flat):
            following = flat[i+1]['text'] if i+1 < len(flat) and flat[i+1]['page'] == row['page'] else ''
            match = parse_start(row['text'], following)
            if match:
                hits.append((i, *match))
        # Require an identifiable Section 1 to avoid treating a random footnote as the start.
        start_at = next((j for j, (_, num, title, kind, _) in enumerate(hits)
                         if section_key(num)[0] == 1 and
                         (kind == 'subsection_start' or (title and FIRST.search(title)))), None)
        if start_at is None:
            reviews.append({'document_id': doc_id, 'page': '', 'section_number': '', 'reason': 'section_one_not_found', 'sample': ''})
            reports.append({'document_id': doc_id, 'pages': len(pages), 'toc_pages_skipped': skipped,
                            'raw_candidates': len(hits), 'accepted_sections': 0, 'review_flags': 1,
                            'first_section_page': '', 'last_section_number': '', 'status': 'needs_format_review'})
            continue
        hits = hits[start_at:]
        accepted = []
        prev = (0, '')
        for hit in hits:
            idx, num, title, kind, confidence = hit
            key = section_key(num)
            # No backwards movement, no repeated section numbers. Section suffixes permitted.
            if key <= prev:
                continue
            if key[0] > prev[0] + 1:
                # Avoid jumps to numbered amendment footnotes; flag possible missing sections.
                reviews.append({'document_id': doc_id, 'page': flat[idx]['page'], 'section_number': num,
                                'reason': 'number_gap_or_false_positive', 'sample': flat[idx]['text'][:180]})
                if key[0] > prev[0] + 4:
                    continue
                confidence = min(confidence, 0.55)
            if kind == 'title_next_line' and NOTE_DETAIL.search(flat[idx]['text']):
                continue
            accepted.append((idx, num, title, kind, confidence))
            prev = key
        for j, (idx, num, title, kind, confidence) in enumerate(accepted):
            end = accepted[j+1][0] if j+1 < len(accepted) else len(flat)
            segment = flat[idx:end]
            if not segment:
                continue
            # Exact candidate text until the next accepted section; includes footnotes/headers.
            content = '\n'.join(r['text'] for r in segment).strip()
            if not content:
                continue
            flags = []
            if confidence < 0.8:
                flags.append('uncertain_heading')
            if len(content) < 70:
                flags.append('short_section')
            if len(content) > 30000:
                flags.append('long_section_or_missed_boundary')
            if NOTE_DETAIL.search(content):
                flags.append('contains_amendment_notes_or_footnotes')
            if j == len(accepted)-1:
                flags.append('last_section_may_include_schedules_or_endnotes')
            for reason in flags:
                reviews.append({'document_id': doc_id, 'page': flat[idx]['page'], 'section_number': num,
                                'reason': reason, 'sample': flat[idx]['text'][:180]})
            src = flat[idx]['source']
            sections.append({'document_id': doc_id, 'law_id': src.get('law_id'),
                'domain': src.get('domain'), 'jurisdiction': src.get('jurisdiction'),
                'title': titles.get(doc_id, ''), 'section_number': num,
                'section_title_candidate': title, 'start_page': flat[idx]['page'],
                'end_page': segment[-1]['page'], 'start_line': flat[idx]['line'],
                'text': content, 'characters': len(content), 'confidence_score_heuristic': confidence,
                'review_flags': flags, 'source_page_url': src.get('source_page_url'),
                'sha256': src.get('sha256'), 'legal_status': src.get('legal_status', 'unknown'),
                'verification_status': 'needs_review', 'full_section_text_verified': False,
                'extraction_note': 'Candidate boundaries only; text may contain page headers, footnotes, schedules or missed sections.'})
        own_flags = [r for r in reviews if r['document_id'] == doc_id]
        reports.append({'document_id': doc_id, 'pages': len(pages), 'toc_pages_skipped': skipped,
                        'raw_candidates': len(hits), 'accepted_sections': len(accepted),
                        'review_flags': len(own_flags), 'first_section_page': flat[accepted[0][0]]['page'] if accepted else '',
                        'last_section_number': accepted[-1][1] if accepted else '',
                        'status': 'needs_review' if accepted else 'needs_format_review'})
    OUT.mkdir(exist_ok=True)
    with (OUT / 'sections_v2.jsonl').open('w', encoding='utf-8') as f:
        for row in sections:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
    for name, rows, cols in [
        ('section_report_v2.csv', reports, ['document_id','pages','toc_pages_skipped','raw_candidates','accepted_sections','review_flags','first_section_page','last_section_number','status']),
        ('review_candidates_v2.csv', reviews, ['document_id','page','section_number','reason','sample'])]:
        with (OUT / name).open('w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
    print(f'Documents: {len(reports)} | Candidate sections: {len(sections)} | Review flags: {len(reviews)}')
    for r in reports:
        print(f"{r['document_id']}: {r['accepted_sections']} candidates; {r['review_flags']} flags; {r['status']}")
    print('Outputs: processed/sections_v2.jsonl, processed/section_report_v2.csv, processed/review_candidates_v2.csv')
    print('CAUTION: All extracted sections are UNVERIFIED; do not treat them as authoritative legal citations.')

if __name__ == '__main__':
    main()
