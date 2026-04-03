import { log } from '../../shared/utils/logger';

export function bindTokenEventsModalHandlers(ctx) {
  const modalEl = document.getElementById('token-events-modal');
  if (!modalEl) return;

  modalEl.addEventListener('click', (e) => {
    const hideBtn = e.target.closest('[data-modal-hide="token-events-modal"]');
    if (!hideBtn) return;

    log('tokenEvents', 'modal hide clicked');
    ctx.$store?.tokenEventsModal?.clear?.();
    ctx.resetView();
  });

  modalEl.addEventListener('hidden', () => {
    ctx.buttonUtils.resetAll();
    ctx.resetButtonStates();
  });
}