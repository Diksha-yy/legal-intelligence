# Legal Intelligence — research evidence register

**Verified from previously supplied evaluation output, not independently rerun in this environment:**

| Module | Reported metric | Result | Scope / caveat |
|---|---|---|---|
| M1 OCR | CER / WER | 0.0000 / 0.0000 | One synthetic PDF; not general OCR accuracy |
| M2 keyword | Accuracy / macro F1 | 82.50% / 84.05% | 40 synthetic employment clauses, 8 classes; independent label review pending |
| M3 BART | ROUGE-1 / ROUGE-2 / ROUGE-L F1 | 0.5263 / 0.4000 / 0.3509 | One reference summary |
| M4 Hindi | BLEU / chrF++ | 8.6969 / 48.3211 | Illustrative unreviewed reference |
| M4 Marathi | BLEU / chrF++ | 12.3990 / 56.6903 | Illustrative unreviewed reference |
| M5 | Precision / recall / F1 | 1.0 / 1.0 / 1.0 | One limited synthetic case |
| M6 | Expected vs calculated score | 25 vs 25 | One test; not a risk prediction accuracy metric |
| M7 | Reported precision / recall / F1 | 1.0 / 1.0 / 1.0 | Inconsistent counts: 6 expected, 7 detected, 6 TP, 0 FP; audit needed |
| M8 | Supported reference answers | 5/5 | Single indexed chunk; no retrieval benchmark |
| M9 | Detected expected changes | 0/2 | Initial test, before replacement; rerun after fix |

**Never** combine heterogeneous metrics into a single 'overall accuracy'. Do not compare to commercial sites without a shared benchmark. The hybrid model comparison script evaluates all three M2 methods on the *same* examples, but the provided dataset remains synthetic employment-only.

## Minimum additional defensible experiments

- Independently review labels and collect held-out examples for **employment, rental, property, divorce**; keep all models evaluated on identical test cases.
- Evaluate language quality separately for English/Hindi/Marathi using reviewed reference translations and factual/number-preservation checks.
- Test M8 on multiple documents and annotated relevant passages; compute Recall@k and MRR.
- Test M9 on annotated additions, deletions, numeric and semantic changes; calculate precision/recall/F1, not just number of returned items.
- Report API warm/cold runtime with PDF page counts, scan status, CPU/RAM, and mode.
- Add actual screenshots only after live execution; never use mock results as observed results.
