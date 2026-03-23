export function formatEventDate(v) {
  if (!v) return "—";
  const d = new Date(v);
  if (Number.isNaN(d.getTime())) return String(v);
  return d.toLocaleString();
}

export function formatEventIP(v) {
  return v || "—";
}

export function formatEventUserAgent(ua) {
  return ua || "—";
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
  return "border-gray-700 text-gray-300 bg-gray-900/20";
}

export function getFlagEmoji(countryCode) {
  if (!countryCode) return "🌍";
  const codePoints = countryCode
    .toUpperCase()
    .split("")
    .map((char) => 127397 + char.charCodeAt());
  return String.fromCodePoint(...codePoints);
}