console.log("we live baby!");

// ===== DOM REFERENCES =====
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");

const summaryText = document.getElementById("summaryText");
const sentimentBadge = document.getElementById("sentimentBadge");
const sentimentScore = document.getElementById("sentimentScore");

const statusText = document.getElementById("statusText");
const spinner = document.getElementById("spinner");

const dropzone = document.getElementById("paste_container");

const articleInput = document.getElementById("articleInput");

// We'll temporarily simulate input

// ===== BUTTON EVENTS =====
analyzeBtn.addEventListener("click", async () => {
  const articleText = articleInput.value;
  if (!articleText.trim()) {
    alert("Please provide text first.");
    return;
  }

  try {
    setLoading(true);

    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: articleText }),
    });

    const data = await response.json();

    updateUI(data);

    setStatus("Analysis complete.");
  } catch (error) {
    console.error(error);
    setStatus("Something went wrong.");
  } finally {
    setLoading(false);
  }
});

clearBtn.addEventListener("click", () => {
  summaryText.textContent = "No summary yet.";
  sentimentBadge.textContent = "Neutral";
  sentimentBadge.className = "sentiment-badge neutral";
  sentimentScore.textContent = "—";
  setStatus("Cleared.");
});

// ===== UI HELPERS =====
function updateUI(data) {
  summaryText.textContent = data.summary;
  sentimentScore.textContent = data.sentiment_score;

  sentimentBadge.textContent = data.sentiment;

  sentimentBadge.classList.remove("positive", "negative", "neutral");

  if (data.sentiment === "Positive") {
    sentimentBadge.classList.add("positive");
  } else if (data.sentiment === "Negative") {
    sentimentBadge.classList.add("negative");
  } else {
    sentimentBadge.classList.add("neutral");
  }
}

function setLoading(isLoading) {
  if (isLoading) {
    spinner.classList.add("is-on");
    setStatus("Analyzing...");
    analyzeBtn.disabled = true;
  } else {
    spinner.classList.remove("is-on");
    analyzeBtn.disabled = false;
  }
}

function setStatus(text) {
  statusText.textContent = text;
}
