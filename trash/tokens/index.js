// frontend/src/tokens/index.js
import Alpine from 'alpinejs';

// Импорт компонентов
import { tokenCreate } from './create/components/tokenCreate.js';
import { tokenEvents } from './events/components/tokenEvents.js';

import { registerTokenEventsModalStore } from "./events/stores/tokenEventsModalStore.js";
import { initEventsBridge } from "./events/stores/tokenEventsStoreBridge.js";

// Экспорт утилит
export * from './shared/utils/api.js';
export * from './shared/utils/clipboard.js';

// Регистрация компонентов
document.addEventListener('alpine:init', () => {
    registerTokenEventsModalStore(Alpine);

    Alpine.data("tokenCreate", (tokenType) => tokenCreate(tokenType));
    Alpine.data("tokenEvents", () => tokenEvents());
    
    console.log('Token components registered!');
});

initEventsBridge();