import re
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer
from app.modules.m2_classification.classifier import split_into_clauses

class AgreementComparator:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def extract_clauses(self, text):
        return [c.strip() for c in split_into_clauses(text) if isinstance(c, str) and c.strip()]

    def compare_text(self, text1, text2):
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def compare_documents(self, text1, text2):
        if not text1 or not text1.strip() or not text2 or not text2.strip():
            raise ValueError('Both documents must contain text.')
        a, b = self.extract_clauses(text1), self.extract_clauses(text2)
        if not a or not b:
            raise ValueError('Could not extract clauses from both documents.')
        from numpy import asarray
        e1 = asarray(self.model.encode(a, normalize_embeddings=True, convert_to_numpy=True))
        e2 = asarray(self.model.encode(b, normalize_embeddings=True, convert_to_numpy=True))
        scores = e1 @ e2.T
        # One-to-one matching prevents multiple old clauses mapping to one new clause.
        pairs = sorted(((float(scores[i,j]), i, j) for i in range(len(a)) for j in range(len(b))), reverse=True)
        used_a, used_b = set(), set()
        matched, changed = [], []
        for semantic, i, j in pairs:
            if i in used_a or j in used_b:
                continue
            lexical = self.compare_text(a[i], b[j])
            if semantic < 0.45 and lexical < 0.50:
                continue
            used_a.add(i); used_b.add(j)
            entry = {'document1_clause': a[i], 'document2_clause': b[j], 'similarity': round(semantic,4)}
            matched.append(entry)
            # Check exact normalized wording; a changed number must never be hidden by high semantic similarity.
            norm_a = ' '.join(a[i].casefold().split())
            norm_b = ' '.join(b[j].casefold().split())
            if norm_a != norm_b:
                changed.append({**entry, 'semantic_similarity': round(semantic,4), 'text_similarity': round(lexical,4),
                                'document1_numbers': re.findall(r'\b\d+(?:[.,]\d+)?%?\b',a[i]),
                                'document2_numbers': re.findall(r'\b\d+(?:[.,]\d+)?%?\b',b[j])})
        return {
            'document1_clause_count': len(a), 'document2_clause_count': len(b),
            'matched_clauses': matched, 'changed_clauses': changed,
            'missing_from_document2': [c for i,c in enumerate(a) if i not in used_a],
            'missing_from_document1': [c for j,c in enumerate(b) if j not in used_b],
            'document1_numbers': re.findall(r'\b\d+(?:[.,]\d+)?%?\b',text1),
            'document2_numbers': re.findall(r'\b\d+(?:[.,]\d+)?%?\b',text2),
            'disclaimer': 'Preliminary automated comparison. All changes and matches require human review.'
        }
