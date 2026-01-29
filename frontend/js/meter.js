let currentValue = 0;

function renderMeter(value) {
  // ✅ Decide color based on buy score
  const color =
    value >= 65 ? "#22c55e" :   // BUY → green
    value >= 40 ? "#facc15" :   // HOLD → yellow
                  "#ef4444";    // SELL → red

  const canvas = document.getElementById("meter");
  const ctx = canvas.getContext("2d");

  const target = Math.min(100, Math.max(0, Math.round(value)));

  // ✅ RESET animation when new value comes
  currentValue = 0;

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    /* Background arc */
    ctx.beginPath();
    ctx.arc(100, 100, 70, Math.PI, 2 * Math.PI);
    ctx.lineWidth = 14;
    ctx.strokeStyle = "#1e293b";
    ctx.stroke();

    /* Animated progress arc */
    const angle = Math.PI + (currentValue / 100) * Math.PI;
    ctx.beginPath();
    ctx.arc(100, 100, 70, Math.PI, angle);
    ctx.lineWidth = 14;
    ctx.strokeStyle = color; // 🔥 COLOR CHANGE APPLIED
    ctx.stroke();
    ctx.shadowBlur = 20;
    ctx.shadowColor = color;

    /* Percentage text */
    ctx.fillStyle = color;
    ctx.font = "bold 20px Segoe UI";
    ctx.textAlign = "center";
    ctx.fillText(`${currentValue}%`, 100, 105);

    if (currentValue < target) {
      currentValue += 1;
      requestAnimationFrame(animate);
    }
  }

  animate();
}
