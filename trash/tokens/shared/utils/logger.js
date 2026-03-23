const DEBUG = true;

function formatScope(scope) {
  return `[tokens:${scope}]`;
}

export function log(scope, message, payload = null) {
  if (!DEBUG) return;
  if (payload !== null) {
    console.log(formatScope(scope), message, payload);
  } else {
    console.log(formatScope(scope), message);
  }
}

export function warn(scope, message, payload = null) {
  if (!DEBUG) return;
  if (payload !== null) {
    console.warn(formatScope(scope), message, payload);
  } else {
    console.warn(formatScope(scope), message);
  }
}

export function error(scope, message, payload = null) {
  if (!DEBUG) return;
  if (payload !== null) {
    console.error(formatScope(scope), message, payload);
  } else {
    console.error(formatScope(scope), message);
  }
}

export function group(scope, message, fn) {
  if (!DEBUG) return fn?.();
  console.group(formatScope(scope), message);
  try {
    fn?.();
  } finally {
    console.groupEnd();
  }
}