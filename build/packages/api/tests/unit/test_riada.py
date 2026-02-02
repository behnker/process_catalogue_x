"""
Unit tests for RIADA (Quality Logs) CRUD endpoints.
Uses the shared 'headers' fixture from conftest.py.
"""

import pytest
from httpx import AsyncClient


class TestRiadaList:
    """Test RIADA listing and filtering."""

    @pytest.mark.asyncio
    async def test_list_riada_unauthorized(self, client: AsyncClient):
        """List RIADA without auth returns 401."""
        response = await client.get("/api/v1/riada/")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_list_riada_empty(self, client: AsyncClient, headers):
        """List RIADA returns empty list initially."""
        response = await client.get("/api/v1/riada/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data


class TestRiadaCRUD:
    """Test full CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_risk(self, client: AsyncClient, headers):
        """Create a new risk item."""
        payload = {
            "title": "Supply chain disruption",
            "description": "Risk of supplier delays",
            "riada_type": "risk",
            "category": "process",
            "severity": "high",
            "probability": 3,
            "impact": 4,
        }
        response = await client.post(
            "/api/v1/riada/",
            json=payload,
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Supply chain disruption"
        assert data["riada_type"] == "risk"
        assert data["code"].startswith("RSK-")
        assert data["risk_score"] == 12  # 3 * 4
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_issue(self, client: AsyncClient, headers):
        """Create an issue with ISS code prefix."""
        response = await client.post(
            "/api/v1/riada/",
            json={
                "title": "System outage",
                "riada_type": "issue",
                "category": "system",
                "severity": "critical",
            },
            headers=headers,
        )
        assert response.status_code == 201
        assert response.json()["code"].startswith("ISS-")

    @pytest.mark.asyncio
    async def test_create_action(self, client: AsyncClient, headers):
        """Create an action with ACT code prefix."""
        response = await client.post(
            "/api/v1/riada/",
            json={
                "title": "Implement backup process",
                "riada_type": "action",
                "category": "process",
            },
            headers=headers,
        )
        assert response.status_code == 201
        assert response.json()["code"].startswith("ACT-")

    @pytest.mark.asyncio
    async def test_create_dependency(self, client: AsyncClient, headers):
        """Create a dependency with DEP code prefix."""
        response = await client.post(
            "/api/v1/riada/",
            json={
                "title": "ERP system integration",
                "riada_type": "dependency",
                "category": "system",
            },
            headers=headers,
        )
        assert response.status_code == 201
        assert response.json()["code"].startswith("DEP-")

    @pytest.mark.asyncio
    async def test_create_assumption(self, client: AsyncClient, headers):
        """Create an assumption with ASM code prefix."""
        response = await client.post(
            "/api/v1/riada/",
            json={
                "title": "Budget available Q2",
                "riada_type": "assumption",
                "category": "data",
            },
            headers=headers,
        )
        assert response.status_code == 201
        assert response.json()["code"].startswith("ASM-")

    @pytest.mark.asyncio
    async def test_get_riada_item(self, client: AsyncClient, headers):
        """Create and retrieve a RIADA item."""
        # Create
        create_response = await client.post(
            "/api/v1/riada/",
            json={
                "title": "Test item",
                "riada_type": "risk",
                "category": "people",
            },
            headers=headers,
        )
        item_id = create_response.json()["id"]

        # Get
        response = await client.get(
            f"/api/v1/riada/{item_id}",
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["id"] == item_id

    @pytest.mark.asyncio
    async def test_get_riada_not_found(self, client: AsyncClient, headers):
        """Get non-existent RIADA returns 404."""
        response = await client.get(
            "/api/v1/riada/00000000-0000-0000-0000-000000000000",
            headers=headers,
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_riada(self, client: AsyncClient, headers):
        """Update a RIADA item."""
        # Create
        create_response = await client.post(
            "/api/v1/riada/",
            json={
                "title": "Original title",
                "riada_type": "risk",
                "category": "process",
                "probability": 2,
                "impact": 2,
            },
            headers=headers,
        )
        item_id = create_response.json()["id"]

        # Update
        response = await client.patch(
            f"/api/v1/riada/{item_id}",
            json={
                "title": "Updated title",
                "probability": 5,
                "impact": 5,
                "status": "mitigated",
            },
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["status"] == "mitigated"
        assert data["risk_score"] == 25  # 5 * 5

    @pytest.mark.asyncio
    async def test_delete_riada(self, client: AsyncClient, headers):
        """Delete a RIADA item."""
        # Create
        create_response = await client.post(
            "/api/v1/riada/",
            json={
                "title": "To be deleted",
                "riada_type": "action",
                "category": "people",
            },
            headers=headers,
        )
        item_id = create_response.json()["id"]

        # Delete
        response = await client.delete(
            f"/api/v1/riada/{item_id}",
            headers=headers,
        )
        assert response.status_code == 204

        # Verify gone
        get_response = await client.get(
            f"/api/v1/riada/{item_id}",
            headers=headers,
        )
        assert get_response.status_code == 404


class TestRiadaFiltering:
    """Test filtering by type, category, severity."""

    @pytest.mark.asyncio
    async def test_filter_by_type(self, client: AsyncClient, headers):
        """Filter RIADA by type."""
        # Create items of different types
        await client.post(
            "/api/v1/riada/",
            json={"title": "Risk 1", "riada_type": "risk", "category": "process"},
            headers=headers,
        )
        await client.post(
            "/api/v1/riada/",
            json={"title": "Issue 1", "riada_type": "issue", "category": "process"},
            headers=headers,
        )

        # Filter by risk
        response = await client.get(
            "/api/v1/riada/?riada_type=risk",
            headers=headers,
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["riada_type"] == "risk"

    @pytest.mark.asyncio
    async def test_filter_by_severity(self, client: AsyncClient, headers):
        """Filter RIADA by severity."""
        await client.post(
            "/api/v1/riada/",
            json={
                "title": "Critical issue",
                "riada_type": "issue",
                "category": "system",
                "severity": "critical",
            },
            headers=headers,
        )

        response = await client.get(
            "/api/v1/riada/?severity=critical",
            headers=headers,
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["severity"] == "critical"

    @pytest.mark.asyncio
    async def test_filter_by_category(self, client: AsyncClient, headers):
        """Filter RIADA by category."""
        await client.post(
            "/api/v1/riada/",
            json={
                "title": "Data quality issue",
                "riada_type": "issue",
                "category": "data",
            },
            headers=headers,
        )

        response = await client.get(
            "/api/v1/riada/?category=data",
            headers=headers,
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["category"] == "data"


class TestRiadaSummary:
    """Test RIADA summary/aggregation endpoint."""

    @pytest.mark.asyncio
    async def test_get_summary(self, client: AsyncClient, headers):
        """Get RIADA summary with aggregations."""
        # Create some items
        await client.post(
            "/api/v1/riada/",
            json={"title": "R1", "riada_type": "risk", "category": "process"},
            headers=headers,
        )
        await client.post(
            "/api/v1/riada/",
            json={"title": "R2", "riada_type": "risk", "category": "people"},
            headers=headers,
        )
        await client.post(
            "/api/v1/riada/",
            json={"title": "I1", "riada_type": "issue", "category": "system"},
            headers=headers,
        )

        response = await client.get(
            "/api/v1/riada/summary",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "by_type" in data
        assert "by_severity" in data
        assert "by_status" in data
        assert "by_category" in data
