const API_BASE = "https://ai-stock-platform-1.onrender.com";

async function analyzeStock() {
  const symbol = document.getElementById("symbol").value.toUpperCase();
  const output = document.getElementById("output");

  if (!symbol) {
    output.innerHTML = "Please enter a stock symbol";
    return;
  }

  // 🔄 SHOW LOADING SHIMMER
  output.innerHTML = `<div class="loading"></div>`;

  try {
    const res = await fetch(`${API_BASE}/analyze/${symbol}`);
    const data = await res.json();

    let recommendation =
      data.buy_score >= 75 ? "STRONG BUY" :
      data.buy_score >= 60 ? "BUY" :
      data.buy_score >= 45 ? "HOLD" : "SELL";

    output.innerHTML = `
      <h3>${symbol}</h3>
      <p><b>Prediction:</b> ${data.prediction}</p>
      <p><b>Sentiment:</b> ${data.sentiment}</p>
      <p><b>Buy Score:</b> ${data.buy_score}</p>
      <h2 class="rec">${recommendation}</h2>
    `;

    renderMeter(data.buy_score);

  } catch (err) {
    output.innerHTML = "❌ Error fetching data";
  }
}
