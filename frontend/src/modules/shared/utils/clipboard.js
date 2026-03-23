export const copyToClipboard = {
    timeouts: new Map(),

    async copy(text) {
        await navigator.clipboard.writeText(text);
        return true;
    },

    setCopiedState(key, callback, duration = 2000) {
        if (this.timeouts.has(key)) {
            clearTimeout(this.timeouts.get(key));
        }

        callback(true);
        this.timeouts.set(key, setTimeout(() => {
            callback(false);
            this.timeouts.delete(key);
        }, duration));
    },

    destroy() {
        this.timeouts.forEach(clearTimeout);
        this.timeouts.clear();
    }
};

export async function copyText(text) {
  if (!text) return false;

  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error("Clipboard copy failed:", err);
    return false;
  }
}

export function openUrl(url) {
  if (!url) return;
  window.open(url, "_blank", "noopener,noreferrer");
}