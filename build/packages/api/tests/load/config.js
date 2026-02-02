/**
 * k6 Load Testing Configuration
 *
 * Usage:
 *   k6 run tests/load/auth.js
 *   k6 run tests/load/processes.js --env BASE_URL=http://localhost:8000
 *
 * With dashboard:
 *   k6 run --out dashboard tests/load/full-suite.js
 */

// Base configuration
export const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
export const API_PREFIX = '/api/v1';

// Test user for dev environment
export const TEST_USER = {
    email: 'admin@dev.local',
};

// Standard load profiles
export const LOAD_PROFILES = {
    // Smoke test - verify endpoints work
    smoke: {
        vus: 1,
        duration: '30s',
    },

    // Light load - normal usage
    light: {
        vus: 10,
        duration: '2m',
    },

    // Medium load - moderate traffic
    medium: {
        vus: 50,
        duration: '5m',
    },

    // Heavy load - target 100 concurrent users
    heavy: {
        vus: 100,
        duration: '10m',
    },

    // Stress test - find breaking point
    stress: {
        stages: [
            { duration: '2m', target: 50 },
            { duration: '5m', target: 100 },
            { duration: '2m', target: 150 },
            { duration: '5m', target: 200 },
            { duration: '2m', target: 0 },
        ],
    },

    // Soak test - sustained load
    soak: {
        vus: 50,
        duration: '30m',
    },
};

// Thresholds for pass/fail
export const STANDARD_THRESHOLDS = {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],  // 95% under 500ms, 99% under 1s
    http_req_failed: ['rate<0.01'],                   // Less than 1% failure rate
    http_reqs: ['rate>10'],                           // At least 10 requests per second
};

// Thresholds for auth endpoints (more strict)
export const AUTH_THRESHOLDS = {
    http_req_duration: ['p(95)<300', 'p(99)<500'],
    http_req_failed: ['rate<0.001'],
    http_reqs: ['rate>5'],
};

// Helper to build full URL
export function url(path) {
    return `${BASE_URL}${API_PREFIX}${path}`;
}

// Common headers
export function authHeaders(token) {
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
    };
}

export function jsonHeaders() {
    return {
        'Content-Type': 'application/json',
    };
}
