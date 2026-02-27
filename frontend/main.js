console.log("we live baby!");

// ===== DOM REFERENCES =====
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");

const summaryText = document.getElementById("summaryText");
const sentimentBadge = document.getElementById("sentimentBadge");
const sentimentScore = document.getElementById("sentimentScore");

const statusText = document.getElementById("statusText");
const spinner = document.getElementById("spinner");

const articleInput = document.getElementById("articleInput");

const savedSummariesContainer = document.getElementById("savedSummaries");

// ===== LOCAL STORAGE =====
const STORAGE_KEY = "saved_summaries";

// ===== INIT =====
renderSavedSummaries();

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

    saveSummary({
      article: articleText,
      summary: data.summary,
      sentiment: data.sentiment.label,
      confidence: data.sentiment.confidence,
      createdAt: new Date().toISOString(),
    });

    renderSavedSummaries();

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

// ===== UI UPDATE =====
function updateUI(data) {
  summaryText.textContent = data.summary;

  const label = data.sentiment.label;
  const confidence = data.sentiment.confidence;

  sentimentBadge.textContent = label;
  sentimentScore.textContent = confidence;

  sentimentBadge.classList.remove("positive", "negative", "neutral");

  if (label.toLowerCase() === "positive") {
    sentimentBadge.classList.add("positive");
  } else if (label.toLowerCase() === "negative") {
    sentimentBadge.classList.add("negative");
  } else {
    sentimentBadge.classList.add("neutral");
  }
}

// ===== LOCAL STORAGE =====
function saveSummary(entry) {
  const existing = getSavedSummaries();

  existing.unshift(entry);

  const trimmed = existing.slice(0, 20);

  localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmed));
}

function getSavedSummaries() {
  return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
}

function deleteSummary(index) {
  const summaries = getSavedSummaries();
  summaries.splice(index, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(summaries));
  renderSavedSummaries();
}

// ===== RENDER SAVED PANEL =====
function renderSavedSummaries() {
  const summaries = getSavedSummaries();

  savedSummariesContainer.innerHTML = "";

  if (summaries.length === 0) {
    savedSummariesContainer.innerHTML = "<p>No saved summaries yet.</p>";
    return;
  }

  summaries.forEach((item, index) => {
    const card = document.createElement("div");
    card.className = "saved-summary";

    const preview =
      item.summary.length > 120
        ? item.summary.slice(0, 120) + "..."
        : item.summary;

    card.innerHTML = `
      <div class="saved-text">${preview}</div>
      <div class="saved-meta">
        <span>${item.sentiment}</span>
        <button class="delete-btn">✕</button>
      </div>
    `;

    // CLICK → LOAD INTO MAIN UI
    card.querySelector(".saved-text").addEventListener("click", () => {
      summaryText.textContent = item.summary;
      sentimentBadge.textContent = item.sentiment;
      sentimentScore.textContent = item.confidence;
    });

    // DELETE BUTTON
    card.querySelector(".delete-btn").addEventListener("click", (e) => {
      e.stopPropagation();
      deleteSummary(index);
    });

    savedSummariesContainer.appendChild(card);
  });
}

// ===== LOADING =====
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
