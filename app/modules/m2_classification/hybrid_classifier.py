from .semantic_classifier import classify_clause_semantic
from .classifier import classify_clause


def classify_clause_hybrid(clause, domain="employment"):
    """
    Hybrid clause classification.

    Employment:
        Existing keyword classifier + semantic classifier

    Other domains:
        Semantic classifier
    """

    semantic_result = classify_clause_semantic(
        clause,
        domain=domain
    )

    if domain != "employment":
        return {
            **semantic_result,
            "method": "semantic"
        }

    keyword_result = classify_clause(clause)

    keyword_category = keyword_result.get(
        "category", "Unclassified"
    )

    semantic_category = semantic_result["category"]

    # Agreement between both classifiers
    if (
        keyword_category != "Unclassified"
        and keyword_category == semantic_category
    ):
        return {
            **semantic_result,
            "category": keyword_category,
            "method": "hybrid_agreement",
            "keyword_category": keyword_category
        }

    # Disagreement: retain both predictions for review
    return {
        **semantic_result,
        "method": "semantic_with_keyword_comparison",
        "keyword_category": keyword_category,
        "needs_review": (
            keyword_category != "Unclassified"
            and keyword_category != semantic_category
        )
    }


def classify_document_hybrid(clauses, domain="employment"):
    return [
        classify_clause_hybrid(clause, domain)
        for clause in clauses
    ]