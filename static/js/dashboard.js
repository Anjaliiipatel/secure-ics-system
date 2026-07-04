// =========================================
// Secure ICS SOC Dashboard
// dashboard.js
// =========================================

function updateClock() {
    const clock = document.getElementById("clock");

    if (!clock) return;

    const now = new Date();

    clock.innerHTML = now.toLocaleString();
}

// =========================================

function random(min, max, decimals = 1) {
    return (
        Math.random() * (max - min) + min
    ).toFixed(decimals);
}

// =========================================
// Live Telemetry
// =========================================

function updateTelemetry() {

    document.getElementById("temp").innerHTML =
        random(68, 84);

    document.getElementById("pressure").innerHTML =
        random(135, 150);

    document.getElementById("rpm").innerHTML =
        Math.floor(
            Math.random() * (2600 - 2200) + 2200
        );

    document.getElementById("vibration").innerHTML =
        random(1.8, 3.2, 2);
}

// =========================================
// Threat Score
// =========================================

function updateThreatScore() {

    const score = Math.floor(
        Math.random() * 60 + 10
    );

    document.getElementById("threat-score").innerHTML =
        score;

    const label =
        document.getElementById("threat-label");

    if (score < 25) {

        label.innerHTML = "LOW";

        label.style.color = "#00ff9d";

    }

    else if (score < 50) {

        label.innerHTML = "MEDIUM";

        label.style.color = "#ffc857";

    }

    else {

        label.innerHTML = "HIGH";

        label.style.color = "#ff5c8d";

    }
}

// =========================================
// Attack Monitor
// =========================================

const attackStates = [

    {
        title: "No Active Attacks",
        subtitle: "Security Gateway monitoring telemetry.",
        badge: "0 Active"
    },

    {
        title: "Replay Attack Blocked",
        subtitle: "Replay detector rejected duplicated telemetry.",
        badge: "1 Active"
    },

    {
        title: "Unauthorized Sensor",
        subtitle: "Authentication policy rejected rogue node.",
        badge: "2 Active"
    },

    {
        title: "Telemetry Tampering",
        subtitle: "Integrity validation failed.",
        badge: "1 Active"
    }

];

function updateAttackMonitor() {

    const attack =
        attackStates[
            Math.floor(
                Math.random() *
                attackStates.length
            )
        ];

    document.getElementById("attack-title")
        .innerHTML = attack.title;

    document.getElementById("attack-subtitle")
        .innerHTML = attack.subtitle;

    document.getElementById("attack-status")
        .innerHTML = attack.badge;
}

// =========================================
// Recent Security Events
// =========================================

const events = [

    "Telemetry packet validated",

    "Replay attack detected",

    "Threat score updated",

    "Sensor authenticated",

    "MITRE ATT&CK mapping generated",

    "Incident queue synchronized",

    "Integrity validation passed",

    "Telemetry anomaly detected",

    "Flood attack blocked",

    "Security report generated"

];

function updateEvents() {

    const container =
        document.getElementById("events");

    if (!container) return;

    const event =
        events[
            Math.floor(
                Math.random() *
                events.length
            )
        ];

    const time =
        new Date().toLocaleTimeString();

    const div =
        document.createElement("div");

    div.className = "event";

    div.innerHTML = `
        <div>
            <strong>${event}</strong><br>
            <span>Security Monitoring</span>
        </div>

        <span>${time}</span>
    `;

    container.prepend(div);

    while (container.children.length > 6) {

        container.removeChild(
            container.lastChild
        );

    }

}

// =========================================
// MITRE ATT&CK
// =========================================

const mitre = [

    {
        id: "T1557",
        name: "Adversary-in-the-Middle"
    },

    {
        id: "T1565",
        name: "Data Manipulation"
    },

    {
        id: "T1499",
        name: "Endpoint DoS"
    },

    {
        id: "T1036",
        name: "Masquerading"
    },

    {
        id: "T0831",
        name: "Manipulation of Control"
    }

];

function updateMITRE() {

    const container =
        document.getElementById(
            "mitre-techniques"
        );

    if (!container) return;

    container.innerHTML = "";

    mitre.forEach(item => {

        container.innerHTML += `

        <div class="mitre-item">

            <strong>${item.id}</strong>

            <span>${item.name}</span>

        </div>

        `;

    });

}

// =========================================
// Incident Counter
// =========================================

function updateIncidents() {

    const count =
        Math.floor(
            Math.random() * 6
        );

    document.getElementById(
        "incident-count"
    ).innerHTML = count;

}

// =========================================
// Boot
// =========================================

updateClock();

updateTelemetry();

updateThreatScore();

updateAttackMonitor();

updateEvents();

updateMITRE();

updateIncidents();

// =========================================

setInterval(updateClock, 1000);

setInterval(updateTelemetry, 2000);

setInterval(updateThreatScore, 3000);

setInterval(updateAttackMonitor, 5000);

setInterval(updateEvents, 3500);

setInterval(updateIncidents, 4000);

setInterval(updateMITRE, 8000);