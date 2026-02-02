# Load Testing with k6

Performance and load testing scripts for the Process Catalogue API.

## Prerequisites

Install k6: https://k6.io/docs/get-started/installation/

```bash
# macOS
brew install k6

# Windows
choco install k6

# Linux
sudo apt-get install k6
```

## Quick Start

```bash
# Start the API server
cd build/packages/api
uvicorn src.main:app --reload

# Run smoke test (1 VU, 30s)
k6 run tests/load/auth.js

# Run with specific profile
k6 run tests/load/processes.js --env PROFILE=medium

# Run full suite with dashboard
k6 run --out dashboard tests/load/full-suite.js
```

## Available Tests

| Script | Description |
|--------|-------------|
| `auth.js` | Authentication endpoints (login, refresh, me) |
| `processes.js` | Process Catalogue CRUD and tree |
| `full-suite.js` | All endpoints with realistic traffic distribution |

## Load Profiles

| Profile | VUs | Duration | Use Case |
|---------|-----|----------|----------|
| `smoke` | 1 | 30s | Verify endpoints work |
| `light` | 10 | 2m | Normal usage |
| `medium` | 50 | 5m | Moderate traffic |
| `heavy` | 100 | 10m | Target baseline (100 concurrent) |
| `stress` | staged | 16m | Find breaking point |
| `soak` | 50 | 30m | Sustained load |

## Thresholds

Default pass/fail thresholds:

- **Response time**: p95 < 500ms, p99 < 1000ms
- **Error rate**: < 1%
- **Throughput**: > 10 req/s

Auth endpoints have stricter thresholds (p95 < 300ms).

## Example Commands

```bash
# Smoke test
k6 run tests/load/auth.js

# Medium load
k6 run tests/load/processes.js --env PROFILE=medium

# Heavy load with custom URL
k6 run tests/load/full-suite.js \
  --env PROFILE=heavy \
  --env BASE_URL=https://api.staging.example.com

# Stress test with output to InfluxDB
k6 run tests/load/full-suite.js \
  --env PROFILE=stress \
  --out influxdb=http://localhost:8086/k6

# Generate HTML report
k6 run tests/load/full-suite.js --out json=results.json
# Then use k6-reporter or k6-html-reporter
```

## Metrics

Custom metrics tracked:

- `login_success` / `login_duration` - Login endpoint
- `list_success` / `list_duration` - List operations
- `tree_success` / `tree_duration` - Tree operations
- `create_success` / `create_duration` - Create operations
- `auth_success` / `process_success` / `riada_success` etc. - Per-group success rates

## CI Integration

Add to GitHub Actions:

```yaml
- name: Run load tests
  uses: grafana/k6-action@v0.3.1
  with:
    filename: build/packages/api/tests/load/full-suite.js
    flags: --env PROFILE=light --env BASE_URL=${{ env.API_URL }}
```

## Interpreting Results

### Healthy Results
- p95 response time < 500ms
- Error rate < 1%
- Consistent throughput

### Warning Signs
- p95 > 500ms or increasing over time
- Error rate > 1%
- Throughput decreasing under load

### Action Items
- If auth is slow: Check JWT verification, database connections
- If list is slow: Add pagination, optimize queries, add indexes
- If creates are slow: Check database write performance, transaction handling
