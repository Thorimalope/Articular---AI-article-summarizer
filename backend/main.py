from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Article Summarizer & Sentiment API")

# -----------------------------
# GLOBAL MODEL VARIABLES
# -----------------------------
summarizer = None
sentiment_analyzer = None


# -----------------------------
# LOAD MODELS ON STARTUP
# -----------------------------
@app.on_event("startup")
def load_models():
    global summarizer, sentiment_analyzer

    print("Loading summarization model...")
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn"
    )
    print("Summarization model loaded.")

    print("Loading sentiment model...")
    sentiment_analyzer = pipeline("sentiment-analysis")
    print("Sentiment model loaded.")


# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# REQUEST MODEL
# -----------------------------
class AnalyzeRequest(BaseModel):
    text: str


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# ANALYZE ENDPOINT
# -----------------------------
@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    text = (req.text or "").strip()
    word_count = len(text.split())

    if word_count < 30:
        return {
            "error": "Please paste a longer article (at least ~30 words).",
            "article_word_count": word_count,
        }

    # Summary
    result = summarizer(
        text,
        max_length=180,
        min_length=60,
        num_beams=4,
        length_penalty=1.2,
        early_stopping=True,
    )

    summary_text = result[0]["summary_text"]
    summary_word_count = len(summary_text.split())

    # Sentiment
    sentiment_result = sentiment_analyzer(summary_text)[0]

    return {
        "article_word_count": word_count,
        "summary": summary_text,
        "summary_word_count": summary_word_count,
        "sentiment": {
            "label": sentiment_result["label"],
            "confidence": round(float(sentiment_result["score"]), 3),
        },
    }
