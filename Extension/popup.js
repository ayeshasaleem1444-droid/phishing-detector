document.getElementById("scanBtn").addEventListener("click", async () => {
  const resultDiv = document.getElementById("result");
  const statusText = document.getElementById("statusText");
  const reasonText = document.getElementById("reasonText");

  // 1. Get the URL of the active browser tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url) {
    statusText.innerText = "Error: Cannot read URL";
    resultDiv.className = "phishing";
    resultDiv.style.display = "block";
    return;
  }

  statusText.innerText = "Scanning URL with AI...";
  resultDiv.className = "";
  resultDiv.style.display = "block";
  reasonText.innerText = "";

  try {
    // 2. Send the URL to your local Python Flask API server
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: tab.url }),
    });

    const data = await response.json();

    // 3. Display the results inside the extension popup window
    if (data.status === "SAFE") {
      resultDiv.className = "safe";
      statusText.innerText = `🟢 SAFE (${data.confidence}%)`;
    } else {
      resultDiv.className = "phishing";
      statusText.innerText = `🚨 PHISHING (${data.confidence}%)`;
    }

    reasonText.innerText = data.reason;
  } catch (error) {
    // Triggers if your Flask python server is turned off
    statusText.innerText = "Error: Python API server is offline!";
    resultDiv.className = "phishing";
    reasonText.innerText = "Make sure to run 'python app.py' in your terminal.";
  }
});
