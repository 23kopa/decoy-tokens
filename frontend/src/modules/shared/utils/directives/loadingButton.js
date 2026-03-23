import { log } from '../logger.js';

export function registerLoadingButtonDirective(Alpine) {
  Alpine.directive('loading-button', (el, { expression }, { evaluateLater, cleanup }) => {
    // Получаем функцию для чтения значения
    const getValue = evaluateLater(expression);
    
    // Функция обновления состояния кнопки
    const updateButtonState = (isLoading) => {
      if (isLoading) {
        el.setAttribute('disabled', 'disabled');
        el.classList.add('pointer-events-none', 'opacity-70', 'cursor-not-allowed');
        
        // Добавляем спиннер если его нет
        if (!el.querySelector('.loading-spinner')) {
          const originalContent = el.innerHTML;
          el.setAttribute('data-original-content', originalContent);
          
          const spinner = document.createElement('span');
          spinner.className = 'inline-block mr-2 loading-spinner animate-spin';
          spinner.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>`;
          
          el.prepend(spinner);
        }
      } else {
        el.removeAttribute('disabled');
        el.classList.remove('pointer-events-none', 'opacity-70', 'cursor-not-allowed');
        
        // Удаляем спиннер
        const spinner = el.querySelector('.loading-spinner');
        if (spinner) {
          spinner.remove();
        }
        
        // Восстанавливаем оригинальное содержимое
        const originalContent = el.getAttribute('data-original-content');
        if (originalContent) {
          el.innerHTML = originalContent;
          el.removeAttribute('data-original-content');
        }
      }
    };

    // Подписываемся на изменения
    const unwatch = Alpine.effect(() => {
      getValue(value => {
        updateButtonState(value);
      });
    });

    // Очистка
    cleanup(() => {
      unwatch();
    });
  });
}