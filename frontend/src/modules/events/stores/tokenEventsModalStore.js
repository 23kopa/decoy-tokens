import { log, warn } from "../../shared/utils/logger.js";

export function registerTokenEventsModalStore(Alpine) {
  Alpine.store("tokenEventsModal", {
    tokenId: null,
    tokenType: null,
    tokenName: null,
    tokenDesc: null,
    tokenTimestamp: null,
    triggerUrl: null,
    isActive: null,

    set(
      tokenId, 
      tokenType, 
      tokenName, 
      tokenDesc = null,
      triggerUrl = null, 
      isActive = null, 
      tokenTimestamp = null
    ) {
      
      this.tokenId = tokenId;
      this.tokenType = tokenType;
      this.tokenName = tokenName;
      this.tokenDesc = tokenDesc;
      this.triggerUrl = triggerUrl;
      this.isActive = isActive;
      this.tokenTimestamp = tokenTimestamp;

      log("store", "tokenEventsModal updated", {
        tokenId: this.tokenId,
        tokenType: this.tokenType,
        tokenName: this.tokenName,
        tokenDesc: this.tokenDesc,
        
        tokenTimestamp: this.tokenTimestamp,
        triggerUrl: this.triggerUrl,
        isActive: this.isActive,
      });
    },

    clear() {
      this.tokenId = null;
      this.tokenType = null;
      this.tokenName = null;
      this.tokenDesc = null;
      this.triggerUrl = null;
      this.isActive = null;
      this.tokenTimestamp = null;

      log("store", "tokenEventsModal cleared");
    },
  });
}

export function registerTokenCardsStore(Alpine) {
  // Создаём store для хранения статусов всех карточек
  Alpine.store('tokenCards', {
    items: {},

    updateStatus(tokenId, isActive) {
      if (this.items[tokenId]) {
        this.items[tokenId].isActive = isActive;
        log('tokenCards', 'status updated', { tokenId, isActive });
      }
    },
  });
  
  // Слушаем глобальное событие обновления статуса из модалки
  document.addEventListener('token-status-changed', (e) => {
    const { tokenId, isActive } = e.detail;
    const store = Alpine.store('tokenCards');
    store.updateStatus(tokenId, isActive);
  });
}