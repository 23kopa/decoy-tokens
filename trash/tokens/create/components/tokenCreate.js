import { createToken, buildTokenPayload, createTokenResult } from "../services/createTokenService.js";
import { useProgressAnimation } from "../utils/tokenProgressAnimation.js";

export function tokenCreate(tokenType) {
  return {
    ...useProgressAnimation(),

    tokenType,

    progress: 0,
    showProgress: false,
    showResult: false,

    resultData: null,

    formData: {
      name: "",
      email: "",
      description: "",
      redirectUrl: "",
    },

    enableRedirect: false,

    init() {
      console.log(`TokenCreate initialized for ${this.tokenType}`);
    },

    buildPayload() {
      return buildTokenPayload({
        tokenType: this.tokenType,
        formData: this.formData,
        enableRedirect: this.enableRedirect,
      });
    },

    async submit() {
      this.showProgress = true;
      this.showResult = false;
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

        this.showResult = true;
        this.showProgress = false;

        this.resetForm();
      } catch (error) {
        this.stopProgress();
        this.showProgress = false;

        if (error.response) {
          this.error = error.response.data.detail || "Ошибка при создании токена";
        } else if (error.request) {
          this.error = "Нет ответа от сервера";
        } else {
          this.error = error.message;
        }

        console.error("Error creating token:", error);
      }
    },

    reset() {
      this.stopProgress();
      this.resetProgress((value) => {
        this.progress = value;
      });

      this.showProgress = false;
      this.showResult = false;
      this.error = null;
      this.resultData = null;
      this.copied = false;
    },

    resetForm() {
      this.formData = {
        name: "",
        email: "",
        description: "",
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