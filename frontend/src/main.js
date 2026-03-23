// frontend/src/main.js
import "./styles/main.css";
import 'flowbite';
import Alpine from 'alpinejs';

import './modules/index.js';

window.Alpine = Alpine;
Alpine.start();

document.addEventListener('DOMContentLoaded', () => {
    console.log('Alpine.js initialized');
});

export { Alpine };