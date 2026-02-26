const API_BASE = "https://ai-stock-platform-zpkg.onrender.com";
const DEFAULT_STOCKS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOGL"];

/* =====================================
   LOAD ON DOM READY
===================================== */

document.addEventListener("DOMContentLoaded", () => {
  console.log("Dashboard Loaded");
  loadDefaultStocks();
});

/* =====================================
   LOAD MARKET OVERVIEW
===================================== */

async function loadDefaultStocks() {
  const container = document.getElementById("default-stocks");
  if (!container) return;

  container.innerHTML = "";

  for (const sym of DEFAULT_STOCKS) {

    // ✅ CREATE CARD FIRST (NO BLOCKING)
    const card = document.createElement("div");
    card.className = "stock-card";
    card.onclick = () => autoAnalyze(sym);

    card.innerHTML = `
      <h3>${sym}</h3>
      <div class="mini-chart">
        <canvas id="chart-${sym}"></canvas>
      </div>
      <p class="mini-signal loading">Loading...</p>
    `;

    container.appendChild(card);

    // ✅ LOAD PRICE CHART IMMEDIATELY
    renderMiniChart(`chart-${sym}`, sym);

    // ✅ LOAD SIGNAL SEPARATELY (NON BLOCKING)
    fetch(`${API_BASE}/analyze/${sym}`)
      .then(res => res.json())
      .then(data => {
        const signalEl = card.querySelector(".mini-signal");
        signalEl.textContent = data.signal;
        signalEl.className = "mini-signal " + data.signal;
      })
      .catch(() => {
        card.querySelector(".mini-signal").textContent = "ERR";
      });
  }
}

/* =====================================
   SEARCH ANALYSIS
===================================== */

async function analyzeStock() {
  const symbolInput = document.getElementById("symbol");
  const output = document.getElementById("output");

  const symbol = symbolInput.value.trim().toUpperCase();
  if (!symbol) {
    output.innerHTML = "Please enter a stock symbol";
    return;
  }

  output.innerHTML = `<div class="loading"></div>`;

  try {
    const res = await fetch(`${API_BASE}/analyze/${symbol}`);
    if (!res.ok) throw new Error();

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
      <p><b>Buy Score:</b> ${data.buy_score}</p>
      <h2 class="rec ${recClass}">${recommendation}</h2>
    `;

    renderMeter(data.buy_score);

  } catch {
    output.innerHTML = "❌ Error fetching data";
  }
}

/* =====================================
   AUTO ANALYZE
===================================== */

function autoAnalyze(symbol) {
  document.getElementById("symbol").value = symbol;
  analyzeStock();
}

/* =====================================
   MINI CHART
===================================== */

async function renderMiniChart(canvasId, symbol) {
  try {
    const res = await fetch(`${API_BASE}/prices/${symbol}`);
    if (!res.ok) throw new Error();

    const priceData = await res.json();
    if (!priceData || priceData.length === 0) return;

    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {
      type: "line",
      data: {
        labels: priceData.map(p => p.date),
        datasets: [{
          data: priceData.map(p => p.Close),
          borderColor: "#22c55e",
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { display: false },
          y: { display: false }
        }
      }
    });

  } catch (err) {
    console.log("Chart error:", symbol, err);
  }
}