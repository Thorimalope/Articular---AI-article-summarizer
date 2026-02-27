from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

print("Loading summarization model...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Model loaded successfully.")

print("Loading sentiment model...")
sentiment_analyzer = pipeline("sentiment-analysis")
print("Sentiment model loaded successfully.")

app = FastAPI(title="Article Summarizer & Sentiment API")

# Allow your frontend to call the API (fine for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later we can lock this down
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return {
            "error": "Please paste a longer article (at least ~30 words).",
            "article_word_count": word_count,
        }

    # Generate summary
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

    # --- SENTIMENT ANALYSIS ---
    sentiment_result = sentiment_analyzer(summary_text)[0]

    sentiment_label = sentiment_result["label"]
    sentiment_score = float(sentiment_result["score"])

    # Debug print (helps confirm backend works)
    print("Sentiment result:", sentiment_result)

    return {
        "article_word_count": word_count,
        "summary": summary_text,
        "summary_word_count": summary_word_count,

        # ✅ CLEAN STRUCTURE
        "sentiment": {
            "label": sentiment_label,
            "confidence": round(sentiment_score, 3),
        },
    }
