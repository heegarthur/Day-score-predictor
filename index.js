function loadData() {
    return JSON.parse(localStorage.getItem("dayscores") || "[]");
}

function saveData(data) {
    localStorage.setItem("dayscores", JSON.stringify(data));
}

function dayOfYear(date) {
    const start = new Date(date.getFullYear(), 0, 0);
    const diff = date - start;
    return Math.floor(diff / 86400000);
}

function getMonth(dayOfYear) {
    const date = new Date(new Date().getFullYear(), 0);
    date.setDate(dayOfYear);
    return date.getMonth() + 1;
}

function getSeason(month) {
    if ([3, 4, 5].includes(month)) return 0;
    if ([6, 7, 8].includes(month)) return 1;
    if ([9, 10, 11].includes(month)) return 2;
    return 3;
}

function getWeekday(dayOfYear) {
    const date = new Date(new Date().getFullYear(), 0);
    date.setDate(dayOfYear);
    return date.getDay();
}

function predictBest(targetDay, data) {
    if (data.length === 0) return null;

    const m = getMonth(targetDay);
    const s = getSeason(m);
    const w = getWeekday(targetDay);
    const target = [m / 12, s / 3, w / 6];

    let bestScore = null;
    let bestDist = Infinity;

    for (let d of data) {
        const month = getMonth(d.day);
        const season = getSeason(month);
        const weekday = getWeekday(d.day);
        const vec = [month / 12, season / 3, weekday / 6];
        const dist = Math.sqrt(vec.map((v, i) => (v - target[i]) ** 2).reduce((a, b) => a + b, 0));

        if (dist < bestDist || (dist === bestDist && d.score > bestScore)) {
            bestDist = dist;
            bestScore = d.score;
        }
    }
    return bestScore;
}

function saveDay() {
    let score = parseInt(document.getElementById("score").value);
    let text = document.getElementById("text").value;
    let today = dayOfYear(new Date());

    if (!score || score < 1 || score > 100) {
        alert("Enter a score (1-100).");
        return;
    }

    const data = loadData();
    data.push({ day: today, score: score, text: text });
    saveData(data);

    document.getElementById("output").innerText = "Day saved";
    document.getElementById("score").value = 0;
    document.getElementById("text").value = "";
    console.log("e")
}

function predict(offset) {
    const today = dayOfYear(new Date());
    const targetDay = today + offset;
    const data = loadData();
    const prediction = predictBest(targetDay, data);

    if (prediction !== null) {
        document.getElementById("output").innerText = `Best match for day ${targetDay}: ${prediction}/100`;
    } else {
        document.getElementById("output").innerText = "No data to use!";
    }
}

function predictShift() {
    const today = dayOfYear(new Date());
    const input = document.getElementById("dayshift").value.trim();
    if (!input) return;
    const shift = parseInt(input);
    const targetDay = today + shift;

    const data = loadData();
    const prediction = predictBest(targetDay, data);

    if (prediction !== null) {
        document.getElementById("output").innerText = `Best match for day ${targetDay}: ${prediction}/100`;
    } else {
        document.getElementById("output").innerText = "No data to use!";
    }
}

function downloadCSV() {
  const data = JSON.parse(localStorage.getItem("dayscores") || "[]");
  if (data.length === 0) {
    alert("No data to download!");
    return;
  }

  let csv = "day,score,text\n";
  data.forEach(item => {
    const line = `${item.day},${item.score},"${item.text.replace(/"/g, '""')}"`;
    csv += line + "\n";
  });

  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "dayscores.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  URL.revokeObjectURL(url);
}