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
      tokenName: s?.tokenName ?? null,
      tokenDesc: s?.tokenDesc ?? null,
      tokenTimestamp: s?.tokenTimestamp ?? null,
      triggerUrl: s?.triggerUrl ?? null,
      isActive: s?.isActive ?? null,
    });

    if (!s?.tokenId) return;

    component.applyTokenContext(
      s.tokenId,
      s.tokenType,
      s.tokenName,
      s.tokenDesc,
      s.tokenTimestamp,
      s.triggerUrl,
      s.isActive,
    );
  };

  syncFromStore();

  component.$watch(
    () => [
      component.$store.tokenEventsModal.tokenId,
      component.$store.tokenEventsModal.tokenType,
      component.$store.tokenEventsModal.tokenName,
      component.$store.tokenEventsModal.tokenDesc,
      component.$store.tokenEventsModal.tokenTimestamp,
      component.$store.tokenEventsModal.triggerUrl,
      component.$store.tokenEventsModal.isActive,
    ],
    (
      [tokenId, tokenType, tokenName, tokenDesc, tokenTimestamp, triggerUrl, isActive],
      [prevTokenId, prevTokenType, prevTokenName, prevTokenDesc, prevTokenTimestamp, prevTriggerUrl, prevIsActive] = []
    ) => {
      log("tokenEvents", "store watcher fired", {
        prev: {
          tokenId: prevTokenId ?? null,
          tokenType: prevTokenType ?? null,
          tokenName: prevTokenName ?? null,
          tokenDesc: prevTokenDesc ?? null,
          tokenTimestamp: prevTokenTimestamp ?? null,
          triggerUrl: prevTriggerUrl ?? null,
          isActive: prevIsActive ?? null,
        },
        next: {
          tokenId: tokenId ?? null,
          tokenType: tokenType ?? null,
          tokenName: tokenName ?? null,
          tokenDesc: tokenDesc ?? null,
          tokenTimestamp: tokenTimestamp ?? null,
          triggerUrl: triggerUrl ?? null,
          isActive: isActive ?? null,
        },
      });

      if (!tokenId) return;

      component.applyTokenContext(
        tokenId,
        tokenType,
        tokenName,
        tokenDesc,
        tokenTimestamp,
        triggerUrl,
        isActive
      );
    }
  );
}