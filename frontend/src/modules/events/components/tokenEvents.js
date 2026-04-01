// frontend/src/modules/tokens/components/TokenEvents.js
import { log, error as logError, group } from '../../shared/utils/logger';
import { copyText, openUrl } from '../../shared/utils/clipboard';
import { tokensApi } from '../../shared/utils/api';
import { buttonFeedback } from '../../shared/utils/buttonFeedback.js';
import { fetchTokenEventsData, bindTokenEventsModalState } from '../services/eventTokenService';
import {
  formatEventDate,
  formatEventIP,
  formatEventUserAgent,
  getEventIcon,
  getEventStatusColor,
} from '../utils/eventPresentation';

export function tokenEvents() {
  return {
    tokenId: null,
    tokenType: null,
    tokenName: null,
    tokenDesc: null,    
    tokenTimestamp: null,
    triggerUrl: null,
    isActive: null,

    events: [],
    stats: null,

    loading: false,
    error: null,

    selectedEvent: null,
    dataLoaded: false,

    buttonLoading: {
      refresh: false,
      download: false
    },

    buttonUtils: buttonFeedback(),

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

        modalEl.addEventListener("hidden", () => {
          this.buttonUtils.resetAll();
          this.resetButtonStates();
        });
      }
    },

    applyTokenContext(tokenId, tokenType, tokenName, tokenDesc = null, tokenTimestamp = null, triggerUrl = null, isActive = null) {
      const same =
        this.tokenId === tokenId &&
        this.tokenType === tokenType &&
        this.tokenName === tokenName &&
        this.tokenDesc === tokenDesc &&
        this.tokenTimestamp === tokenTimestamp &&
        this.triggerUrl === triggerUrl;
        this.isActive === isActive;

      this.tokenId = tokenId;
      this.tokenType = tokenType || null;
      this.tokenName = tokenName || null;
      this.tokenDesc = tokenDesc || null;
      this.triggerUrl = triggerUrl || null;
      this.isActive = isActive;
      this.tokenTimestamp = tokenTimestamp || null;

      log("tokenEvents", "applyTokenContext", {
        same,
        tokenId: this.tokenId,
        tokenType: this.tokenType,
        tokenDesc: this.tokenDesc,
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
        tokenDesc: this.tokenDesc,
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
          console.log("tokenDesc:", this.tokenDesc);
          console.log("tokenTimestamp:", this.tokenTimestamp);
          console.log("triggerUrl:", this.triggerUrl);
          console.log("events count:", this.events.length);
          console.log("selectedEvent:", this.selectedEvent);
          console.log("stats:", this.stats);
        });

        const eventCount = this.events.length;
        if (eventCount > 0) {
          window.dispatchEvent(new CustomEvent('notification-show', {
            detail: {
              message: `Загружено ${eventCount} ${this.getEventWord(eventCount)}`,
              type: 'success',
              duration: 3000
            }
          }));
        }

      } catch (err) {
        logError("tokenEvents", "loadData failed", err);

        this.error = "Не удалось загрузить события";
        this.events = [];
        this.stats = null;
        this.selectedEvent = null;
        
        window.dispatchEvent(new CustomEvent('notification-show', {
          detail: {
            message: 'Ошибка загрузки событий',
            type: 'error',
            duration: 5000
          }
        }));

      } finally {
        this.loading = false;
        log("tokenEvents", "loadData finished", {
          loading: this.loading,
          dataLoaded: this.dataLoaded,
        });
      }
    },

    getEventWord(count) {
      if (count % 10 === 1 && count % 100 !== 11) return 'событие';
      if ([2, 3, 4].includes(count % 10) && ![12, 13, 14].includes(count % 100)) return 'события';
      return 'событий';
    },

    async loadDataWithFeedback() {
      const buttonId = 'refresh_' + (this.tokenId || 'unknown');
      
      this.buttonLoading.refresh = true;
      this.buttonUtils.showLoading(buttonId, 600);
      
      try {
        await this.loadData();
      } finally {
        this.buttonUtils.hideLoading(buttonId);
        setTimeout(() => {
          this.buttonLoading.refresh = false;
        }, 100);
      }
    },

    async downloadEventWithFeedback(event) {
      if (!event) return;
      
      const buttonId = 'download_' + (this.tokenId || 'unknown');
      
      this.buttonLoading.download = true;
      this.buttonUtils.showLoading(buttonId, 400);
      
      try {
        await this.downloadEvent(event);
        window.dispatchEvent(new CustomEvent('notification-show', {
          detail: {
            message: 'Файл сохранён',
            type: 'success',
            duration: 3000
          }
        }));
      } catch (err) {
        window.dispatchEvent(new CustomEvent('notification-show', {
          detail: {
            message: 'Ошибка при скачивании',
            type: 'error',
            duration: 5000
          }
        }));
      } finally {
        this.buttonUtils.hideLoading(buttonId);
        setTimeout(() => {
          this.buttonLoading.download = false;
        }, 100);
      }
    },

    async downloadEvent(event) {
      if (!event) return;
      
      try {
        const eventData = JSON.stringify(event, null, 2);
        const blob = new Blob([eventData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `event-${event.id || 'event'}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        log('tokenEvents', 'event downloaded', { eventId: event.id });
      } catch (err) {
        logError('tokenEvents', 'download failed', err);
        throw err;
      }
    },

    timeAgo(timestamp) {
      if (!timestamp) return '—'

      const now = new Date()
      const date = new Date(timestamp)
      const diff = Math.floor((now - date) / 1000)

      if (diff < 60) return `${diff} сек назад`
      if (diff < 3600) return `${Math.floor(diff / 60)} мин назад`
      if (diff < 86400) return `${Math.floor(diff / 3600)} ч назад`
      if (diff < 604800) return `${Math.floor(diff / 86400)} д назад`

      return date.toLocaleDateString()
    },

    resetButtonStates() {
      this.buttonLoading = {
        refresh: false,
        download: false
      };
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

    openTriggerUrl() {
      openUrl(this.triggerUrl);
    },

    async copyTriggerUrl() {
      await copyText(this.triggerUrl);
      window.dispatchEvent(new CustomEvent('notification-show', {
        detail: {
          message: 'URL скопирован',
          type: 'success',
          duration: 2000
        }
      }));
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

        if (this.$store?.tokenCards) {
          const currentItems = this.$store.tokenCards.items || {};
          const currentCard = currentItems[this.tokenId] || {};

          this.$store.tokenCards.items = {
            ...currentItems,
            [this.tokenId]: {
              ...currentCard,
              isActive: data.is_active,
            }
          };
        }

        window.dispatchEvent(new CustomEvent('token-status-changed', {
          detail: {
            tokenId: this.tokenId,
            isActive: data.is_active
          }
        }));

        log("tokenEvents", "token status updated", {
          tokenId: this.tokenId,
          isActive: data.is_active,
        });

        window.dispatchEvent(new CustomEvent('notification-show', {
          detail: {
            message: data.is_active ? 'Токен активирован' : 'Токен деактивирован',
            type: data.is_active ? 'success' : 'warning',
            duration: 3000
          }
        }));
      } catch (err) {
        logError("tokenEvents", "toggleTokenActive failed", err);
        window.dispatchEvent(new CustomEvent('notification-show', {
          detail: {
            message: 'Ошибка при изменении статуса',
            type: 'error',
            duration: 5000
          }
        }));
      }
    }

  };
}