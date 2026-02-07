"""
Pytest fixtures for Process Catalogue API tests.

Provides:
- Async database session with transaction rollback
- Test organization and user
- Authenticated test client
- RLS context setup
"""

import os

# Set test environment before app/settings are imported.
# This disables rate limiting middleware and decorator checks.
os.environ["ENVIRONMENT"] = "test"

from typing import AsyncGenerator
from uuid import uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.core.auth import create_access_token
from src.core.database import get_db
from src.main import app
from src.models.organization import (
    AllowedDomain,
    Organization,
    User,
    UserOrganization,
)


# Use a separate test database or the same with transaction rollback
TEST_DATABASE_URL = settings.DATABASE_URL


@pytest_asyncio.fixture
async def engine():
    """Create async engine for tests."""
    _engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_size=5,
        max_overflow=0,
    )
    yield _engine
    await _engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a transactional database session for each test.
    Rolls back after each test for isolation.
    """
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        # Start a savepoint for rollback
        await session.begin_nested()
        yield session
        # Rollback to clean up test data
        await session.rollback()


@pytest_asyncio.fixture
async def test_org(db_session: AsyncSession) -> Organization:
    """Create a test organization."""
    org = Organization(
        id=str(uuid4()),
        name="Test Organization",
        slug=f"test-org-{uuid4().hex[:8]}",
        subscription_tier="pro",
        settings={"theme": "default"},
        is_active=True,
    )
    db_session.add(org)

    # Add allowed domain
    domain = AllowedDomain(
        id=str(uuid4()),
        organization_id=org.id,
        domain="test.local",
        is_verified=True,
    )
    db_session.add(domain)

    await db_session.flush()
    return org


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession, test_org: Organization) -> User:
    """Create a test user with admin role."""
    user = User(
        id=str(uuid4()),
        email=f"testuser-{uuid4().hex[:8]}@test.local",
        display_name="Test User",
        default_organization_id=test_org.id,
        is_active=True,
    )
    db_session.add(user)

    membership = UserOrganization(
        id=str(uuid4()),
        user_id=user.id,
        organization_id=test_org.id,
        role="admin",
        status="active",
    )
    db_session.add(membership)

    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def auth_token(test_user: User, test_org: Organization) -> str:
    """Create a valid JWT access token for the test user."""
    return create_access_token(
        user_id=test_user.id,
        organization_id=test_org.id,
        role="admin",
        email=test_user.email,
    )


@pytest_asyncio.fixture
async def auth_headers(auth_token: str) -> dict[str, str]:
    """HTTP headers with authentication."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Async test client for API testing.
    Uses the real database - dev-login creates its own test data.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def authenticated_client(client: AsyncClient) -> AsyncClient:
    """Test client with auth headers from dev-login."""
    # Get tokens via dev-login
    response = await client.post("/api/v1/auth/dev-login")
    tokens = response.json()
    client.headers.update({"Authorization": f"Bearer {tokens['access_token']}"})
    return client


@pytest_asyncio.fixture
async def headers(client: AsyncClient) -> dict[str, str]:
    """Auth headers from dev-login for simple test usage."""
    response = await client.post("/api/v1/auth/dev-login")
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


# Utility fixtures for specific test scenarios


@pytest_asyncio.fixture
async def viewer_user(db_session: AsyncSession, test_org: Organization) -> User:
    """Create a user with viewer role (limited permissions)."""
    user = User(
        id=str(uuid4()),
        email=f"viewer-{uuid4().hex[:8]}@test.local",
        display_name="Viewer User",
        default_organization_id=test_org.id,
        is_active=True,
    )
    db_session.add(user)

    membership = UserOrganization(
        id=str(uuid4()),
        user_id=user.id,
        organization_id=test_org.id,
        role="viewer",
        status="active",
    )
    db_session.add(membership)

    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def viewer_token(viewer_user: User, test_org: Organization) -> str:
    """JWT token for viewer user."""
    return create_access_token(
        user_id=viewer_user.id,
        organization_id=test_org.id,
        role="viewer",
        email=viewer_user.email,
    )
