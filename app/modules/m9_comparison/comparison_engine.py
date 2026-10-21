"""M9 explainable comparison screening. Standard-library only.
Modes: legal, template, two_documents. Not a legal compliance verdict.
"""
from __future__ import annotations
import re
from difflib import SequenceMatcher
from collections import Counter

MAX_CLAUSES = 150
MIN_MATCH = 0.48


def _clean(value):
    return re.sub(r'\s+', ' ', str(value or '')).strip()


def _split(text):
    text = str(text or '')
    parts = re.split(r'(?m)^\s*(?=(?:\d{1,3}[.)]|\([a-z]\)|[A-Z][A-Za-z /]{3,45}:)\s+)|\n\s*\n+', text)
    parts = [_clean(p) for p in parts if len(_clean(p)) >= 28]
    if len(parts) < 2:
        parts = [_clean(p) for p in re.split(r'(?<=[.;])\s+|\n+', text) if len(_clean(p)) >= 28]
    return parts[:MAX_CLAUSES]


def _clauses(classification, text):
    if isinstance(classification, dict):
        for key in ('clauses', 'classified_clauses', 'results'):
            rows = classification.get(key)
            if isinstance(rows, list):
                items = []
                for row in rows:
                    v = row if isinstance(row, str) else (row.get('clause') or row.get('text') or '') if isinstance(row, dict) else ''
                    if len(_clean(v)) >= 28:
                        items.append(_clean(v))
                if items:
                    return items[:MAX_CLAUSES]
    return _split(text)


def _tokens(s):
    return set(re.findall(r'[a-z0-9]+', s.lower()))


def _score(a, b):
    ta, tb = _tokens(a), _tokens(b)
    overlap = len(ta & tb) / len(ta | tb) if ta and tb else 0
    sequence = SequenceMatcher(None, a.lower()[:700], b.lower()[:700]).ratio()
    return round(.55 * overlap + .45 * sequence, 3)


def _numbers(text):
    return re.findall(r'(?<!\w)(?:₹|rs\.?\s*)?\d+(?:[,.]\d+)*(?:\s*%|\s*(?:days?|months?|years?|hours?))?', text.lower())


def _preview(s, limit=180):
    s = _clean(s)
    return s if len(s) <= limit else s[:limit].rsplit(' ', 1)[0] + '…'


def _title(change, a, b):
    if change == 'modified' and _numbers(a) != _numbers(b):
        return 'Number, amount or duration may have changed'
    return {'modified': 'Clause wording changed', 'added': 'Clause added in second document',
            'removed': 'Clause absent from second document', 'similar': 'Similar clause found'}.get(change, 'Review clause')


def _pairwise(left, right, mode, max_findings=20):
    candidates = sorted(((_score(a, b), i, j) for i, a in enumerate(left) for j, b in enumerate(right)), reverse=True)
    matched_l, matched_r, pairs = set(), set(), []
    for score, i, j in candidates:
        if score < MIN_MATCH:
            break
        if i not in matched_l and j not in matched_r:
            matched_l.add(i); matched_r.add(j); pairs.append((i, j, score))
    counts = Counter()
    findings = []
    for i, j, score in sorted(pairs):
        a, b = left[i], right[j]
        if a.casefold() == b.casefold():
            counts['unchanged'] += 1
            continue
        # Similar wording alone is not enough to declare an important modification.
        change = 'similar' if score >= .87 and _numbers(a) == _numbers(b) else 'modified'
        counts[change] += 1
        if change == 'modified':
            findings.append({'title': _title(change, a, b), 'change_type': change,
                             'old_excerpt': _preview(a), 'new_excerpt': _preview(b),
                             'explanation': 'Corresponding clauses differ; review the original wording.',
                             'suggested_action': 'Check both complete clauses before signing.',
                             'evidence': {'document1_clause_id': f'C{i+1}', 'document2_clause_id': f'C{j+1}'},
                             'match_score': score, 'review_required': True})
    for i, a in enumerate(left):
        if i not in matched_l:
            counts['removed'] += 1
            findings.append({'title': _title('removed', a, ''), 'change_type': 'removed',
                             'old_excerpt': _preview(a), 'new_excerpt': '',
                             'explanation': 'No sufficiently similar clause was found in the second document.',
                             'suggested_action': 'Check whether this obligation was removed or reworded.',
                             'evidence': {'document1_clause_id': f'C{i+1}', 'document2_clause_id': None},
                             'review_required': True})
    for j, b in enumerate(right):
        if j not in matched_r:
            counts['added'] += 1
            findings.append({'title': _title('added', '', b), 'change_type': 'added',
                             'old_excerpt': '', 'new_excerpt': _preview(b),
                             'explanation': 'No sufficiently similar clause was found in the first document.',
                             'suggested_action': 'Read the new clause and check its implications.',
                             'evidence': {'document1_clause_id': None, 'document2_clause_id': f'C{j+1}'},
                             'review_required': True})
    # Sort modifications first, then additions and removals. Never discard summary counts.
    findings.sort(key=lambda f: {'modified': 0, 'added': 1, 'removed': 2}.get(f['change_type'], 3))
    return {'status': 'completed', 'mode': mode, 'method': 'heuristic_clause_alignment',
            'summary': {'document1_clauses': len(left), 'document2_clauses': len(right),
                        'unchanged': counts['unchanged'], 'similar': counts['similar'],
                        'modified': counts['modified'], 'added': counts['added'],
                        'removed': counts['removed'], 'findings_shown': min(len(findings), max_findings),
                        'review_required': bool(findings)},
            'important_findings': findings[:max_findings],
            'disclaimer': 'Preliminary text comparison. Matching errors are possible; check original clauses.'}


