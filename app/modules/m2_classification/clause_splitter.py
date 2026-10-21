import re


def split_legal_clauses(text):
    """
    Split document text into candidate clauses.

    Handles:
    - Newlines
    - Numbered clauses
    - Multiple sentences in one paragraph
    """

    if not isinstance(text, str) or not text.strip():
        return []

    text = text.replace("\r\n", "\n").strip()

    # Split paragraphs and numbered sections
    sections = re.split(
        r"\n\s*\n+|\n(?=\s*(?:\d+(?:\.\d+)*[.)]|[a-zA-Z][.)])\s+)",
        text
    )

    clauses = []

    for section in sections:
        section = section.strip()

        if not section:
            continue

        # Split multiple sentences
        sentences = re.split(
            r"(?<=[.!?])\s+(?=[A-Z])",
            section
        )

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence.split()) >= 4:
                clauses.append(sentence)

    return clauses