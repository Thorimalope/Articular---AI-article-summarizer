import os
import json
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

SUMMARIZATION_URL = "https://router.huggingface.co/hf-inference/models/sshleifer/distilbart-cnn-12-6"
SENTIMENT_URL = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"

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

    try:
        # Summarize
        sum_response = httpx.post(SUMMARIZATION_URL, headers=HEADERS, json={
            "inputs": text,
            "parameters": {"max_length": 180, "min_length": 60}
        }, timeout=120)

        print("Sum status:", sum_response.status_code)
        print("Sum raw:", sum_response.text)

        sum_data = sum_response.json()

        if isinstance(sum_data, dict) and "error" in sum_data:
            return {"error": f"Summarization error: {sum_data['error']}"}

        summary_text = sum_data[0]["summary_text"]

        # Sentiment
        sent_response = httpx.post(SENTIMENT_URL, headers=HEADERS, json={
            "inputs": summary_text
        }, timeout=60)

        print("Sent status:", sent_response.status_code)
        print("Sent raw:", sent_response.text)

        sent_data = sent_response.json()

        if isinstance(sent_data, dict) and "error" in sent_data:
            return {"error": f"Sentiment error: {sent_data['error']}"}

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

    except httpx.TimeoutException:
        return {"error": "The AI model is warming up, please try again in 30 seconds."}
    except Exception as e:
        print("Unexpected error:", str(e))
        return {"error": f"Unexpected error: {str(e)}"}
