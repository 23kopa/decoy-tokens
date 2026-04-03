import { downloadEventJson } from '../services/eventDownloadService';
import { showSuccess, showError } from '../utils/eventNotifications';

export async function downloadEventJsonAction(ctx, event) {
  if (!event) return;

  const buttonId = 'download_' + (ctx.tokenId || 'unknown');

  ctx.buttonLoading.download = true;
  ctx.buttonUtils.showLoading(buttonId, 400);

  try {
    await downloadEventJson(event);
    showSuccess('Файл сохранён');
  } catch {
    showError('Ошибка при скачивании');
  } finally {
    ctx.buttonUtils.hideLoading(buttonId);

    setTimeout(() => {
      ctx.buttonLoading.download = false;
    }, 100);
  }
}