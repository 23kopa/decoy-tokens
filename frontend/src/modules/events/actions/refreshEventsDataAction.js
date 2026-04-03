import { loadEventsDataAction } from './loadEventsDataAction';

export async function refreshEventsDataAction(ctx) {
  const buttonId = 'refresh_' + (ctx.tokenId || 'unknown');

  ctx.buttonLoading.refresh = true;
  ctx.refreshing = true;
  ctx.buttonUtils.showLoading(buttonId, 600);

  const MIN_DURATION = 1500; // 1.5 секунды
  const start = Date.now();

  try {
    await loadEventsDataAction(ctx, {
      preserveData: true,
      silent: true,
    });
  } finally {
    const elapsed = Date.now() - start;
    const remaining = Math.max(0, MIN_DURATION - elapsed);

    setTimeout(() => {
      ctx.buttonUtils.hideLoading(buttonId);

      ctx.buttonLoading.refresh = false;
      ctx.refreshing = false;
    }, remaining);
  }
}