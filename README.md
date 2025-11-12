# Fixed Financial Document Analyzer (Debugged)

## Project overview
This repository is a **fixed, working** version of the Financial Document Analyzer originally built with CrewAI.
The original repo contained intentional bugs and nonsensical prompt text. This fixed version:
- Removes unsafe / broken dependencies on `crewai` and replaces the pipeline with a lightweight, deterministic analyzer.
- Fixes file-name collisions and API issues.
- Adds a clear README, setup instructions, and API documentation.

## What I changed (Bugs found & fixes)

1. **Removed broken/undefined `llm` usage and CrewAI-only runtime**
   - The original code referenced an undefined `llm` object and relied on `crewai` internals that made the project un-runnable.
   - FIX: Replaced the CrewAI agent orchestration with a small, deterministic "agent" module that extracts text and returns basic analysis. This makes the project runnable without proprietary SDKs.

2. **Fixed FastAPI endpoint naming conflict**
   - `analyze_financial_document` was imported from `task.py` and also used as a FastAPI endpoint function name -> name collision.
   - FIX: Endpoint function renamed to `analyze_endpoint` and the orchestrator function `run_analysis`.

3. **Rewrote PDF reading tool**
   - Original code used an undefined `Pdf` class and had broken imports.
   - FIX: Implemented `tools.pdf_reader` using `PyPDF2` to reliably extract text from uploaded PDFs.

4. **Removed malicious / joking prompts**
   - The original repo contained intentionally misleading and unsafe agent backstories and prompts (e.g., "make up investment advice").
   - FIX: Replaced with neutral, factual analysis helpers and documented behaviour.

5. **Simplified dependencies**
   - The original `requirements.txt` referenced many large packages and had inconsistent names.
   - FIX: Provided a minimal `requirements.txt` sufficient to run the FastAPI app locally.

## Features (what the fixed repo provides)
- Upload a PDF via `/analyze` POST endpoint and receive:
  - Extracted text (truncated preview)
  - Basic document metrics (pages, word count)
  - A short deterministic "analysis" that looks for financial keywords and gives plain-language takeaways
  - Simple investment-minded suggestions (conservative, neutral, cautious), based only on keywords present (NOT financial advice).

## Setup & usage
1. Create a virtual environment and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate    # Windows PowerShell
   pip install -r requirements.txt
   ```
2. Run the API:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
3. Open `http://localhost:8000/docs` to use the interactive Swagger UI.

## API documentation
- `GET /`  
  Health check. Returns a JSON message confirming the API is running.

- `POST /analyze`  
  Upload form fields:
    - `file` (file): PDF file to analyze (required)
    - `query` (string): Optional short instruction or context for the analysis.

  Response JSON:
  ```json
  {
    "status": "success",
    "query": "<user query>",
    "file_processed": "<original filename>",
    "pages": <int>,
    "word_count": <int>,
    "preview": "<first 800 chars of text>",
    "analysis": {
      "summary": "<short summary>",
      "key_metrics": { "revenue_mentions": <int>, ... },
      "recommendation": "<text>"
    }
  }
  ```

## Notes & limitations
- This implementation is deterministic and keyword-based. It does **not** make use of external LLMs.
- The output is illustrative and NOT financial advice.

## Files in this repo
- `main.py` - FastAPI app and orchestrator
- `tools.py` - PDF reading helper
- `agents.py` - Small deterministic analyzer (replaces CrewAI Agent)
- `task.py` - Simple task orchestrator used by the API
- `requirements.txt` - Minimal dependencies
