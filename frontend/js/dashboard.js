const API_BASE = "https://ai-stock-platform-zpkg.onrender.com";

const DEFAULT_STOCKS = [
  "AAPL", "MSFT", "TSLA", "NVDA",
  "RELIANCE.NS", "TCS.NS",
  "GC=F", "SI=F",
  "^NSEI", "^BSESN"
];

let expandedChartInstance = null;


/* =====================================================
   LOGO + SYMBOL FORMAT
===================================================== */
function getLogo(sym) {

  const logoMap = {

    // US
    AAPL: "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/apple.svg",
    MSFT: "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/microsoft.svg",
    TSLA: "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/tesla.svg",
    NVDA: "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/nvidia.svg",

    // India
    RELIANCE: "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/relianceindustrieslimited.svg",
    TCS: "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/tata.svg",

    // Commodities
    "GC=F": "https://img.icons8.com/color/48/gold-bars.png",
    "SI=F": "https://img.icons8.com/color/48/silver-bars.png",

    // Indices
    "^NSEI": "https://cdn-icons-png.flaticon.com/512/2991/2991148.png",
    "^BSESN": "https://cdn-icons-png.flaticon.com/512/2991/2991148.png"
  };

  const clean = sym.replace(".NS", "");
  return logoMap[clean] || 
         "https://cdn-icons-png.flaticon.com/512/2991/2991148.png";
}

function formatSymbol(sym) {
  if (sym === "^BSESN") return "SENSEX";
  if (sym === "^NSEI") return "NIFTY 50";
  if (sym === "GC=F") return "GOLD";
  if (sym === "SI=F") return "SILVER";
  return sym.replace(".NS", "");
}

function safeId(sym) {
  return sym.replace(/[^a-zA-Z0-9]/g, "");
}


/* =====================================================
   ON LOAD
===================================================== */
document.addEventListener("DOMContentLoaded", () => {
  loadDefaultStocks();
  loadMarketSentiment();
  loadMarketNews();
});


/* =====================================================
   LOAD MARKET OVERVIEW
===================================================== */
async function loadDefaultStocks() {

  const container = document.getElementById("default-stocks");
  container.innerHTML = "";

  for (const sym of DEFAULT_STOCKS) {

    const id = safeId(sym);

    const card = document.createElement("div");
    card.className = "stock-card";
    card.onclick = () => expandChart(sym);

    card.innerHTML = `
      <div class="card-header">
        <img src="${getLogo(sym)}"
             class="stock-logo"
             onerror="this.src='https://cdn-icons-png.flaticon.com/512/2991/2991148.png'"/>
        <h3>${formatSymbol(sym)}</h3>
      </div>

      <div class="mini-chart">
        <canvas id="chart-${id}"></canvas>
      </div>

      <div class="expanded-info">
        <p class="news">Loading latest news...</p>
      </div>

      <p class="mini-signal loading">Loading...</p>
    `;

    container.appendChild(card);

    renderMiniChart(`chart-${id}`, sym);

    /* LOAD SIGNAL */
    fetch(`${API_BASE}/analyze/${sym}`)
      .then(res => res.json())
      .then(data => {
        const signalEl = card.querySelector(".mini-signal");

        if (!data.signal) throw new Error();

        signalEl.textContent = data.signal;
        signalEl.className = "mini-signal " + data.signal;
      })
      .catch(() => {
        const signalEl = card.querySelector(".mini-signal");
        signalEl.textContent = "HOLD";
        signalEl.className = "mini-signal HOLD";
      });

    /* LOAD NEWS */
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


/* =====================================================
   MARKET SENTIMENT
===================================================== */
async function loadMarketSentiment() {

  const el = document.getElementById("market-sentiment");

  try {
    const res = await fetch(`${API_BASE}/market-sentiment`);
    const data = await res.json();
    el.textContent = `${data.mood} (${data.value})`;
  } catch {
    el.textContent = "Unavailable";
  }
}


/* =====================================================
   MARKET NEWS
===================================================== */
async function loadMarketNews() {

  const container = document.getElementById("market-news");

  try {
    const res = await fetch(`${API_BASE}/market-news`);
    const data = await res.json();

    if (!data.headlines || data.headlines.length === 0) {
      container.textContent = "No major market news.";
      return;
    }

    container.innerHTML = data.headlines
      .slice(0, 5)
      .map(h => `<div class="news-item">• ${h}</div>`)
      .join("");

  } catch {
    container.textContent = "News unavailable.";
  }
}


/* =====================================================
   SEARCH ANALYSIS
===================================================== */
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


/* =====================================================
   MINI CHART
===================================================== */
async function renderMiniChart(canvasId, symbol) {

  try {
    const res = await fetch(`${API_BASE}/prices/${symbol}`);
    const rawData = await res.json();
    const data = rawData.filter(p => p.Close && p.Close > 0);

    const ctx = document.getElementById(canvasId).getContext("2d");

    new Chart(ctx, {
      type: "line",
      data: {
        labels: data.map(p => p.date),
        datasets: [{
          data: data.map(p => p.Close),
          borderColor: "#22c55e",
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { display: false }, y: { display: false } }
      }
    });

  } catch (err) {
    console.log("Mini chart error:", err);
  }
}


/* =====================================================
   EXPANDED CHART
===================================================== */
async function expandChart(symbol) {

  const modal = document.getElementById("chart-modal");
  modal.classList.add("active");

  try {

    const res = await fetch(`${API_BASE}/prices/${symbol}`);
    const rawData = await res.json();
    const data = rawData.filter(p => p.Close && p.Close > 0);

    const ctx = document.getElementById("expanded-chart").getContext("2d");

    if (expandedChartInstance) expandedChartInstance.destroy();

    expandedChartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels: data.map(p => p.date),
        datasets: [{
          label: `${formatSymbol(symbol)} Price`,
          data: data.map(p => p.Close),
          borderColor: "#22c55e",
          borderWidth: 2,
          tension: 0.3,
          pointRadius: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { color: "#e5e7eb" } }
        },
        scales: {
          x: { ticks: { color: "#94a3b8" } },
          y: { ticks: { color: "#94a3b8" } }
        }
      }
    });

  } catch (err) {
    console.log("Expanded chart error:", err);
  }
}

function closeModal() {
  document.getElementById("chart-modal").classList.remove("active");
}