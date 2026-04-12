document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get(["broncoCompanionAck"], (r) => {
    if (!r.broncoCompanionAck) {
      chrome.storage.local.set({ broncoCompanionAck: Date.now() });
    }
  });
});
