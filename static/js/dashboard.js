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
  async function updateTelemetry() {
  try {
    const response = await fetch("/api/telemetry");
    const data = await response.json();

    if (!data || data.length === 0) return;

    const latest = data[data.length - 1];

    document.getElementById("temp").textContent =
      Number(latest.temperature || 0).toFixed(1);

    document.getElementById("pressure").textContent =
      Number(latest.pressure || 0).toFixed(1);

    document.getElementById("rpm").textContent =
      Math.floor(Number(latest.rpm || 0));

    document.getElementById("vibration").textContent =
      (Math.random() * (3.2 - 1.8) + 1.8).toFixed(2);

  } catch (error) {
    console.log("Telemetry API error:", error);
  }
}
}


// =========================================
// Threat Score
// =========================================

function updateThreatScore() {
  async function updateThreatScore() {
  try {
    const response = await fetch("/api/threat-score");
    const data = await response.json();

    const scoreElement = document.getElementById("threat-score");
    const labelElement = document.getElementById("threat-label");

    scoreElement.textContent = data.score;
    labelElement.textContent = data.level;

    if (data.level === "LOW") {
      labelElement.style.color = "#00ff9d";
    } else if (data.level === "MEDIUM") {
      labelElement.style.color = "#ffc857";
    } else {
      labelElement.style.color = "#ff5c8d";
    }

  } catch (error) {
    console.log("Threat score API error:", error);
  }
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
  async function updateEvents() {
  const events = document.getElementById("events");
  if (!events) return;

  try {
    const response = await fetch("/api/events");
    const data = await response.json();

    events.innerHTML = "";

    if (!data.events || data.events.length === 0) {
      events.innerHTML = `
        <div class="event">
          <div>
            <strong>Waiting for security events...</strong><br>
            <span>Start telemetry client or run an attack simulation</span>
          </div>
        </div>
      `;
      return;
    }

    data.events.slice(-7).reverse().forEach((line) => {
      const text = String(line).trim();

      const isDanger =
        text.includes("CRITICAL") ||
        text.includes("HIGH") ||
        text.includes("Replay") ||
        text.includes("Integrity") ||
        text.includes("Unauthorized");

      const div = document.createElement("div");
      div.className = isDanger ? "event danger" : "event";

      div.innerHTML = `
        <div>
          <strong>${text}</strong><br>
          <span>Security Monitoring</span>
        </div>
      `;

      events.appendChild(div);
    });

  } catch (error) {
    console.log("Events API error:", error);

    events.innerHTML = `
      <div class="event danger">
        <div>
          <strong>Security Events API unavailable</strong><br>
          <span>Check /api/events and Flask logs</span>
        </div>
      </div>
    `;
  }
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

// =========================================
// MITRE ATT&CK
// =========================================

async function updateMITRE() {
  const mitre = document.getElementById("mitre-techniques");
  if (!mitre) return;

  try {
    const response = await fetch("/api/mitre");
    const techniques = await response.json();

    mitre.innerHTML = "";

    techniques.slice(0, 5).forEach((technique) => {
      const item = document.createElement("div");
      item.className = "mitre-item";

      item.innerHTML = `
        <strong>${technique.technique_id}</strong>
        <span>${technique.technique}</span>
      `;

      mitre.appendChild(item);
    });

  } catch (error) {
    console.log("MITRE API error:", error);
  }
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
// Incident Count
// =========================================

async function updateIncidents() {
  const count = document.getElementById("incident-count");
  if (!count) return;

  try {
    const response = await fetch("/api/incidents");
    const incidents = await response.json();

    const active = incidents.filter(
      (incident) => incident.status === "OPEN"
    );

    count.textContent = active.length;

  } catch (error) {
    console.log("Incidents API error:", error);
  }
}
// =========================================
// IOCs List
// =========================================

async function updateIOCs() {
  const container = document.getElementById("ioc-list");
  if (!container) return;

  try {
    const response = await fetch("/api/iocs");
    const iocs = await response.json();

    container.innerHTML = "";

    iocs.slice(-5).reverse().forEach((ioc) => {
      const item = document.createElement("div");
      item.className = `incident ${ioc.severity.toLowerCase()}`;

      item.innerHTML = `
        <strong>${ioc.id}</strong>
        <span>${ioc.type} · ${ioc.severity} · ${ioc.source}</span>
      `;

      container.appendChild(item);
    });

  } catch (error) {
    console.log("IOC API error:", error);
  }
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
  updateEvents();
  updateMITRE();
  updateIncidents();
  updateIOCs();

  setupReportsButton();
  setupNavigation();

  setInterval(updateClock, 1000);
  setInterval(updateTelemetry, 2000);
  setInterval(updateThreatScore, 3000);
  setInterval(updateEvents, 3500);
  setInterval(updateMITRE, 8000);
  setInterval(updateIncidents, 5000);
  setInterval(updateIOCs, 5000);
}

document.addEventListener("DOMContentLoaded", bootDashboard);