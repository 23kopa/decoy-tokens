export function getIpChangedEventIds(previousEvents = [], nextEvents = []) {
  const previousIpById = new Map(
    previousEvents.map((event) => [event.id, event.current_ip || null])
  );

  return nextEvents
    .filter((event) => {
      if (!previousIpById.has(event.id)) return false;

      const prevIp = previousIpById.get(event.id);
      const nextIp = event.current_ip || null;

      return prevIp !== nextIp;
    })
    .map((event) => event.id);
}