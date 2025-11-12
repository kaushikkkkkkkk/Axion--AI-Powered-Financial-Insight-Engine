from tools import read_pdf_text
from agents import summarize_text, keyword_counts, generate_recommendation

def analyze_financial_document(file_path: str, query: str = "") -> dict:
    """Reads PDF, extracts text, computes simple metrics and returns an analysis dict."""
    data = read_pdf_text(file_path)
    text = data.get('text', '')
    pages = data.get('pages', 0)
    # basic metrics
    words = len(text.split())
    preview = text[:800]
    summary = summarize_text(text, max_chars=600)
    keys = keyword_counts(text)
    recommendation = generate_recommendation(keys)
    return {
        'pages': pages,
        'word_count': words,
        'preview': preview,
        'summary': summary,
        'key_metrics': keys,
        'recommendation': recommendation
    }
