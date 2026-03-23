// frontend/src/modules/tokens/services/createTokenService.js
import { tokensApi } from '../../shared/utils/api';

export async function createToken(payload) {
  return tokensApi.post("/tokens", payload);
}

export function buildTokenPayload({ tokenType, formData, enableRedirect }) {
  const requestData = {
    name: formData.name.trim(),
    type: tokenType,
    desc: formData.desc || null,
    notify_email: formData.email,
    payload: {},
  };

  if (tokenType === "link" && enableRedirect && formData.redirectUrl) {
    requestData.payload.redirect_url = formData.redirectUrl;
  }

  return requestData;
}

export function createTokenResult({ formData, data, tokenType }) {
  return {
    name: formData.name,
    email: formData.email,
    description: formData.desc,
    redirectUrl: formData.redirectUrl,
    tokenId: data.id,
    triggerUrl: data.trigger_url,
    tokenType,
  };
}