/* Opt-in extension spike: no scraping or network calls. */
(function () {
  if (window.__AGENT_BRONCOS_EXT__) return;
  window.__AGENT_BRONCOS_EXT__ = true;
  try {
    document.documentElement.dataset.agentBroncosCompanion = "1";
  } catch (e) {
    void e;
  }
})();
