"""
Unit tests for Business Model Canvas CRUD endpoints.
Uses the shared 'headers' fixture from conftest.py.
"""

import pytest
from httpx import AsyncClient


class TestBusinessModelCanvas:
    """Test Business Model Canvas endpoints."""

    @pytest.mark.asyncio
    async def test_get_canvas_unauthorized(self, client: AsyncClient):
        """Get canvas without auth returns 401."""
        response = await client.get("/api/v1/business-model/canvas")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_canvas_creates_default(self, client: AsyncClient, headers):
        """Get canvas creates default if none exists."""
        response = await client.get(
            "/api/v1/business-model/canvas",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "entries_by_component" in data

        # Verify all 9 BMC components
        components = data["entries_by_component"]
        expected = [
            "key_partners",
            "key_activities",
            "key_resources",
            "value_propositions",
            "customer_relationships",
            "channels",
            "customer_segments",
            "cost_structure",
            "revenue_streams",
        ]
        for component in expected:
            assert component in components

    @pytest.mark.asyncio
    async def test_get_canvas_returns_same(self, client: AsyncClient, headers):
        """Subsequent calls return the same canvas."""
        response1 = await client.get(
            "/api/v1/business-model/canvas",
            headers=headers,
        )
        response2 = await client.get(
            "/api/v1/business-model/canvas",
            headers=headers,
        )
        assert response1.json()["id"] == response2.json()["id"]


class TestBusinessModelEntries:
    """Test BMC entry CRUD."""

    @pytest.mark.asyncio
    async def test_create_entry(self, client: AsyncClient, headers):
        """Create a new BMC entry."""
        # Ensure canvas exists
        await client.get("/api/v1/business-model/canvas", headers=headers)

        payload = {
            "component": "value_propositions",
            "title": "Global Sourcing Network",
            "description": "Access to 500+ verified suppliers worldwide",
            "priority": 1,
        }
        response = await client.post(
            "/api/v1/business-model/entries",
            json=payload,
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["component"] == "value_propositions"
        assert data["title"] == "Global Sourcing Network"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_entry_all_components(self, client: AsyncClient, headers):
        """Create entries for all 9 BMC components."""
        await client.get("/api/v1/business-model/canvas", headers=headers)

        components_data = [
            ("key_partners", "Supplier Network"),
            ("key_activities", "Sourcing Operations"),
            ("key_resources", "Technology Platform"),
            ("value_propositions", "Cost Reduction"),
            ("customer_relationships", "Dedicated Account Managers"),
            ("channels", "Direct Sales"),
            ("customer_segments", "DIY Retailers"),
            ("cost_structure", "Operations Team"),
            ("revenue_streams", "Commission Fees"),
        ]

        for component, title in components_data:
            response = await client.post(
                "/api/v1/business-model/entries",
                json={"component": component, "title": title},
                headers=headers,
            )
            assert response.status_code == 201, f"Failed for {component}"
            assert response.json()["component"] == component

    @pytest.mark.asyncio
    async def test_entry_appears_in_canvas(self, client: AsyncClient, headers):
        """Created entry appears in canvas response."""
        await client.get("/api/v1/business-model/canvas", headers=headers)

        # Create entry
        await client.post(
            "/api/v1/business-model/entries",
            json={
                "component": "customer_segments",
                "title": "Bunnings Retail",
            },
            headers=headers,
        )

        # Get canvas
        canvas_response = await client.get(
            "/api/v1/business-model/canvas",
            headers=headers,
        )
        customer_segments = canvas_response.json()["entries_by_component"]["customer_segments"]
        assert any(e["title"] == "Bunnings Retail" for e in customer_segments)

    @pytest.mark.asyncio
    async def test_delete_entry(self, client: AsyncClient, headers):
        """Delete a BMC entry."""
        await client.get("/api/v1/business-model/canvas", headers=headers)

        # Create entry
        create_response = await client.post(
            "/api/v1/business-model/entries",
            json={
                "component": "key_activities",
                "title": "To Delete",
            },
            headers=headers,
        )
        entry_id = create_response.json()["id"]

        # Delete it
        delete_response = await client.delete(
            f"/api/v1/business-model/entries/{entry_id}",
            headers=headers,
        )
        assert delete_response.status_code == 204

        # Verify not in canvas
        canvas_response = await client.get(
            "/api/v1/business-model/canvas",
            headers=headers,
        )
        key_activities = canvas_response.json()["entries_by_component"]["key_activities"]
        assert not any(e["id"] == entry_id for e in key_activities)

    @pytest.mark.asyncio
    async def test_delete_entry_not_found(self, client: AsyncClient, headers):
        """Delete non-existent entry returns 404."""
        response = await client.delete(
            "/api/v1/business-model/entries/00000000-0000-0000-0000-000000000000",
            headers=headers,
        )
        assert response.status_code == 404


class TestBusinessModelEntryDetails:
    """Test entry with various fields."""

    @pytest.mark.asyncio
    async def test_create_entry_with_all_fields(self, client: AsyncClient, headers):
        """Create entry with all optional fields."""
        await client.get("/api/v1/business-model/canvas", headers=headers)

        payload = {
            "component": "value_propositions",
            "title": "Comprehensive Entry",
            "description": "Detailed description of the value proposition",
            "priority": 1,
            "tags": ["critical", "q1-2026"],
        }
        response = await client.post(
            "/api/v1/business-model/entries",
            json=payload,
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Detailed description of the value proposition"

    @pytest.mark.asyncio
    async def test_multiple_entries_per_component(self, client: AsyncClient, headers):
        """Component can have multiple entries."""
        await client.get("/api/v1/business-model/canvas", headers=headers)

        # Create multiple entries
        for i in range(3):
            await client.post(
                "/api/v1/business-model/entries",
                json={
                    "component": "key_partners",
                    "title": f"Partner {i+1}",
                },
                headers=headers,
            )

        # Get canvas
        canvas_response = await client.get(
            "/api/v1/business-model/canvas",
            headers=headers,
        )
        key_partners = canvas_response.json()["entries_by_component"]["key_partners"]
        partner_titles = [e["title"] for e in key_partners]
        assert "Partner 1" in partner_titles
        assert "Partner 2" in partner_titles
        assert "Partner 3" in partner_titles
