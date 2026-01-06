const API_URL = "http://127.0.0.1:5000/predict";

const btn = document.getElementById("predict");
const status = document.getElementById("status");

const resultBox = document.getElementById("result");
const difficultyEl = document.getElementById("result-difficulty");
const scoreEl = document.getElementById("result-score");

function extractProblemFields() {
  const root = document.querySelector(".problem-statement");
  if (!root) return null;

  const title =
    root.querySelector(".header .title")?.innerText.trim() || "";

  const input_description =
    root.querySelector(".input-specification")?.innerText.trim() || "";

  const output_description =
    root.querySelector(".output-specification")?.innerText.trim() || "";

  const sample_io = Array.from(
    root.querySelectorAll(".sample-test")
  )
    .map(s => s.innerText.trim())
    .join("\n\n");

  const cloned = root.cloneNode(true);
  cloned.querySelector(".input-specification")?.remove();
  cloned.querySelector(".output-specification")?.remove();
  cloned.querySelectorAll(".sample-test").forEach(e => e.remove());

  const description = cloned.innerText.trim();

  return {
    title,
    description,
    input_description,
    output_description,
    sample_io
  };
}

btn.onclick = async () => {
  status.innerText = "Extracting problem text...";
  resultBox.style.display = "none";

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true
    });

    const [{ result }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: extractProblemFields
    });

    if (!result) {
      throw new Error("Failed to extract problem fields");
    }

    status.innerText = "Calling prediction API...";

    const resp = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(result)
    });

    if (!resp.ok) {
      throw new Error(`API error: ${resp.status}`);
    }

    const data = await resp.json();
    console.log("API response:", data);

    const cls = data.predicted_class.toLowerCase();

    difficultyEl.innerHTML =
      `<span class="badge ${cls}">${data.predicted_class}</span>`;

    scoreEl.innerText = (data.predicted_score*10).toFixed(2);

    resultBox.style.display = "flex";
    status.innerText = "";

  } catch (err) {
    status.innerText = "";
    resultBox.style.display = "none";
    alert(`Error: ${err.message}`);
    console.error(err);
  }
};
