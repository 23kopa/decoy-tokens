import { tokensApi } from "../../shared/utils/api.js";
import { log } from "../../shared/utils/logger.js";

export async function fetchTokenEventsData(tokenId) {
  const [events, stats] = await Promise.all([
    tokensApi.get(`/tokens/${tokenId}/events?limit=50`),
    tokensApi.get(`/tokens/${tokenId}/events/stats`).catch(() => null),
  ]);

  return {
    events: Array.isArray(events) ? events : [],
    stats: stats || null,
  };
}

export function bindTokenEventsModalState(component) {
  const syncFromStore = () => {
    const s = component.$store?.tokenEventsModal;

    log("tokenEvents", "syncFromStore called", {
      tokenId: s?.tokenId ?? null,
      tokenType: s?.tokenType ?? null,
      tokenTimestamp: s?.tokenTimestamp ?? null,
      triggerUrl: s?.triggerUrl ?? null,
      isActive: s?.isActive ?? null,
      tokenName: s?.tokenName ?? null,
    });

    if (!s?.tokenId) return;

    component.applyTokenContext(
      s.tokenId,
      s.tokenType,
      s.triggerUrl,
      s.isActive,
      s.tokenName,
      s.tokenTimestamp
    );
  };

  syncFromStore();

  component.$watch(
    () => [
      component.$store.tokenEventsModal.tokenId,
      component.$store.tokenEventsModal.tokenType,
      component.$store.tokenEventsModal.tokenName,
      component.$store.tokenEventsModal.triggerUrl,
      component.$store.tokenEventsModal.isActive,
      component.$store.tokenEventsModal.tokenTimestamp,
    ],
    ([tokenId, tokenType, tokenName, triggerUrl, isActive, tokenTimestamp], [prevTokenId, prevTokenType, prevTokenName, prevTriggerUrl, prevIsActive, prevTokenTimestamp] = []) => {
      log("tokenEvents", "store watcher fired", {
        prev: {
          tokenId: prevTokenId ?? null,
          tokenType: prevTokenType ?? null,
          tokenName: prevTokenName ?? null,
          triggerUrl: prevTriggerUrl ?? null,
          tokenTimestamp: prevTokenTimestamp ?? null,
        },
        next: {
          tokenId: tokenId ?? null,
          tokenName: tokenName ?? null,
          tokenType: tokenType ?? null,
          triggerUrl: triggerUrl ?? null,
          isActive: isActive ?? null,
          tokenTimestamp: tokenTimestamp ?? null,
        },
      });

      if (!tokenId) return;

      component.applyTokenContext(tokenId, tokenType, tokenName, triggerUrl, isActive, tokenTimestamp);
    }
  );
}