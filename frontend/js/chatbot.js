const API_BASE = "https://ai-stock-platform-zpkg.onrender.com";

async function sendMessage() {
  const input = document.getElementById("userMessage");
  const chatBox = document.getElementById("chatBox");

  const message = input.value.trim();
  if (!message) return;

  chatBox.innerHTML += `<div class="user-msg">🧑 ${message}</div>`;
  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    if (!res.ok) throw new Error("Backend error");

    const data = await res.json();

    chatBox.innerHTML += `<div class="bot-msg">🤖 ${data.reply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (err) {
    chatBox.innerHTML += `<div class="error-msg">❌ Chatbot unavailable</div>`;
  }
}
