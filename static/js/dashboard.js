// =========================================
// Secure ICS SOC Dashboard
// dashboard.js
// =========================================

function updateClock() {
  const clock = document.getElementById("clock");

  if (!clock) return;

  const now = new Date();
  clock.textContent = now.toLocaleString();
}

function randomBetween(min, max, decimals = 1) {
  return (Math.random() * (max - min) + min).toFixed(decimals);
}

// =========================================
// Live Telemetry
// =========================================

function updateTelemetry() {
  const temp = document.getElementById("temp");
  const pressure = document.getElementById("pressure");
  const rpm = document.getElementById("rpm");
  const vibration = document.getElementById("vibration");

  if (temp) temp.textContent = randomBetween(68, 84, 1);
  if (pressure) pressure.textContent = randomBetween(135, 150, 1);
  if (rpm) rpm.textContent = Math.floor(Math.random() * (2600 - 2200) + 2200);
  if (vibration) vibration.textContent = randomBetween(1.8, 3.2, 2);
}

// =========================================
// Threat Score
// =========================================

function updateThreatScore() {
  const scoreElement = document.getElementById("threat-score");
  const labelElement = document.getElementById("threat-label");

  if (!scoreElement || !labelElement) return;

  const score = Math.floor(Math.random() * 70 + 12);

  scoreElement.textContent = score;

  if (score < 30) {
    labelElement.textContent = "LOW";
    labelElement.style.color = "#00ff9d";
  } else if (score < 55) {
    labelElement.textContent = "MEDIUM";
    labelElement.style.color = "#ffc857";
  } else {
    labelElement.textContent = "HIGH";
    labelElement.style.color = "#ff5c8d";
  }
}

// =========================================
// Attack Monitor
// =========================================

const attackStates = [
  {
    title: "No Active Attacks",
    subtitle: "Security Gateway is monitoring telemetry traffic.",
    badge: "0 Active",
    shield: "✓"
  },
  {
    title: "Replay Attack Blocked",
    subtitle: "Replay detector rejected duplicated telemetry.",
    badge: "1 Active",
    shield: "!"
  },
  {
    title: "Unauthorized Sensor",
    subtitle: "Authentication policy rejected rogue device.",
    badge: "1 Active",
    shield: "!"
  },
  {
    title: "Telemetry Tampering",
    subtitle: "HMAC integrity validation failed.",
    badge: "1 Active",
    shield: "!"
  },
  {
    title: "Flood Pattern Logged",
    subtitle: "High-volume telemetry pattern detected.",
    badge: "2 Active",
    shield: "!"
  }
];

function updateAttackMonitor() {
  const title = document.getElementById("attack-title");
  const subtitle = document.getElementById("attack-subtitle");
  const status = document.getElementById("attack-status");
  const shield = document.querySelector(".shield");

  if (!title || !subtitle || !status) return;

  const attack = attackStates[Math.floor(Math.random() * attackStates.length)];

  title.textContent = attack.title;
  subtitle.textContent = attack.subtitle;
  status.textContent = attack.badge;

  if (shield) {
    shield.textContent = attack.shield;
  }
}

// =========================================
// Security Events
// =========================================

const normalEvents = [
  "Telemetry packet validated by Security Gateway",
  "HMAC-SHA256 integrity verification passed",
  "Sensor authentication validated",
  "Replay detection window cleared",
  "Anomaly detection scan completed",
  "Threat score recalculated",
  "MITRE ATT&CK mapping updated",
  "Incident queue synchronized",
  "Security report engine ready",
  "Controller API health check passed"
];

const attackEvents = [
  "Replay Attack blocked",
  "Unauthorized Sensor rejected",
  "Integrity Failure detected",
  "Telemetry Anomaly generated",
  "Flooding pattern logged",
  "Tampered packet rejected"
];

function createEvent(message, isDanger = false) {
  const event = document.createElement("div");
  event.className = isDanger ? "event danger" : "event";

  const time = new Date().toLocaleTimeString();

  event.innerHTML = `
    <div>
      <strong>${message}</strong><br>
      <span>Security Monitoring</span>
    </div>
    <span>${time}</span>
  `;

  return event;
}

function updateEvents() {
  const events = document.getElementById("events");

  if (!events) return;

  const isDanger = Math.random() > 0.72;

  const message = isDanger
    ? attackEvents[Math.floor(Math.random() * attackEvents.length)]
    : normalEvents[Math.floor(Math.random() * normalEvents.length)];

  events.prepend(createEvent(message, isDanger));

  while (events.children.length > 7) {
    events.removeChild(events.lastChild);
  }
}

// =========================================
// MITRE ATT&CK
// =========================================

const mitreTechniques = [
  ["T1557", "Adversary-in-the-Middle"],
  ["T1565", "Data Manipulation"],
  ["T1036", "Masquerading"],
  ["T1499", "Endpoint DoS"],
  ["T0831", "Manipulation of Control"]
];

function updateMITRE() {
  const mitre = document.getElementById("mitre-techniques");

  if (!mitre) return;

  mitre.innerHTML = "";

  mitreTechniques.forEach(([id, name]) => {
    const item = document.createElement("div");
    item.className = "mitre-item";

    item.innerHTML = `
      <strong>${id}</strong>
      <span>${name}</span>
    `;

    mitre.appendChild(item);
  });
}

// =========================================
// Incident Count
// =========================================

function updateIncidentCount() {
  const count = document.getElementById("incident-count");

  if (!count) return;

  count.textContent = Math.floor(Math.random() * 5 + 1);
}

// =========================================
// Reports Button
// =========================================

function setupReportsButton() {
  const button = document.getElementById("generate-report");
  const status = document.getElementById("report-status");

  if (!button || !status) return;

  button.addEventListener("click", () => {
    status.textContent = "Generating reports...";

    setTimeout(() => {
      const now = new Date().toLocaleTimeString();
      status.textContent = `Reports generated successfully at ${now}.`;
    }, 800);
  });
}

// =========================================
// Sidebar Active Link
// =========================================

function setupNavigation() {
  const links = document.querySelectorAll("nav a");

  links.forEach((link) => {
    link.addEventListener("click", () => {
      links.forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
    });
  });
}

// =========================================
// Boot
// =========================================

function bootDashboard() {
  updateClock();
  updateTelemetry();
  updateThreatScore();
  updateAttackMonitor();
  updateEvents();
  updateMITRE();
  updateIncidentCount();

  setupReportsButton();
  setupNavigation();

  setInterval(updateClock, 1000);
  setInterval(updateTelemetry, 2000);
  setInterval(updateThreatScore, 3000);
  setInterval(updateAttackMonitor, 5000);
  setInterval(updateEvents, 3500);
  setInterval(updateIncidentCount, 4500);
  setInterval(updateMITRE, 8000);
}

document.addEventListener("DOMContentLoaded", bootDashboard);