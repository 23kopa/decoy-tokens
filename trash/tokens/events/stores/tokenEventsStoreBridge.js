import { log, warn } from "../../shared/utils/logger.js";

export function initEventsBridge() {
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(
      'button[data-modal-toggle="token-events-modal"][data-token-id]'
    );
    if (!btn) return;

    const tokenId = btn.dataset.tokenId;
    const tokenName = btn.dataset.tokenName || null;
    const tokenType = btn.dataset.tokenType || null;
    const tokenTimestamp = btn.dataset.tokenTimestamp || null;
    const triggerUrl = btn.dataset.triggerUrl || null;
    const isActive = btn.dataset.tokenActive === "true";

    log("eventsBridge", "modal trigger clicked", {
      tokenId,
      tokenName,
      tokenType,
      tokenTimestamp,
      triggerUrl,
      isActive,
      dataset: { ...btn.dataset },
    });

    const store = window.Alpine?.store("tokenEventsModal");
    if (!store) {
      warn("eventsBridge", "tokenEventsModal store not found");
      return;
    }

    store.set(tokenId, tokenType, tokenName, triggerUrl, isActive, tokenTimestamp);
  });
}