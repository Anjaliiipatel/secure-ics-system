function updateClock() {
  const clock = document.getElementById("clock");
  const now = new Date();
  clock.textContent = now.toLocaleString();
}

function randomBetween(min, max, decimals = 1) {
  return (Math.random() * (max - min) + min).toFixed(decimals);
}

function updateTelemetry() {
  document.getElementById("temp").textContent = randomBetween(68, 84, 1);
  document.getElementById("pressure").textContent = randomBetween(132, 151, 1);
  document.getElementById("rpm").textContent = Math.floor(Math.random() * (2600 - 2200) + 2200);
  document.getElementById("vibration").textContent = randomBetween(1.8, 3.1, 2);
  document.getElementById("telemetry-rate").textContent = randomBetween(9.8, 15.6, 1);
  document.getElementById("threat-score").textContent = Math.floor(Math.random() * 8 + 14);
}

const eventMessages = [
  "Telemetry received from Sensor Node 3",
  "Data integrity verified",
  "Zero Trust policy check passed",
  "Anomaly detection scan completed",
  "Sensor authentication validated",
  "Replay detection window cleared"
];

function updateEvents() {
  const events = document.getElementById("events");
  events.innerHTML = "";

  eventMessages.slice(0, 5).forEach((message) => {
    const event = document.createElement("div");
    event.className = "event";

    const time = new Date().toLocaleTimeString();

    event.innerHTML = `
      <div>
        <strong>${message}</strong><br>
        <span>Security Monitoring</span>
      </div>
      <span>${time}</span>
    `;

    events.appendChild(event);
  });
}

updateClock();
updateTelemetry();
updateEvents();

setInterval(updateClock, 1000);
setInterval(updateTelemetry, 3000);
setInterval(updateEvents, 5000);