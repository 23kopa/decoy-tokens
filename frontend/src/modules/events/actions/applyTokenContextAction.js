export function applyTokenContextAction(
  ctx,
  tokenId,
  tokenType,
  tokenName,
  tokenDesc = null,
  tokenTimestamp = null,
  triggerUrl = null,
  isActive = null
) {
  const same =
    ctx.tokenId === tokenId &&
    ctx.tokenType === tokenType &&
    ctx.tokenName === tokenName &&
    ctx.tokenDesc === tokenDesc &&
    ctx.tokenTimestamp === tokenTimestamp &&
    ctx.triggerUrl === triggerUrl &&
    ctx.isActive === isActive;

  ctx.tokenId = tokenId;
  ctx.tokenType = tokenType || null;
  ctx.tokenName = tokenName || null;
  ctx.tokenDesc = tokenDesc || null;
  ctx.triggerUrl = triggerUrl || null;
  ctx.isActive = isActive;
  ctx.tokenTimestamp = tokenTimestamp || null;

  if (!same) {
    ctx.loadData();
  }
}