def run_comparison(text: str, classification: dict, legal_references: dict,
                   mode: str = 'legal', reference_text: str | None = None) -> dict:
    """Preserves existing M9 call signature in legal_ai_pipeline_m9.py."""
    mode = (mode or 'legal').lower().strip()
    if mode not in ('legal', 'template', 'two_documents'):
        return {'status': 'unsupported_mode', 'mode': mode, 'important_findings': [],
                'reason': 'Choose legal, template, or two_documents.'}
    left = _clauses(classification, text)
    if mode in ('template', 'two_documents'):
        if not (reference_text or '').strip():
            return {'status': 'needs_reference', 'mode': mode, 'important_findings': [],
                    'reason': 'Provide reference agreement text or extracted second-document text.'}
        right = _split(reference_text)
        if not left or not right:
            return {'status': 'insufficient_clauses', 'mode': mode, 'important_findings': [],
                    'reason': 'One document has no usable clauses.'}
        result = _pairwise(left, right, mode)
        if mode == 'template':
            result['disclaimer'] += ' Template differences are not legal violations.'
        return result

    refs = legal_references.get('results', []) if isinstance(legal_references, dict) else []
    if not refs:
        return {'status': 'no_references', 'mode': 'legal', 'important_findings': [],
                'reason': 'M8 returned no legal references.'}
    findings = []
    for ref in refs[:5]:
        evidence = _clean(ref.get('text'))
        if not evidence or not left:
            continue
        i, score = max(((i, _score(clause, evidence)) for i, clause in enumerate(left)), key=lambda pair: pair[1])
        findings.append({'title': 'Possible related legal reference',
                         'change_type': 'legal_reference_candidate',
                         'agreement_excerpt': _preview(left[i]),
                         'reference_excerpt': _preview(evidence),
                         'explanation': 'A potentially related legal passage was retrieved; applicability and meaning are not verified.',
                         'suggested_action': 'Check the cited law, section, jurisdiction and effective date with a qualified reviewer.',
                         'evidence': {'agreement_clause_id': f'C{i+1}', 'law_id': ref.get('law_id'),
                                      'document_id': ref.get('document_id'), 'page': ref.get('page'),
                                      'source_url': ref.get('source_url')},
                         'match_score': score, 'verification_status': ref.get('verification_status', 'unverified'),
                         'legal_violation_confirmed': False, 'review_required': True})
    return {'status': 'completed', 'mode': 'legal', 'method': 'legal_reference_screening',
            'summary': {'agreement_clauses': len(left), 'references_reviewed': len(findings),
                        'confirmed_violations': 0, 'review_required': bool(findings)},
            'important_findings': findings,
            'disclaimer': 'Related references only. This does not determine legal compliance or violations.'}
