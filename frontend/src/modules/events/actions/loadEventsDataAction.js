import { log, error as logError, group } from '../../shared/utils/logger';
import { fetchTokenEventsData } from '../services/showEventsInfoService';
import { getEventWord } from '../utils/eventPresentation';
import { showError, showSuccess } from '../utils/eventNotifications';
import { getIpChangedEventIds } from '../utils/eventDiff';

export async function loadEventsDataAction(ctx, options = {}) {
  const {
    silent = false,
    preserveData = false,
  } = options;

  const isInitialLoad = !preserveData;

  if (isInitialLoad) {
    ctx.loading = true;
    ctx.dataLoaded = false;
    ctx.ipChangedEventIds = [];
  }

  ctx.error = null;

  const previousEvents = Array.isArray(ctx.events) ? [...ctx.events] : [];

  log('tokenEvents', 'loadData started', {
    tokenId: ctx.tokenId,
    tokenType: ctx.tokenType,
    tokenName: ctx.tokenName,
    tokenDesc: ctx.tokenDesc,
    tokenTimestamp: ctx.tokenTimestamp,
    triggerUrl: ctx.triggerUrl,
    preserveData,
    silent,
  });

  try {
    const { events, stats } = await fetchTokenEventsData(ctx.tokenId);
    const nextEvents = Array.isArray(events) ? events : [];

    if (preserveData) {
      ctx.ipChangedEventIds = getIpChangedEventIds(previousEvents, nextEvents);
    } else {
      ctx.ipChangedEventIds = [];
    }

    ctx.previousEventsSnapshot = previousEvents;
    ctx.events = nextEvents;
    ctx.stats = stats || null;
    ctx.selectedEvent = ctx.events[0] || null;
    ctx.dataLoaded = true;

    group('tokenEvents', 'loadData success', () => {
      console.log('tokenId:', ctx.tokenId);
      console.log('events count:', ctx.events.length);
      console.log('selectedEvent:', ctx.selectedEvent);
      console.log('stats:', ctx.stats);
      console.log('ipChangedEventIds:', ctx.ipChangedEventIds);
    });

    const eventCount = ctx.events.length;
    if (!silent && eventCount > 0) {
      showSuccess(`Загружено ${eventCount} ${getEventWord(eventCount)}`);
    }
  } catch (err) {
    logError('tokenEvents', 'loadData failed', err);

    ctx.error = 'Не удалось загрузить события';

    if (isInitialLoad) {
      ctx.events = [];
      ctx.stats = null;
      ctx.selectedEvent = null;
      ctx.dataLoaded = false;
      ctx.ipChangedEventIds = [];
      ctx.previousEventsSnapshot = [];
    }

    if (!silent) {
      showError('Ошибка загрузки событий');
    }
  } finally {
    if (isInitialLoad) {
      ctx.loading = false;
    }

    log('tokenEvents', 'loadData finished', {
      loading: ctx.loading,
      dataLoaded: ctx.dataLoaded,
      preserveData,
      silent,
      ipChangedEventIds: ctx.ipChangedEventIds,
    });
  }
}