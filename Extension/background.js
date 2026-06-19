// background.js
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  // Only scan the main website link, ignore background sub-frames/ads
  if (details.frameId !== 0) return;

  const targetUrl = details.url;

  // 🟢 1. YOUR TRUSTED WHITELIST: Add any sites here that the AI accidentally blocks
  const whitelist = [
    "ilovepdf.com",
    "github.com",
    "wikipedia.org",
    "stackoverflow.com",
  ];

  // Check if the current URL matches any domain in your whitelist
  const isWhitelisted = whitelist.some((domain) => targetUrl.includes(domain));

  // 2. Skip internal pages, search engines, and whitelisted sites
  if (
    isWhitelisted || // Bypasses the AI instantly if the site is in your whitelist
    targetUrl.includes("127.0.0.1") ||
    targetUrl.includes("localhost") ||
    targetUrl.startsWith("chrome://") ||
    targetUrl.startsWith("chrome-extension://") ||
    targetUrl.startsWith("about:") ||
    targetUrl.includes("google.com/search") ||
    targetUrl.includes("google.com/url") ||
    targetUrl.includes("bing.com/search")
  ) {
    return;
  }

  try {
    // Send URL to Python Flask Server
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: targetUrl }),
    });

    const data = await response.json();

    // Hard check: ONLY redirect if Python explicitly screams PHISHING
    if (data.status === "PHISHING") {
      chrome.tabs.update(details.tabId, {
        url:
          chrome.runtime.getURL("block.html") +
          "?url=" +
          encodeURIComponent(targetUrl),
      });
    }
  } catch (error) {
    console.error("Flask server communication error:", error);
  }
});
