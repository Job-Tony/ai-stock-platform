const API_BASE = "https://ai-stock-platform-zpkg.onrender.com";
const DEFAULT_STOCKS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOGL"];

async function analyze() {
  const sym = document.getElementById("symbol").value.toUpperCase();

  if (!sym) {
    alert("Please enter a stock symbol");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/analyze/${sym}`);
    if (!res.ok) throw new Error("API error");

    const data = await res.json();

    document.getElementById("result").innerHTML = `
      <p><b>Signal:</b> ${data.signal}</p>
      <p><b>Buy Score:</b> ${data.buy_score}</p>
      <p><b>Confidence:</b> ${data.confidence}%</p>
    `;

    renderMeter(Number(data.buy_score)); // 🔥 normalized meter
  } catch (err) {
    document.getElementById("result").innerHTML =
      "⚠️ Server waking up… please try again in a few seconds";
  }
}
