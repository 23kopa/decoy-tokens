import { log } from './logger.js';

export function notification() {
  return {
    // Состояние уведомлений
    notifications: [],
    
    // Максимальное количество уведомлений
    maxNotifications: 5,
    
    // Таймеры для автоматического скрытия
    timers: {},

    /**
     * Показать уведомление
     * @param {string} message - текст уведомления
     * @param {string} type - тип: 'success', 'error', 'info', 'warning'
     * @param {number} duration - длительность показа (мс)
     */
    show(message, type = 'info', duration = 3000) {
      const id = Date.now() + Math.random().toString(36).substr(2, 9);
      
      const notification = {
        id,
        message,
        type,
        duration,
        visible: true,
        createdAt: Date.now()
      };

      // Добавляем уведомление
      this.notifications.push(notification);
      
      // Ограничиваем количество
      if (this.notifications.length > this.maxNotifications) {
        this.notifications.shift();
      }

      log('notification', 'show', { message, type, id });

      // Автоматически скрываем через duration
      if (duration > 0) {
        this.timers[id] = setTimeout(() => {
          this.hide(id);
        }, duration);
      }

      return id;
    },

    /**
     * Скрыть уведомление
     */
    hide(id) {
      const index = this.notifications.findIndex(n => n.id === id);
      if (index !== -1) {
        // Очищаем таймер
        if (this.timers[id]) {
          clearTimeout(this.timers[id]);
          delete this.timers[id];
        }
        
        // Помечаем как скрытое
        this.notifications[index].visible = false;
        
        // Удаляем через небольшую задержку (для анимации)
        setTimeout(() => {
          this.notifications = this.notifications.filter(n => n.id !== id);
        }, 300);
      }
    },

    /**
     * Очистить все уведомления
     */
    clearAll() {
      Object.values(this.timers).forEach(timer => clearTimeout(timer));
      this.timers = {};
      this.notifications = [];
    },

    /**
     * Вспомогательные методы для разных типов
     */
    success(message, duration = 3000) {
      return this.show(message, 'success', duration);
    },

    error(message, duration = 5000) {
      return this.show(message, 'error', duration);
    },

    info(message, duration = 3000) {
      return this.show(message, 'info', duration);
    },

    warning(message, duration = 4000) {
      return this.show(message, 'warning', duration);
    },

    /**
     * Получить классы для типа уведомления
     */
    getTypeClasses(type) {
      const classes = {
        success: 'border-emerald-500/50 bg-emerald-950/30 text-emerald-200',
        error: 'border-red-500/50 bg-red-950/30 text-red-200',
        info: 'border-blue-500/50 bg-blue-950/30 text-blue-200',
        warning: 'border-yellow-500/50 bg-yellow-950/30 text-yellow-200'
      };
      return classes[type] || classes.info;
    },

    /**
     * Получить иконку для типа
     */
    getTypeIcon(type) {
      const icons = {
        success: '✓',
        error: '✗',
        info: 'ℹ',
        warning: '⚠'
      };
      return icons[type] || icons.info;
    }
  };
}