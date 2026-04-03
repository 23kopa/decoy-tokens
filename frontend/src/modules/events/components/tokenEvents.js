// modules/events/components/TokenEvents.js
import { log } from '../../shared/utils/logger';
import { copyText, openUrl } from '../../shared/utils/clipboard';
import { buttonFeedback } from '../../shared/utils/buttonFeedback.js';

import { bindTokenEventsModalState } from '../services/showEventsInfoService.js';
import { downloadEventJson } from '../services/eventDownloadService';
import { bindTokenEventsModalHandlers } from '../handlers/bindTokenEventsModalHandlers';

import { loadEventsDataAction } from '../actions/loadEventsDataAction';
import { refreshEventsDataAction } from '../actions/refreshEventsDataAction.js';
import { downloadEventJsonAction } from '../actions/downloadEventJsonAction';
import { applyTokenContextAction } from '../actions/applyTokenContextAction';

import { toggleTokenActiveAction } from '../../tokens/actions/toggleTokenActiveAction';

import { showSuccess } from '../utils/eventNotifications';

import {
  formatEventDate,
  formatEventIP,
  getEventIcon,
  getEventStatusColor,
  getTimeAgo,
} from '../utils/eventPresentation';

import { getInitialEventsState } from '../state/eventsState.js';
import {
  resetEventsButtonStates,
  resetEventsView,
} from '../state/eventsResetters.js';


export function tokenEvents() {
  return {

    ...getInitialEventsState(),
    
    buttonLoading: {
      refresh: false,
      download: false
    },

    buttonUtils: buttonFeedback(),

    init() {
      bindTokenEventsModalState(this);
      bindTokenEventsModalHandlers(this);
    },

    selectEvent(ev) {
      this.selectedEvent = ev;
    },

    isEventIpChanged(event) {
      return this.ipChangedEventIds.includes(event.id);
    },

    formatDate: formatEventDate,
    formatIP: formatEventIP,
    getEventIcon,
    getEventStatusColor,
    getTimeAgo,

    applyTokenContext(
      tokenId,
      tokenType,
      tokenName,
      tokenDesc = null,
      tokenTimestamp = null,
      triggerUrl = null,
      isActive = null
    ) {
      applyTokenContextAction(
        this,
        tokenId,
        tokenType,
        tokenName,
        tokenDesc,
        tokenTimestamp,
        triggerUrl,
        isActive
      );
    },

    async loadData() {
      await loadEventsDataAction(this);
    },

    async refreshData() {
      await refreshEventsDataAction(this);
    },

    async downloadEventJson(event) {
      await downloadEventJsonAction(this, event);
    },

    async copyTriggerUrl() {
      await copyText(this.triggerUrl);
      showSuccess('URL скопирован', 2000);
    },

    async toggleTokenActive() {
      await toggleTokenActiveAction(this);
    },

    openTriggerUrl() {
      openUrl(this.triggerUrl);
    },

    resetButtonStates() {
      resetEventsButtonStates(this);
    },

    resetView() {
      resetEventsView(this);
    },

  };
}