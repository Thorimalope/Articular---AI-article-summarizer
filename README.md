# Articular — AI Article Summarizer

Articular is a lightweight full-stack AI web application that summarizes long-form articles and performs sentiment analysis using transformer models from Hugging Face.

The project demonstrates end-to-end integration between a Vanilla JavaScript frontend and a FastAPI backend, with AI inference powered through the Hugging Face Inference API.

---

## 🚀 Features

- Paste full-length articles for summarization
- AI-generated concise summaries
- Sentiment classification (Positive / Negative / Neutral)
- Confidence score display
- Saved summaries using browser Local Storage
- RESTful FastAPI backend
- Secure Hugging Face API integration

---

## 🏗️ Architecture Overview
```
Frontend (HTML, CSS, Vanilla JS)
            ⬇
  FastAPI Backend (Python)
            ⬇
Hugging Face Inference API
```

The frontend handles user interaction and rendering. The backend processes requests and securely communicates with Hugging Face. Hugging Face performs AI inference for summarization and sentiment analysis.

---

## 🖥️ Tech Stack

**Frontend**
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)
- Browser Local Storage API

**Backend**
- Python 3.11
- FastAPI
- Uvicorn
- python-dotenv
- CORS Middleware

**AI Integration**
- Hugging Face Transformer Models
- Hugging Face Hosted Inference API
- API Token Authentication

---

## 📦 Project Structure
```
project-root/
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
└── backend/
    ├── main.py
    ├── requirements.txt
    ├── runtime.txt
    ├── Procfile
    └── .env (not committed)
```

---

## ⚙️ How It Works

1. User pastes article text into the UI.
2. Frontend sends a POST request to the FastAPI backend.
3. Backend sends the text to Hugging Face's Inference API.
4. Hugging Face returns:
   - Summary
   - Sentiment label
   - Confidence score
5. Backend returns the formatted JSON response.
6. Frontend displays results and stores summaries in Local Storage.

---

## 🔐 Environment Variables

Create a `.env` file inside the `backend` folder:
```env
HUGGINGFACE_API_TOKEN=your_token_here
```

> ⚠️ Never commit this file to GitHub.

---

## 🛠️ Local Development Setup

**1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo/backend
```

**2️⃣ Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

**3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

**4️⃣ Run the Backend**
```bash
uvicorn main:app --reload
```

Then visit: `http://localhost:8000/docs`

**5️⃣ Run the Frontend**

Open `frontend/index.html` in your browser, or use a live server extension.

---

## 🌍 Deployment Notes

- Backend deployed using **Railway**
- Python runtime pinned to **3.11**
- Hugging Face inference moved to API-based model calls
- Environment variables configured in hosting dashboard
- CORS enabled for frontend-backend communication

---

## 🔄 Architectural Evolution

Originally, transformer models were loaded locally using the `transformers` library. Deployment challenges included:

- Rust compilation errors (`tokenizers`)
- Large memory usage
- Hosting platform restrictions
- Long cold start times

**Solution:**
- Downsized models
- Migrated to Hugging Face Hosted Inference API
- Reduced backend memory footprint
- Improved deployment reliability

---

## ⚠️ Limitations

- No user authentication
- Local Storage limited to individual browser
- Dependent on Hugging Face API availability
- API rate limits may apply
- No database integration

---

## 🔮 Future Improvements

- User accounts & authentication
- Cloud database integration
- PDF article upload support
- Model fine-tuning
- Improved caching
- UI/UX enhancements

---

## 📚 Learning Outcomes

This project demonstrates:

- Full-stack web development
- REST API design with FastAPI
- AI model integration in production systems
- Deployment troubleshooting
- Environment configuration and security practices
- Real-world ML hosting constraints
