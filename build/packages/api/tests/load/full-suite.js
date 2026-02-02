/**
 * k6 Load Test: Full API Suite
 *
 * Comprehensive load test covering all major endpoints.
 * Simulates realistic user behavior with mixed operations.
 *
 * Run:
 *   k6 run tests/load/full-suite.js
 *   k6 run tests/load/full-suite.js --env PROFILE=heavy
 *   k6 run --out dashboard tests/load/full-suite.js
 */

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend } from 'k6/metrics';
import { url, authHeaders, jsonHeaders, LOAD_PROFILES, STANDARD_THRESHOLDS } from './config.js';

// Custom metrics per endpoint group
const authRate = new Rate('auth_success');
const processRate = new Rate('process_success');
const riadaRate = new Rate('riada_success');
const portfolioRate = new Rate('portfolio_success');
const surveyRate = new Rate('survey_success');

const authDuration = new Trend('auth_duration');
const processDuration = new Trend('process_duration');
const riadaDuration = new Trend('riada_duration');
const portfolioDuration = new Trend('portfolio_duration');
const surveyDuration = new Trend('survey_duration');

// Select profile
const profile = __ENV.PROFILE || 'smoke';
export const options = {
    ...LOAD_PROFILES[profile],
    thresholds: {
        ...STANDARD_THRESHOLDS,
        'auth_success': ['rate>0.99'],
        'process_success': ['rate>0.95'],
        'riada_success': ['rate>0.95'],
        'portfolio_success': ['rate>0.95'],
        'survey_success': ['rate>0.95'],
    },
};

export function setup() {
    console.log(`Running full suite load test with profile: ${profile}`);

    const loginRes = http.post(url('/auth/dev-login'), null, { headers: jsonHeaders() });
    if (loginRes.status !== 200) {
        throw new Error(`Setup failed: ${loginRes.status}`);
    }

    return { token: loginRes.json('access_token') };
}

export default function (data) {
    const headers = authHeaders(data.token);

    // Randomly select which endpoint group to test (simulates varied user behavior)
    const rand = Math.random();

    if (rand < 0.3) {
        // 30% - Process operations (most common)
        testProcesses(headers);
    } else if (rand < 0.5) {
        // 20% - RIADA operations
        testRiada(headers);
    } else if (rand < 0.65) {
        // 15% - Portfolio operations
        testPortfolio(headers);
    } else if (rand < 0.75) {
        // 10% - Survey operations
        testSurveys(headers);
    } else if (rand < 0.85) {
        // 10% - Operating Model
        testOperatingModel(headers);
    } else if (rand < 0.95) {
        // 10% - Prompt Library
        testPrompts(headers);
    } else {
        // 5% - Auth refresh
        testAuthRefresh(data.token);
    }

    sleep(0.5 + Math.random());  // Random delay 0.5-1.5s
}

function testProcesses(headers) {
    group('Processes', function () {
        const start = Date.now();

        // List
        let res = http.get(url('/processes/'), { headers });
        let ok = check(res, { 'list ok': (r) => r.status === 200 });

        // Tree
        res = http.get(url('/processes/tree'), { headers });
        ok = ok && check(res, { 'tree ok': (r) => r.status === 200 });

        // Search
        res = http.get(url('/processes/?search=source'), { headers });
        ok = ok && check(res, { 'search ok': (r) => r.status === 200 });

        processDuration.add(Date.now() - start);
        processRate.add(ok);
    });
}

function testRiada(headers) {
    group('RIADA', function () {
        const start = Date.now();

        // List
        let res = http.get(url('/riada/'), { headers });
        let ok = check(res, { 'list ok': (r) => r.status === 200 });

        // Summary
        res = http.get(url('/riada/summary'), { headers });
        ok = ok && check(res, { 'summary ok': (r) => r.status === 200 });

        // Filter by type
        res = http.get(url('/riada/?riada_type=risk'), { headers });
        ok = ok && check(res, { 'filter ok': (r) => r.status === 200 });

        riadaDuration.add(Date.now() - start);
        riadaRate.add(ok);
    });
}

function testPortfolio(headers) {
    group('Portfolio', function () {
        const start = Date.now();

        // List
        let res = http.get(url('/portfolio/'), { headers });
        let ok = check(res, { 'list ok': (r) => r.status === 200 });

        // Tree
        res = http.get(url('/portfolio/tree'), { headers });
        ok = ok && check(res, { 'tree ok': (r) => r.status === 200 });

        portfolioDuration.add(Date.now() - start);
        portfolioRate.add(ok);
    });
}

function testSurveys(headers) {
    group('Surveys', function () {
        const start = Date.now();

        // List
        let res = http.get(url('/surveys/'), { headers });
        let ok = check(res, { 'list ok': (r) => r.status === 200 });

        // Filter by mode
        res = http.get(url('/surveys/?mode=ai_fluency'), { headers });
        ok = ok && check(res, { 'filter ok': (r) => r.status === 200 });

        surveyDuration.add(Date.now() - start);
        surveyRate.add(ok);
    });
}

function testOperatingModel(headers) {
    group('Operating Model', function () {
        // First get a process
        const listRes = http.get(url('/processes/?page_size=1'), { headers });
        if (listRes.status !== 200) return;

        const items = listRes.json('items');
        if (!items || items.length === 0) return;

        const processId = items[0].id;

        // Get operating model
        const res = http.get(url(`/processes/${processId}/operating-model`), { headers });
        check(res, { 'om list ok': (r) => r.status === 200 });

        // Get summary
        const summaryRes = http.get(url(`/processes/${processId}/operating-model/summary`), { headers });
        check(summaryRes, { 'om summary ok': (r) => r.status === 200 });
    });
}

function testPrompts(headers) {
    group('Prompts', function () {
        // List templates
        let res = http.get(url('/prompts/templates'), { headers });
        check(res, { 'templates ok': (r) => r.status === 200 });

        // List LLM configs
        res = http.get(url('/prompts/llm-config'), { headers });
        check(res, { 'llm-config ok': (r) => r.status === 200 });
    });
}

function testAuthRefresh(token) {
    group('Auth', function () {
        const start = Date.now();

        // Get current user
        const res = http.get(url('/auth/me'), { headers: authHeaders(token) });
        const ok = check(res, { 'me ok': (r) => r.status === 200 });

        authDuration.add(Date.now() - start);
        authRate.add(ok);
    });
}

export function teardown(data) {
    console.log('Full suite load test completed');
}
