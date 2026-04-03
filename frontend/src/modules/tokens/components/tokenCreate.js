import { createToken, buildTokenPayload, createTokenResult } from '../services/createTokenService';
import { useProgressAnimation } from '../utils/tokenProgressAnimation';
import { copyText, openUrl } from '../../shared/utils/clipboard';

export function tokenCreate(tokenType, modalId, debug = false) {
  return {
    ...useProgressAnimation(),

    tokenType,
    modalId,
    debug,

    view: 'create',
    progress: 0,
    error: null,
    copied: false,

    resultData: null,

    formData: {
      name: "",
      email: "",
      desc: "",
      redirectUrl: "",
    },

    enableRedirect: false,

    init() {
      console.log(`TokenCreate initialized for ${this.tokenType}`);

      if (this.debug) {
        this.setView('result');
      }
    },

    setView(view) {
      this.view = view;

      if (view === 'create') {
        this.progress = 0;
        return;
      }

      if (view === 'progress') {
        this.resultData = null;
        if (this.debug) {
          this.progress = 10;
        }
        return;
      }

      if (view === 'result') {
        if (this.debug) {
          this.resultData = {
            tokenId: "12345678-abcd-efgh-ijkl-1234567890ab",
            email: "test@example.com",
            tokenType: this.tokenType,
            description: "Тестовое описание токена",
            redirectUrl: "https://example.com/test",
            triggerUrl: "https://example.com/very/long/url"
          };
        }
      }
    },

    buildPayload() {
      return buildTokenPayload({
        tokenType: this.tokenType,
        formData: this.formData,
        enableRedirect: this.enableRedirect,
      });
    },

    async submit() {
      this.setView('progress');
      this.progress = 0;
      this.error = null;

      this.startProgress((value) => {
        this.progress = value;
      });

      try {
        const payload = this.buildPayload();
        const data = await createToken(payload);

        await this.completeProgress((value) => {
          this.progress = value;
        });

        this.resultData = createTokenResult({
          formData: this.formData,
          data,
          tokenType: this.tokenType,
        });

        this.setView('result');
        this.resetForm();
      } catch (error) {
        this.stopProgress();

        if (error.response) {
          this.error = error.response.data.detail || "Ошибка при создании токена";
        } else if (error.request) {
          this.error = "Нет ответа от сервера";
        } else {
          this.error = error.message;
        }

        this.setView('create');
        console.error("Error creating token:", error);
      }
    },

    async copyResultTriggerUrl() {
      const ok = await copyText(this.resultData?.triggerUrl);

      if (!ok) {
        window.dispatchEvent(new CustomEvent('notification-show', {
          detail: {
            message: 'Не удалось скопировать ссылку',
            type: 'error',
            duration: 3000
          }
        }));
        return;
      }

      this.copied = true;

      window.dispatchEvent(new CustomEvent('notification-show', {
        detail: {
          message: 'URL скопирован',
          type: 'success',
          duration: 2000
        }
      }));

      setTimeout(() => {
        this.copied = false;
      }, 2000);
    },

    openResultTriggerUrl() {
      openUrl(this.resultData?.triggerUrl);
    },

    reset() {
      this.stopProgress();
      this.resetProgress((value) => {
        this.progress = value;
      });

      this.view = 'create';
      this.error = null;
      this.resultData = null;
      this.copied = false;
    },

    resetForm() {
      this.formData = {
        name: "",
        email: "",
        desc: "",
        redirectUrl: "",
      };
      this.enableRedirect = false;
    },

    resetAll() {
      this.reset();
      this.resetForm();
    },

    destroy() {
      this.stopProgress?.();
    },

  };
}