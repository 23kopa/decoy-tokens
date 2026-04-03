export function showSuccess(message, duration = 3000) {
  window.dispatchEvent(new CustomEvent('notification-show', {
    detail: { message, type: 'success', duration }
  }));
}

export function showError(message, duration = 5000) {
  window.dispatchEvent(new CustomEvent('notification-show', {
    detail: { message, type: 'error', duration }
  }));
}

export function showWarning(message, duration = 3000) {
  window.dispatchEvent(new CustomEvent('notification-show', {
    detail: { message, type: 'warning', duration }
  }));
}