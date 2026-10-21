"""Fast unit tests: no model download needed."""
from app.services.multilingual_report import localize_report

sample = {
    'summary': 'Rental agreement summary.',
    'missing_clauses': {'expected_clauses': ['Security Deposit'], 'total_expected': 1},
    'risk_analysis': {'risk_score': 85, 'risk_level': 'Higher screening score',
                      'findings': [{'issue': 'Missing deposit', 'reason': 'Not found', 'weight': 10}]},
    'fairness_analysis': {'findings': [{'indicator': 'Penalty', 'explanation': 'Review clause',
                                        'matched_text': 'forfeiture', 'clause_excerpt': 'Original evidence'}]},
    'legal_references': {'count': 1, 'notice': 'Verify law', 'results': [
        {'chunk_id': 'RENT_001:p1:c1', 'page': 1, 'source_url': 'https://example.org',
         'text': 'Original law text', 'verification_status': 'unverified'}]},
}

def fake_translate(text, target_language):
    return {'translated_text': f'{target_language}: {text}'}

hi = localize_report(sample, 'Hindi ', translate_fn=fake_translate)
assert hi['summary'] == 'Hindi: Rental agreement summary.'
assert hi['missing_clauses']['expected_clauses'] == ['Hindi: Security Deposit']
assert hi['risk_analysis']['risk_score'] == 85
assert hi['fairness_analysis']['findings'][0]['matched_text'] == 'forfeiture'
assert hi['legal_references']['results'][0]['page'] == 1
assert 'text' not in hi['legal_references']['results'][0]
assert localize_report(sample, 'English')['summary'] == sample['summary']
print('PASS: English passthrough, Hindi labels, scores and evidence protected')
