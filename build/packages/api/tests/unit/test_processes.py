"""
Unit tests for Process Catalogue CRUD endpoints.
"""

import pytest
from httpx import AsyncClient


async def get_headers(client: AsyncClient) -> dict[str, str]:
    """Get auth headers via dev-login."""
    response = await client.post("/api/v1/auth/dev-login")
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestProcessList:
    """Test process listing and filtering."""

    @pytest.mark.asyncio
    async def test_list_processes_unauthorized(self, client: AsyncClient):
        """List processes without auth returns 401."""
        response = await client.get("/api/v1/processes/")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_list_processes_empty(self, client: AsyncClient, headers):
        """List processes returns empty list initially."""
        response = await client.get("/api/v1/processes/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["page"] == 1


class TestProcessCRUD:
    """Test full CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_process(self, client: AsyncClient, headers):
        """Create a new process."""
        payload = {
            "code": "L0-01",
            "name": "Sourcing",
            "description": "Core sourcing value chain",
            "level": "L0",
            "process_type": "primary",
            "current_automation": "manual",
        }
        response = await client.post(
            "/api/v1/processes/",
            json=payload,
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == "L0-01"
        assert data["name"] == "Sourcing"
        assert data["level"] == "L0"
        assert data["status"] in ("active", "draft")  # default may vary
        assert "id" in data
        return data["id"]

    @pytest.mark.asyncio
    async def test_get_process(self, client: AsyncClient, headers):
        """Create and retrieve a process."""
        # Create first
        create_response = await client.post(
            "/api/v1/processes/",
            json={
                "code": "L0-02",
                "name": "Supply Chain",
                "level": "L0",
            },
            headers=headers,
        )
        process_id = create_response.json()["id"]

        # Get it
        response = await client.get(
            f"/api/v1/processes/{process_id}",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == process_id
        assert data["code"] == "L0-02"

    @pytest.mark.asyncio
    async def test_get_process_not_found(self, client: AsyncClient, headers):
        """Get non-existent process returns 404."""
        response = await client.get(
            "/api/v1/processes/00000000-0000-0000-0000-000000000000",
            headers=headers,
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_process(self, client: AsyncClient, headers):
        """Update a process."""
        # Create first
        create_response = await client.post(
            "/api/v1/processes/",
            json={
                "code": "L0-03",
                "name": "Original Name",
                "level": "L0",
            },
            headers=headers,
        )
        process_id = create_response.json()["id"]

        # Update it
        response = await client.patch(
            f"/api/v1/processes/{process_id}",
            json={"name": "Updated Name", "description": "New description"},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "New description"

    @pytest.mark.asyncio
    async def test_delete_process(self, client: AsyncClient, headers):
        """Delete a process (soft delete to archived)."""
        # Create first
        create_response = await client.post(
            "/api/v1/processes/",
            json={
                "code": "L0-04",
                "name": "To Be Deleted",
                "level": "L0",
            },
            headers=headers,
        )
        process_id = create_response.json()["id"]

        # Delete it
        response = await client.delete(
            f"/api/v1/processes/{process_id}",
            headers=headers,
        )
        assert response.status_code == 204

        # Verify it's archived (still accessible but status changed)
        get_response = await client.get(
            f"/api/v1/processes/{process_id}",
            headers=headers,
        )
        assert get_response.status_code == 200
        assert get_response.json()["status"] == "archived"


class TestProcessFiltering:
    """Test filtering and search."""

    @pytest.mark.asyncio
    async def test_filter_by_level(self, client: AsyncClient, headers):
        """Filter processes by level."""
        # Create L0 and L1 processes
        await client.post(
            "/api/v1/processes/",
            json={"code": "L0-10", "name": "L0 Process", "level": "L0"},
            headers=headers,
        )
        await client.post(
            "/api/v1/processes/",
            json={"code": "L1-10", "name": "L1 Process", "level": "L1"},
            headers=headers,
        )

        # Filter by L0
        response = await client.get(
            "/api/v1/processes/?level=L0",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        for item in data["items"]:
            assert item["level"] == "L0"

    @pytest.mark.asyncio
    async def test_search_processes(self, client: AsyncClient, headers):
        """Search processes by name."""
        await client.post(
            "/api/v1/processes/",
            json={"code": "L0-20", "name": "Unique Procurement", "level": "L0"},
            headers=headers,
        )

        response = await client.get(
            "/api/v1/processes/?search=Procurement",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert any("Procurement" in item["name"] for item in data["items"])


class TestProcessTree:
    """Test process tree endpoint."""

    @pytest.mark.asyncio
    async def test_get_tree(self, client: AsyncClient, headers):
        """Get process tree structure."""
        response = await client.get(
            "/api/v1/processes/tree",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestProcessHierarchy:
    """Test parent-child relationships."""

    @pytest.mark.asyncio
    async def test_create_child_process(self, client: AsyncClient, headers):
        """Create a child process with parent reference."""
        # Create parent
        parent_response = await client.post(
            "/api/v1/processes/",
            json={"code": "L0-30", "name": "Parent Process", "level": "L0"},
            headers=headers,
        )
        parent_id = parent_response.json()["id"]

        # Create child
        child_response = await client.post(
            "/api/v1/processes/",
            json={
                "code": "L1-30",
                "name": "Child Process",
                "level": "L1",
                "parent_id": parent_id,
            },
            headers=headers,
        )
        assert child_response.status_code == 201
        child_data = child_response.json()
        assert child_data["parent_id"] == parent_id

    @pytest.mark.asyncio
    async def test_filter_by_parent(self, client: AsyncClient, headers):
        """Filter processes by parent_id."""
        # Create parent
        parent_response = await client.post(
            "/api/v1/processes/",
            json={"code": "L0-40", "name": "Parent", "level": "L0"},
            headers=headers,
        )
        parent_id = parent_response.json()["id"]

        # Create child
        await client.post(
            "/api/v1/processes/",
            json={
                "code": "L1-40",
                "name": "Child",
                "level": "L1",
                "parent_id": parent_id,
            },
            headers=headers,
        )

        # Filter by parent
        response = await client.get(
            f"/api/v1/processes/?parent_id={parent_id}",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        for item in data["items"]:
            assert item["parent_id"] == parent_id
