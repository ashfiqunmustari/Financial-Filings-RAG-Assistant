from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import answer_question
from fastapi import HTTPException
import logging
logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Financial Filings Q&A API",
    version="1.0"
)

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "Financial Filings Q&A API is running."
    }

@app.post("/ask")
def ask(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        return answer_question(request.question)
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise HTTPException(status_code=500, detail="Failed to process the question.")
    
@app.get("/health")
def health():
    return {"status": "ok"}