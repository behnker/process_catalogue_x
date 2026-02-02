/**
 * k6 Load Test: Process Catalogue Endpoints
 *
 * Tests:
 *   - GET /processes (list)
 *   - GET /processes/tree
 *   - POST /processes (create)
 *   - GET /processes/{id}
 *   - PATCH /processes/{id}
 *
 * Run:
 *   k6 run tests/load/processes.js
 *   k6 run tests/load/processes.js --env PROFILE=heavy
 */

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';
import { url, authHeaders, jsonHeaders, LOAD_PROFILES, STANDARD_THRESHOLDS } from './config.js';

// Custom metrics
const listSuccess = new Rate('list_success');
const listDuration = new Trend('list_duration');
const treeSuccess = new Rate('tree_success');
const treeDuration = new Trend('tree_duration');
const createSuccess = new Rate('create_success');
const createDuration = new Trend('create_duration');
const processesCreated = new Counter('processes_created');

// Select profile
const profile = __ENV.PROFILE || 'smoke';
export const options = {
    ...LOAD_PROFILES[profile],
    thresholds: STANDARD_THRESHOLDS,
};

// Get auth token in setup
export function setup() {
    console.log(`Running processes load test with profile: ${profile}`);

    const loginRes = http.post(url('/auth/dev-login'), null, { headers: jsonHeaders() });
    if (loginRes.status !== 200) {
        throw new Error(`Setup failed: could not login - ${loginRes.status}`);
    }

    return {
        token: loginRes.json('access_token'),
    };
}

export default function (data) {
    const headers = authHeaders(data.token);

    // Test 1: List Processes
    group('List Processes', function () {
        const start = Date.now();
        const res = http.get(url('/processes/'), { headers });
        listDuration.add(Date.now() - start);

        const ok = check(res, {
            'list status is 200': (r) => r.status === 200,
            'list has items array': (r) => Array.isArray(r.json('items')),
            'list has total': (r) => r.json('total') !== undefined,
        });
        listSuccess.add(ok);
    });

    sleep(0.3);

    // Test 2: Get Process Tree
    group('Process Tree', function () {
        const start = Date.now();
        const res = http.get(url('/processes/tree'), { headers });
        treeDuration.add(Date.now() - start);

        const ok = check(res, {
            'tree status is 200': (r) => r.status === 200,
            'tree is array': (r) => Array.isArray(r.json()),
        });
        treeSuccess.add(ok);
    });

    sleep(0.3);

    // Test 3: Create Process (10% of iterations to avoid DB bloat)
    if (Math.random() < 0.1) {
        group('Create Process', function () {
            const uniqueCode = `L0-K6-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
            const payload = JSON.stringify({
                code: uniqueCode,
                name: `Load Test Process ${uniqueCode}`,
                level: 'L0',
                process_type: 'primary',
                description: 'Created by k6 load test',
            });

            const start = Date.now();
            const res = http.post(url('/processes/'), payload, { headers });
            createDuration.add(Date.now() - start);

            const ok = check(res, {
                'create status is 201': (r) => r.status === 201,
                'create has id': (r) => r.json('id') !== undefined,
            });
            createSuccess.add(ok);

            if (ok) {
                processesCreated.add(1);

                // Get the created process
                const processId = res.json('id');
                const getRes = http.get(url(`/processes/${processId}`), { headers });
                check(getRes, {
                    'get created process status is 200': (r) => r.status === 200,
                });

                // Update it
                const updateRes = http.patch(
                    url(`/processes/${processId}`),
                    JSON.stringify({ description: 'Updated by k6' }),
                    { headers }
                );
                check(updateRes, {
                    'update status is 200': (r) => r.status === 200,
                });
            }
        });
    }

    // Test 4: Filter by level
    group('Filter by Level', function () {
        const res = http.get(url('/processes/?level=L0'), { headers });
        check(res, {
            'filter status is 200': (r) => r.status === 200,
            'filter returns L0 only': (r) => {
                const items = r.json('items');
                return items.every(i => i.level === 'L0');
            },
        });
    });

    sleep(0.5);
}

export function teardown(data) {
    console.log('Processes load test completed');
    // Note: Created test data should be cleaned up separately
}
