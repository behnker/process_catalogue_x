/**
 * k6 Load Test: Authentication Endpoints
 *
 * Tests:
 *   - POST /auth/dev-login (dev environment only)
 *   - POST /auth/refresh
 *   - GET /auth/me
 *
 * Run:
 *   k6 run tests/load/auth.js
 *   k6 run tests/load/auth.js --env PROFILE=medium
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';
import { url, authHeaders, jsonHeaders, LOAD_PROFILES, AUTH_THRESHOLDS } from './config.js';

// Custom metrics
const loginSuccess = new Rate('login_success');
const loginDuration = new Trend('login_duration');
const meSuccess = new Rate('me_success');
const meDuration = new Trend('me_duration');

// Select profile from environment or default to smoke
const profile = __ENV.PROFILE || 'smoke';
export const options = {
    ...LOAD_PROFILES[profile],
    thresholds: AUTH_THRESHOLDS,
};

export function setup() {
    console.log(`Running auth load test with profile: ${profile}`);
    console.log(`Target: ${LOAD_PROFILES[profile].vus || 'staged'} VUs`);
}

export default function () {
    // Test 1: Dev Login
    const loginStart = Date.now();
    const loginRes = http.post(
        url('/auth/dev-login'),
        null,
        { headers: jsonHeaders() }
    );
    loginDuration.add(Date.now() - loginStart);

    const loginOk = check(loginRes, {
        'login status is 200': (r) => r.status === 200,
        'login has access_token': (r) => r.json('access_token') !== undefined,
        'login has refresh_token': (r) => r.json('refresh_token') !== undefined,
    });
    loginSuccess.add(loginOk);

    if (!loginOk) {
        console.error(`Login failed: ${loginRes.status} - ${loginRes.body}`);
        return;
    }

    const tokens = loginRes.json();
    const accessToken = tokens.access_token;
    const refreshToken = tokens.refresh_token;

    sleep(0.5);

    // Test 2: Get Current User
    const meStart = Date.now();
    const meRes = http.get(
        url('/auth/me'),
        { headers: authHeaders(accessToken) }
    );
    meDuration.add(Date.now() - meStart);

    const meOk = check(meRes, {
        'me status is 200': (r) => r.status === 200,
        'me has email': (r) => r.json('email') !== undefined,
        'me has organizations': (r) => r.json('organizations') !== undefined,
    });
    meSuccess.add(meOk);

    sleep(0.5);

    // Test 3: Refresh Token
    const refreshRes = http.post(
        url('/auth/refresh'),
        JSON.stringify({ refresh_token: refreshToken }),
        { headers: jsonHeaders() }
    );

    check(refreshRes, {
        'refresh status is 200': (r) => r.status === 200,
        'refresh has new access_token': (r) => r.json('access_token') !== undefined,
    });

    sleep(1);
}

export function teardown(data) {
    console.log('Auth load test completed');
}
