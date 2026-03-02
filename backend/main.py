import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Article Summarizer & Sentiment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_TOKEN = os.environ.get("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

SUMMARIZATION_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
SENTIMENT_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

class AnalyzeRequest(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    text = (req.text or "").strip()
    word_count = len(text.split())

    if word_count < 30:
        return {"error": "Please paste a longer article (at least ~30 words).", "article_word_count": word_count}

    # Summarize
    sum_response = httpx.post(SUMMARIZATION_URL, headers=HEADERS, json={
        "inputs": text,
        "parameters": {"max_length": 180, "min_length": 60}
    }, timeout=60)
    
    sum_data = sum_response.json()
    if isinstance(sum_data, dict) and "error" in sum_data:
        return {"error": f"Summarization model error: {sum_data['error']}"}
    
    summary_text = sum_data[0]["summary_text"]

    # Sentiment
    sent_response = httpx.post(SENTIMENT_URL, headers=HEADERS, json={"inputs": summary_text}, timeout=30)
    
    sent_data = sent_response.json()
    if isinstance(sent_data, dict) and "error" in sent_data:
        return {"error": f"Sentiment model error: {sent_data['error']}"}
    
    sentiment = sent_data[0][0]

    return {
        "article_word_count": word_count,
        "summary": summary_text,
        "summary_word_count": len(summary_text.split()),
        "sentiment": {
            "label": sentiment["label"],
            "confidence": round(float(sentiment["score"]), 3),
        },
    }
