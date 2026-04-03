import { log, error as logError } from '../../shared/utils/logger';
import { updateTokenStatus } from '../services/tokenStatusService';
import { showError, showSuccess, showWarning } from '../../events/utils/eventNotifications';

export async function toggleTokenActiveAction(ctx) {
  if (!ctx.tokenId) return;

  const nextValue = !ctx.isActive;

  try {
    const data = await updateTokenStatus(ctx.tokenId, nextValue);

    ctx.isActive = data.is_active;

    if (ctx.$store?.tokenEventsModal) {
      ctx.$store.tokenEventsModal.isActive = data.is_active;
    }

    if (ctx.$store?.tokenCards) {
      const currentItems = ctx.$store.tokenCards.items || {};
      const currentCard = currentItems[ctx.tokenId] || {};

      ctx.$store.tokenCards.items = {
        ...currentItems,
        [ctx.tokenId]: {
          ...currentCard,
          isActive: data.is_active,
        }
      };
    }

    window.dispatchEvent(new CustomEvent('token-status-changed', {
      detail: {
        tokenId: ctx.tokenId,
        isActive: data.is_active
      }
    }));

    log('tokenEvents', 'token status updated', {
      tokenId: ctx.tokenId,
      isActive: data.is_active,
    });

  } catch (err) {
    logError('tokenEvents', 'toggleTokenActive failed', err);
    showError('Ошибка при изменении статуса');
  }
}