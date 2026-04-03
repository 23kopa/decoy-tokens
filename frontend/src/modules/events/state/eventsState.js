export function getInitialEventsState() {
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
    refreshing: false,
    error: null,

    selectedEvent: null,
    dataLoaded: false,

    previousEventsSnapshot: [],
    ipChangedEventIds: [],

    buttonLoading: {
      refresh: false,
      download: false,
    },
  };
}