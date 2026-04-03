export function resetEventsView(ctx) {
  ctx.tokenId = null;
  ctx.tokenType = null;
  ctx.tokenName = null;
  ctx.tokenDesc = null;
  ctx.tokenTimestamp = null;
  ctx.triggerUrl = null;
  ctx.isActive = null;

  ctx.events = [];
  ctx.stats = null;

  ctx.loading = false;
  ctx.refreshing = false;
  ctx.error = null;

  ctx.selectedEvent = null;
  ctx.dataLoaded = false;
  
  ctx.previousEventsSnapshot = [];
  ctx.ipChangedEventIds = [];
}

export function resetEventsButtonStates(ctx) {
  ctx.buttonLoading = {
    refresh: false,
    download: false,
  };
}