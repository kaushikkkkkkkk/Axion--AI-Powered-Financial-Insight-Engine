from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os, uuid
from task import analyze_financial_document

app = FastAPI(title="Financial Document Analyzer (Fixed)")

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    # Save uploaded file
    file_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    file_path = f"data/financial_document_{file_id}.pdf"
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Validate query
        if not query:
            query = "Analyze this financial document for investment insights"

        analysis = analyze_financial_document(file_path=file_path, query=query)

        return {
            "status": "success",
            "query": query,
            "file_processed": file.filename,
            "pages": analysis['pages'],
            "word_count": analysis['word_count'],
            "preview": analysis['preview'],
            "analysis": {
                "summary": analysis['summary'],
                "key_metrics": analysis['key_metrics'],
                "recommendation": analysis['recommendation']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # cleanup
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
