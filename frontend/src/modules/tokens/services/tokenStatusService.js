import { tokensApi } from '../../shared/utils/api';

export async function updateTokenStatus(tokenId, isActive) {
  return tokensApi.patch(`/tokens/${tokenId}/status`, {
    is_active: isActive,
  });
}