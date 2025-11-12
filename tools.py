import os
from PyPDF2 import PdfReader

def read_pdf_text(path: str) -> dict:
    """Read PDF and return dict with pages, full_text."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found: {path}")
    reader = PdfReader(path)
    pages = len(reader.pages)
    texts = []
    for p in reader.pages:
        try:
            texts.append(p.extract_text() or '')
        except Exception:
            texts.append('')
    full_text = "\n".join(texts)
    return {"pages": pages, "text": full_text}
