import Alpine from 'alpinejs';

// Импорт компонентов
import { tokenCreate } from './components/tokenCreate';

// Экспорт утилит для внешнего использования
export * from './services/createTokenService';
export * from './utils/tokenProgressAnimation';

document.addEventListener('alpine:init', () => {
    Alpine.data('tokenCreate', (tokenType, debug = false) => tokenCreate(tokenType, debug));
    console.log('Token components registered!');
});