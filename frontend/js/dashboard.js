const API_BASE = "https://ai-stock-platform-zpkg.onrender.com";
const DEFAULT_STOCKS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOGL"];

document.addEventListener("DOMContentLoaded", () => {
  loadDefaultStocks();
});

/* =========================
   LOAD MARKET OVERVIEW
========================= */
async function loadDefaultStocks() {
  const container = document.getElementById("default-stocks");
  container.innerHTML = "";

  for (const sym of DEFAULT_STOCKS) {
    const card = document.createElement("div");
    card.className = "stock-card";
    card.onclick = () => autoAnalyze(sym);

    card.innerHTML = `
      <h3>${sym}</h3>

      <div class="mini-chart">
        <canvas id="chart-${sym}"></canvas>
      </div>

      <div class="expanded-info">
        <p class="news">Loading latest news...</p>
      </div>

      <p class="mini-signal loading">Loading...</p>
    `;

    container.appendChild(card);

    renderMiniChart(`chart-${sym}`, sym);

    // SIGNAL
    fetch(`${API_BASE}/analyze/${sym}`)
      .then(res => res.json())
      .then(data => {
        const signalEl = card.querySelector(".mini-signal");
        signalEl.textContent = data.signal;
        signalEl.className = "mini-signal " + data.signal;
      });

    // NEWS
    fetch(`${API_BASE}/news/${sym}`)
      .then(res => res.json())
      .then(news => {
        const newsEl = card.querySelector(".news");

        if (!news.headlines || news.headlines.length === 0) {
          newsEl.textContent = "No major news.";
          return;
        }

        newsEl.innerHTML = news.headlines
          .slice(0, 2)
          .map(h => `• ${h}`)
          .join("<br>");
      })
      .catch(() => {
        card.querySelector(".news").textContent = "News unavailable";
      });
  }
}

/* =========================
   SEARCH ANALYSIS
========================= */
async function analyzeStock() {
  const symbol = document.getElementById("symbol").value.trim().toUpperCase();
  const output = document.getElementById("output");

  if (!symbol) {
    output.innerHTML = "Please enter a symbol";
    return;
  }

  output.innerHTML = `<div class="loading"></div>`;

  try {
    const res = await fetch(`${API_BASE}/analyze/${symbol}`);
    const data = await res.json();

    let recommendation =
      data.buy_score >= 75 ? "STRONG BUY" :
      data.buy_score >= 60 ? "BUY" :
      data.buy_score >= 45 ? "HOLD" : "SELL";

    const recClass = recommendation.replace(" ", "-");

    output.innerHTML = `
      <h3>${symbol}</h3>
      <p><b>Prediction:</b> ${Number(data.prediction).toFixed(4)}</p>
      <p><b>Sentiment:</b> ${Number(data.sentiment).toFixed(3)}</p>
      <p><b>Risk Level:</b> ${data.risk_level}</p>
      <p><b>Model MAE:</b> ${data.model_mae}</p>
      <p><b>Buy Score:</b> ${data.buy_score}</p>
      <h2 class="rec ${recClass}">${recommendation}</h2>
    `;

    renderMeter(data.buy_score);

  } catch {
    output.innerHTML = "Error fetching data";
  }
}

function autoAnalyze(symbol) {
  document.getElementById("symbol").value = symbol;
  analyzeStock();
}

/* =========================
   MINI CHART
========================= */
async function renderMiniChart(canvasId, symbol) {
  try {
    const res = await fetch(`${API_BASE}/prices/${symbol}`);
    const priceData = await res.json();

    const ctx = document.getElementById(canvasId).getContext("2d");

    new Chart(ctx, {
      type: "line",
      data: {
        labels: priceData.map(p => p.date),
        datasets: [{
          data: priceData.map(p => p.Close),
          borderColor: "#22c55e",
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.4,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 600
        },
        plugins: { legend: { display: false } },
        scales: {
          x: { display: false },
          y: { display: false }
        }
      }
    });

  } catch (err) {
    console.log(err);
  }
}