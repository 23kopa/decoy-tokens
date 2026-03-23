import Alpine from 'alpinejs';

import { tokenEvents } from './components/tokenEvents';
import { notification } from '../shared/utils/notification';
import { registerTokenEventsModalStore, registerTokenCardsStore } from './stores/tokenEventsModalStore';
import { initEventsBridge } from './stores/tokenEventsStoreBridge';

export * from './services/eventTokenService';
export * from './utils/eventPresentation';

document.addEventListener('alpine:init', () => {
    registerTokenEventsModalStore(Alpine);
    registerTokenCardsStore;
    Alpine.data('tokenEvents', () => tokenEvents());
    Alpine.data('notification', () => notification()); 
    console.log('Event components registered!');
});

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initEventsBridge());
} else {
    initEventsBridge();
}