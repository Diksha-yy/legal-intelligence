"""Localize the user-facing parts of Legal Intelligence's English analysis.

Preserves original evidence, legal citations, scores, and full original report.
Uses existing M4 translate_text(text, target_language=...) interface.
"""
from __future__ import annotations
from copy import deepcopy

LANGUAGES = {'english': 'English', 'hindi': 'Hindi', 'marathi': 'Marathi'}

# Translate only known user-facing fields; never translate arbitrary text recursively.
TEXT_FIELDS = {'summary', 'risk_level', 'issue', 'reason', 'type',
               'indicator', 'explanation', 'disclaimer', 'notice',
               'category', 'recommendation', 'description', 'title', 'suggested_action', 'potential_impact'}
LABEL_LIST_FIELDS = {'expected_clauses', 'detected_clauses', 'potentially_missing_clauses'}
# Immutable evidence/metadata, including source excerpts, document clauses, and URLs.
PROTECTED_FIELDS = {'ocr', 'classification', 'legal_references', 'original_text',
                    'full_text', 'clause', 'clause_excerpt', 'matched_text',
                    'text', 'source_text', 'source_url', 'source_sha256',
                    'document_type', 'domain', 'filename', 'status',
                    'risk_score', 'fairness_score', 'weight', 'confidence',
                    'similarity', 'page', 'law_id', 'document_id', 'chunk_id',
                    'verification_status', 'legal_status'}


def localize_report(report: dict, target_language: str = 'English', translate_fn=None) -> dict:
    """Return original English report plus a compact localized user-facing view.

    Only works on an English analysis. This is OUTPUT localization, not source
    document language detection/translation. Does not validate legal accuracy.
    """
    if not isinstance(report, dict):
        raise TypeError('report must be a dictionary')
    language = LANGUAGES.get(str(target_language).strip().lower())
    if language is None:
        raise ValueError('Supported report languages: English, Hindi, Marathi')

    if translate_fn is None and language != 'English':
        from app.modules.m4_translation.translator import translate_text
        translate_fn = translate_text

    cache = {}

    def translate(value):
        if not isinstance(value, str) or not value.strip() or language == 'English':
            return value
        if value not in cache:
            result = translate_fn(value, target_language=language)
            if not isinstance(result, dict) or not isinstance(result.get('translated_text'), str):
                raise ValueError('M4 must return a dictionary with translated_text')
            cache[value] = result['translated_text']
        return cache[value]

    def walk(node):
        if isinstance(node, list):
            return [walk(x) for x in node]
        if not isinstance(node, dict):
            return deepcopy(node)
        result = {}
        for key, value in node.items():
            if key in PROTECTED_FIELDS:
                result[key] = deepcopy(value)
            elif key in LABEL_LIST_FIELDS and isinstance(value, list):
                result[key] = [translate(item) if isinstance(item, str) else deepcopy(item)
                               for item in value]
            elif key in TEXT_FIELDS and isinstance(value, str):
                result[key] = translate(value)
            elif isinstance(value, (dict, list)):
                result[key] = walk(value)
            else:
                result[key] = deepcopy(value)
        return result

    # Compact display layer: do not copy full OCR/classification/RAG passages twice.
    display = {
        'summary': report.get('summary', ''),
        'missing_clauses': report.get('missing_clauses', {}),
        'risk_analysis': report.get('risk_analysis', {}),
        'fairness_analysis': report.get('fairness_analysis', {}),
        'comparison_analysis': report.get('comparison_analysis', {}),
        'legal_references': {
            'count': report.get('legal_references', {}).get('count', 0),
            'notice': report.get('legal_references', {}).get('notice', ''),
            'results': [
                {key: entry.get(key) for key in
                 ('chunk_id', 'document_id', 'law_id', 'page', 'source_url',
                  'verification_status', 'legal_status')}
                for entry in report.get('legal_references', {}).get('results', [])
            ],
        },
    }
    localized = walk(display)
    localized['language'] = language
    localized['translation_status'] = 'not_required' if language == 'English' else 'machine_translated_unverified'
    return localized
