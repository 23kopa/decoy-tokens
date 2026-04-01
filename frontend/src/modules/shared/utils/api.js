function getCookie(name) {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
}

export class ApiClient {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;

        const method = (options.method || 'GET').toUpperCase();

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (!['GET', 'HEAD', 'OPTIONS'].includes(method)) {
            const csrf = getCookie('csrf_token');
            if (csrf) {
                headers['X-CSRF-Token'] = csrf;
            }
        }

        const response = await fetch(url, {
            ...options,
            headers,
            credentials: 'include'
        });

        if (!response.ok) {
            const text = await response.text();
            throw new ApiError(response.status, text || response.statusText);
        }

        return response.json();
    }

    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    patch(endpoint, data) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    }

    get(endpoint) {
        return this.request(endpoint, {
            method: 'GET'
        });
    }
}

export class ApiError extends Error {
    constructor(status, message) {
        super(message);
        this.name = 'ApiError';
        this.status = status;
    }
}

export const tokensApi = new ApiClient('/api/v1');