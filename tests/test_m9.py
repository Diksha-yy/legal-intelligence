import unittest
from app.modules.m9_comparison.comparison_engine import run_comparison

A = 'The employee must provide 30 days notice before leaving.\n\nSalary is paid on the first day of each month.'
B = 'The employee must provide 60 days notice before leaving.\n\nThe employee may work remotely with approval.'

class TestM9(unittest.TestCase):
    def test_document_comparison(self):
        out = run_comparison(A, {}, {}, mode='two_documents', reference_text=B)
        self.assertEqual(out['status'], 'completed')
        self.assertGreaterEqual(out['summary']['modified'], 1)
        self.assertTrue(out['important_findings'])
        self.assertLess(len(str(out['important_findings'][0])), 1500)

    def test_template_requires_reference(self):
        out = run_comparison(A, {}, {}, mode='template')
        self.assertEqual(out['status'], 'needs_reference')

    def test_legal_not_verdict(self):
        refs = {'results': [{'text': 'Employers shall maintain wage records.', 'law_id': 'EXAMPLE', 'page': 2}]}
        out = run_comparison(A, {}, refs)
        self.assertFalse(out['important_findings'][0]['legal_violation_confirmed'])

if __name__ == '__main__':
    unittest.main()
