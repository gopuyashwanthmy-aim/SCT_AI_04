import re
from collections import Counter

STOPWORDS = set({'for', 'been', 'being', 'no', 'the', 'it', 'you', 'does', 'that', 'would', 'those', 'an', 'at', 'these', 'to', 'if', 'me', 'from', 'by', 'not', 'on', 'a', 'and', 'of', 'can', 'could', 'as', 'was', 'i', 'then', 'or', 'in', 'but', 'my', 'with', 'be', 'do', 'this', 'your', 'we', 'are', 'is', 'should', 'did', 'were'})

def tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-zA-Z0-9]+", (text or "").lower()) if w not in STOPWORDS]

def overlap_score(a: str, b: str) -> float:
    aa, bb = set(tokens(a)), set(tokens(b))
    if not aa:
        return 0.0
    return round(len(aa & bb) / len(aa), 3)

def evaluate_case(question: str, answer: str, context: str) -> dict:
    relevance = overlap_score(answer, question)
    faithfulness = overlap_score(answer, context) if context.strip() else 0.0
    unsupported = 1.0 - faithfulness if context.strip() else 1.0
    return {
        "answer_relevance_proxy": relevance,
        "faithfulness_proxy": faithfulness,
        "hallucination_risk_proxy": round(unsupported, 3),
        "note": "Lexical-overlap proxies only; not semantic or factuality guarantees."
    }

def evaluate_dataset(cases: list[dict]) -> list[dict]:
    rows = []
    for case in cases:
        rows.append({
            "id": case["id"],
            "question": case["question"],
            "context": case.get("context", ""),
            "answer": case["answer"],
            **evaluate_case(case["question"], case["answer"], case.get("context", "")),
        })
    return rows
