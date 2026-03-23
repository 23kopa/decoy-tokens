import { log, warn } from "../../shared/utils/logger.js";

export function registerTokenEventsModalStore(Alpine) {
  Alpine.store("tokenEventsModal", {
    tokenId: null,
    tokenName: null,
    tokenType: null,
    tokenTimestamp: null,
    triggerUrl: null,
    isActive: null,

    set(
      tokenId, 
      tokenType, 
      tokenName, 
      triggerUrl = null, 
      isActive = null, 
      tokenTimestamp = null
    ) {
      
      this.tokenId = tokenId;
      this.tokenType = tokenType;
      this.tokenName = tokenName;
      this.triggerUrl = triggerUrl;
      this.isActive = isActive;
      this.tokenTimestamp = tokenTimestamp;

      log("store", "tokenEventsModal updated", {
        tokenId: this.tokenId,
        tokenType: this.tokenType,
        tokenName: this.tokenName,
        tokenTimestamp: this.tokenTimestamp,
        triggerUrl: this.triggerUrl,
        isActive: this.isActive,
      });
    },

    clear() {
      this.tokenId = null;
      this.tokenName = null;
      this.tokenType = null;
      this.triggerUrl = null;
      this.isActive = null;
      this.tokenTimestamp = null;

      log("store", "tokenEventsModal cleared");
    },
  });
}