from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    # TEMP: mock response so you can wire up the frontend first
    text = (req.text or "").strip()
    word_count = len(text.split())

    if word_count < 30:
        return {
            "error": "Please paste a longer article (at least ~30 words).",
            "article_word_count": word_count,
        }

    return {
        "article_word_count": word_count,
        "summary": "Mock summary (backend is connected). Next we’ll plug in the real summarizer model.",
        "summary_word_count": 14,
        "sentiment_label": "Neutral",
        "sentiment_score": 0.55,
    }
