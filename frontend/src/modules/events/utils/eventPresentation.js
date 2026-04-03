export function formatEventDate(v) {
  if (!v) return "—";

  const d = new Date(v);
  if (Number.isNaN(d.getTime())) return String(v);

  const pad = (n) => String(n).padStart(2, '0');

  const day = pad(d.getDate());
  const month = pad(d.getMonth() + 1);
  const year = d.getFullYear();

  const hours = pad(d.getHours());
  const minutes = pad(d.getMinutes());

  return `${day}.${month}.${year} ${hours}:${minutes}`;
}

export function formatEventIP(v) {
  return v || "—";
}

export function getEventIcon(event) {
  if (event?.additional_data?.bot_info?.is_bot) return "🤖";
  if (event?.is_first) return "✨";
  return "👁️";
}

export function getEventStatusColor(event) {
  if (event?.additional_data?.bot_info?.is_bot) {
    return "border-yellow-700 text-yellow-300 bg-yellow-900/20";
  }
  if (event?.is_first) {
    return "border-emerald-700 text-emerald-300 bg-emerald-900/20";
  }
  return "border-gray-700 text-gray-300";
}

export function getTimeAgo(timestamp) {
  if (!timestamp) return '—';

  const now = new Date();
  const date = new Date(timestamp);
  const diff = Math.floor((now - date) / 1000);

  if (diff < 60) return `${diff} сек назад`;
  if (diff < 3600) return `${Math.floor(diff / 60)} мин назад`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} ч назад`;
  if (diff < 604800) return `${Math.floor(diff / 86400)} д назад`;

  return date.toLocaleDateString();
}

export function getEventWord(count) {
  if (count % 10 === 1 && count % 100 !== 11) return 'событие';
  if ([2, 3, 4].includes(count % 10) && ![12, 13, 14].includes(count % 100)) return 'события';
  return 'событий';
}