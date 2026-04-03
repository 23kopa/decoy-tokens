import { log, error as logError } from '../../shared/utils/logger';

export async function downloadEventJson(event) {
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
}