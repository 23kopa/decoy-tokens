import { log } from '../utils/logger.js';

export function buttonFeedback() {
  return {
    // Состояние для каждой кнопки
    buttonStates: {},
    
    // Таймеры для сброса состояния
    timers: {},

    /**
     * Показать состояние загрузки на кнопке
     * @param {string} buttonId - уникальный идентификатор кнопки
     * @param {number} duration - минимальная длительность анимации (мс)
     */
    showLoading(buttonId, duration = 500) {
      // Очищаем предыдущий таймер для этой кнопки
      if (this.timers[buttonId]) {
        clearTimeout(this.timers[buttonId]);
      }

      // Устанавливаем состояние загрузки
      this.buttonStates[buttonId] = {
        isLoading: true,
        startTime: Date.now(),
        minDuration: duration
      };

      log('buttonFeedback', 'showLoading', { buttonId, duration });
    },

    /**
     * Скрыть состояние загрузки
     * @param {string} buttonId - уникальный идентификатор кнопки
     */
    hideLoading(buttonId) {
      const state = this.buttonStates[buttonId];
      if (!state) return;

      const elapsed = Date.now() - state.startTime;
      const remaining = Math.max(0, state.minDuration - elapsed);

      log('buttonFeedback', 'hideLoading', { buttonId, elapsed, remaining });

      // Если прошло достаточно времени - скрываем сразу
      if (remaining <= 0) {
        this._resetButton(buttonId);
        return;
      }

      // Иначе ждём оставшееся время
      this.timers[buttonId] = setTimeout(() => {
        this._resetButton(buttonId);
      }, remaining);
    },

    /**
     * Проверить, загружается ли кнопка
     */
    isLoading(buttonId) {
      return !!this.buttonStates[buttonId]?.isLoading;
    },

    /**
     * Сбросить состояние кнопки
     */
    _resetButton(buttonId) {
      delete this.buttonStates[buttonId];
      delete this.timers[buttonId];
      log('buttonFeedback', 'resetButton', { buttonId });
    },

    /**
     * Очистить все состояния (при закрытии модалки)
     */
    resetAll() {
      Object.keys(this.timers).forEach(key => clearTimeout(this.timers[key]));
      this.buttonStates = {};
      this.timers = {};
      log('buttonFeedback', 'resetAll');
    }
  };
}