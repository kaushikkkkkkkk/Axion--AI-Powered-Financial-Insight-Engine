# Deterministic analyzer 'agent' - small helper functions to analyze extracted text.
import re

KEYWORDS = {
    'revenue': ['revenue', 'sales', 'turnover'],
    'profit': ['profit', 'net income', 'earnings'],
    'loss': ['loss', 'net loss', 'negative'],
    'cash': ['cash', 'cash flow', 'liquidity'],
    'debt': ['debt', 'liabilities', 'borrowings'],
}

def summarize_text(text: str, max_chars: int = 400) -> str:
    # Very simple "summary": first non-empty paragraph up to max_chars
    for part in text.split('\n\n'):
        cleaned = part.strip()
        if cleaned:
            return (cleaned[:max_chars] + '...') if len(cleaned) > max_chars else cleaned
    return text[:max_chars]

def keyword_counts(text: str) -> dict:
    lc = text.lower()
    counts = {}
    for k, variants in KEYWORDS.items():
        c = 0
        for v in variants:
            c += lc.count(v)
        counts[k] = c
    return counts

def generate_recommendation(keyword_counts: dict) -> str:
    # Deterministic rule-based recommendations (NOT financial advice)
    if keyword_counts.get('loss', 0) > max(1, keyword_counts.get('profit', 0)):
        return "Document mentions losses more than profits. Suggest conservative approach: review cost structure and cash runway."
    if keyword_counts.get('debt', 0) > 0 and keyword_counts.get('cash', 0) == 0:
        return "Debt mentions appear without cash highlights — investigate liquidity and maturity profile."
    if keyword_counts.get('revenue', 0) > 0 and keyword_counts.get('profit', 0) > 0:
        return "Revenue and profit both referenced — consider further ratio analysis (gross margin, operating margin). This is a neutral signal."
    if sum(keyword_counts.values()) == 0:
        return "No major financial keywords found — the document may be non-financial or narrative in nature."
    return "Mixed signals found — recommend performing deeper numerical analysis with full financial statements."
