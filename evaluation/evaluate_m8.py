
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, PROJECT_ROOT)

from app.modules.m8_rag.legal_qa import LegalQA

# --------------------------------------------------
# Synthetic employment document
# --------------------------------------------------

document_text = """
EMPLOYMENT AGREEMENT

The employee will work as a Software Engineer at ABC Technologies.

The employee will work 40 hours per week, from Monday to Friday.

The monthly salary will be INR 40,000, payable on the last
working day of each month.

The employee will receive medical insurance benefits.

The employee must provide necessary background checks.

The employee must give 30 days written notice before
voluntarily terminating the employment agreement.

Both parties must sign this agreement.

The employee must keep confidential all company information,
trade secrets, and customer data during and after employment.
"""

# --------------------------------------------------
# Test questions and reference answers
# --------------------------------------------------

test_cases = [
    {
        "question": "What is the monthly salary?",
        "expected_answer": "INR 40,000"
    },
    {
        "question": "How many hours per week must the employee work?",
        "expected_answer": "40 hours per week"
    },
    {
        "question": "What is the notice period?",
        "expected_answer": "30 days"
    },
    {
        "question": "What benefits are provided?",
        "expected_answer": "medical insurance"
    },
    {
        "question": "What information must remain confidential?",
        "expected_answer": "trade secrets"
    }
]

# These reference answers are drafted from the synthetic
# document and are not independently annotated.

# --------------------------------------------------
# Initialize model and index document
# --------------------------------------------------

print("\nLoading M8 LegalQA model...")

qa = LegalQA()

index_start = time.perf_counter()

chunk_count = qa.index_document(document_text)

index_time = time.perf_counter() - index_start

print("\nDocument indexed.")
print("Total chunks:", chunk_count)
print(f"Indexing time: {index_time:.4f} seconds")

# --------------------------------------------------
# Evaluate retrieval and answer support
# --------------------------------------------------

results = []

for case in test_cases:

    question = case["question"]
    expected_answer = case["expected_answer"]

    start_time = time.perf_counter()

    output = qa.ask_question(
        question,
        top_k=3
    )

    query_time = time.perf_counter() - start_time

    retrieved_text = " ".join(
        item["text"]
        for item in output["sources"]
    ).lower()

    # Check whether the reference answer appears in
    # the retrieved source passages.
    answer_supported = (
        expected_answer.lower() in retrieved_text
    )

    # Check whether the expected answer appears in
    # the full extractive answer returned by M8.
    answer_returned = (
        expected_answer.lower() in output["answer"].lower()
    )

    results.append({
        "question": question,
        "expected_answer": expected_answer,
        "answer_supported": answer_supported,
        "answer_returned": answer_returned,
        "retrieved_count": len(output["sources"]),
        "query_time": query_time,
        "sources": output["sources"]
    })

# --------------------------------------------------
# Calculate simple pilot metrics
# --------------------------------------------------

total_questions = len(results)

supported_count = sum(
    item["answer_supported"]
    for item in results
)

returned_count = sum(
    item["answer_returned"]
    for item in results
)

support_rate = (
    supported_count / total_questions
    if total_questions else 0
)

answer_return_rate = (
    returned_count / total_questions
    if total_questions else 0
)

average_query_time = (
    sum(item["query_time"] for item in results)
    / total_questions
    if total_questions else 0
)

# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n========== M8 EVALUATION RESULTS ==========")

print("Total Questions:", total_questions)
print("Document Chunks:", chunk_count)

print(
    f"Reference Answer Support Rate: "
    f"{support_rate:.4f}"
)

print(
    f"Reference Answer Return Rate: "
    f"{answer_return_rate:.4f}"
)

print(
    f"Average Query Time: "
    f"{average_query_time:.4f} seconds"
)

print("\n--- Question-Level Results ---")

for index, item in enumerate(results, start=1):

    print(f"\nQuestion {index}: {item['question']}")

    print("Expected Answer:", item["expected_answer"])

    print("Answer Supported:", item["answer_supported"])

    print("Answer Returned:", item["answer_returned"])

    print("Retrieved Sources:", item["retrieved_count"])

    print(
        f"Query Time: {item['query_time']:.4f} seconds"
    )

    for source in item["sources"]:
        print(
            f"  {source['source']} | "
            f"Similarity: {source['similarity']:.4f} | "
            f"Rank: {source['rank']}"
        )

print("\nDisclaimer:")
print(
    "This is a synthetic retrieval evaluation. "
    "Similarity scores are not confidence scores "
    "or measures of legal correctness."
)

# --------------------------------------------------
# Save results
# --------------------------------------------------

output_dir = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "results"
)

os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    "m8_results.txt"
)

with open(output_file, "w", encoding="utf-8") as f:

    f.write("M8 Legal QA Evaluation\n")
    f.write("=" * 40 + "\n")

    f.write(f"Total Questions: {total_questions}\n")
    f.write(f"Document Chunks: {chunk_count}\n")
    f.write(f"Indexing Time: {index_time:.4f} seconds\n")

    f.write(
        f"Reference Answer Support Rate: "
        f"{support_rate:.4f}\n"
    )

    f.write(
        f"Reference Answer Return Rate: "
        f"{answer_return_rate:.4f}\n"
    )

    f.write(
        f"Average Query Time: "
        f"{average_query_time:.4f} seconds\n"
    )

    for index, item in enumerate(results, start=1):

        f.write(f"\nQuestion {index}: {item['question']}\n")

        f.write(
            f"Expected Answer: {item['expected_answer']}\n"
        )

        f.write(
            f"Answer Supported: {item['answer_supported']}\n"
        )

        f.write(
            f"Answer Returned: {item['answer_returned']}\n"
        )

        f.write(
            f"Query Time: {item['query_time']:.4f} seconds\n"
        )

        f.write("Retrieved Sources:\n")

        for source in item["sources"]:
            f.write(
                f"- {source['source']}, "
                f"similarity={source['similarity']:.4f}, "
                f"rank={source['rank']}\n"
            )

print("\nResults saved to:", output_file)