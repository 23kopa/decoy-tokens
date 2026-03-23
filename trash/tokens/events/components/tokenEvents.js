import { log, error as logError, group } from "../../shared/utils/logger.js";
import { copyText, openUrl } from "../../shared/utils/clipboard.js";
import { tokensApi } from "../../shared/utils/api.js";
import { fetchTokenEventsData, bindTokenEventsModalState } from "../services/eventTokenService.js";
import {
  formatEventDate,
  formatEventIP,
  formatEventUserAgent,
  getEventIcon,
  getEventStatusColor,
  getFlagEmoji,
} from "../utils/eventPresentation.js";

export function tokenEvents() {
  return {
    tokenId: null,
    tokenName: null,
    tokenType: null,
    tokenTimestamp: null,
    triggerUrl: null,
    isActive: null,

    events: [],
    stats: null,

    loading: false,
    error: null,

    selectedEvent: null,
    dataLoaded: false,

    init() {
      log("tokenEvents", "init called");

      bindTokenEventsModalState(this);

      const modalEl = document.getElementById("token-events-modal");
      if (modalEl) {
        modalEl.addEventListener("click", (e) => {
          const hideBtn = e.target.closest('[data-modal-hide="token-events-modal"]');
          if (!hideBtn) return;

          log("tokenEvents", "modal hide clicked");

          this.$store?.tokenEventsModal?.clear?.();
          this.resetView();
        });
      }
    },

    applyTokenContext(tokenId, tokenType, tokenName, triggerUrl = null, isActive = null, tokenTimestamp = null) {
      const same =
        this.tokenId === tokenId &&
        this.tokenType === tokenType &&
        this.tokenName === tokenName &&
        this.tokenTimestamp === tokenTimestamp &&
        this.triggerUrl === triggerUrl;
        this.isActive === isActive;

      this.tokenId = tokenId;
      this.tokenType = tokenType || null;
      this.tokenName = tokenName || null;
      this.triggerUrl = triggerUrl || null;
      this.isActive = isActive;
      this.tokenTimestamp = tokenTimestamp || null;

      log("tokenEvents", "applyTokenContext", {
        same,
        tokenId: this.tokenId,
        tokenName: this.tokenName,
        tokenType: this.tokenType,
        tokenTimestamp: this.tokenTimestamp,
        triggerUrl: this.triggerUrl,
        isActive: this.isActive,
      });

      if (!same) this.loadData();
    },

    async loadData() {

      this.loading = true;
      this.error = null;
      this.dataLoaded = false;

      log("tokenEvents", "loadData started", {
        tokenId: this.tokenId,
        tokenType: this.tokenType,
        tokenName: this.tokenName,
        tokenTimestamp: this.tokenTimestamp,
        triggerUrl: this.triggerUrl,
      });

      try {
        const { events, stats } = await fetchTokenEventsData(this.tokenId);

        this.events = Array.isArray(events) ? events : [];
        this.stats = stats || null;
        this.selectedEvent = this.events[0] || null;
        this.dataLoaded = true;

        group("tokenEvents", "loadData success", () => {
          console.log("tokenId:", this.tokenId);
          console.log("tokenType:", this.tokenType);
          console.log("tokenName:", this.tokenName);
          console.log("tokenTimestamp:", this.tokenTimestamp);
          console.log("triggerUrl:", this.triggerUrl);
          console.log("events count:", this.events.length);
          console.log("selectedEvent:", this.selectedEvent);
          console.log("stats:", this.stats);
        });
      } catch (err) {
        logError("tokenEvents", "loadData failed", err);

        this.error = "Не удалось загрузить события";
        this.events = [];
        this.stats = null;
        this.selectedEvent = null;
      } finally {
        this.loading = false;
        log("tokenEvents", "loadData finished", {
          loading: this.loading,
          dataLoaded: this.dataLoaded,
        });
      }
    },

    resetView() {
      this.tokenId = null;
      this.tokenType = null;
      this.events = [];
      this.stats = null;
      this.selectedEvent = null;
      this.loading = false;
      this.error = null;
      this.dataLoaded = false;
      this.triggerUrl = null;
      this.isActive = null;

      log("tokenEvents", "resetView called");
    },

    selectEvent(ev) {
      this.selectedEvent = ev;
    },
    
    formatDate: formatEventDate,
    formatIP: formatEventIP,
    formatUserAgent: formatEventUserAgent,
    getEventIcon,
    getEventStatusColor,
    getFlagEmoji,

    openTriggerUrl() {
      openUrl(this.triggerUrl);
    },

    async copyTriggerUrl() {
      await copyText(this.triggerUrl);
    },

    async toggleTokenActive() {
      if (!this.tokenId) return;

      const nextValue = !this.isActive;

      try {
        const data = await tokensApi.patch(`/tokens/${this.tokenId}/status`, {
          is_active: nextValue,
        });

        this.isActive = data.is_active;

        if (this.$store?.tokenEventsModal) {
          this.$store.tokenEventsModal.isActive = data.is_active;
        }

        log("tokenEvents", "token status updated", {
          tokenId: this.tokenId,
          isActive: this.isActive,
        });
      } catch (err) {
        logError("tokenEvents", "toggleTokenActive failed", err);
      }
    },

  };
}