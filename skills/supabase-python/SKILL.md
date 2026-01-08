---
name: supabase-python
description: FastAPI with Supabase and SQLAlchemy/SQLModel
---

# Supabase + Python Skill

*Load with: base.md + supabase.md + python.md*

FastAPI patterns with Supabase Auth and SQLAlchemy/SQLModel for database access.

**Sources:** [Supabase Python Client](https://supabase.com/docs/reference/python/introduction) | [SQLModel](https://sqlmodel.tiangolo.com/)

---

## Core Principle

**SQLAlchemy/SQLModel for queries, Supabase for auth/storage.**

Use SQLAlchemy or SQLModel for type-safe database access. Use supabase-py for auth, storage, and realtime. FastAPI for the API layer.

---

## Project Structure

```
project/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── posts.py
│   │   │   └── users.py
│   │   └── deps.py              # Dependencies (auth, db)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Settings
│   │   └── security.py          # Auth helpers
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py           # Database session
│   │   └── models.py            # SQLModel models
│   ├── services/
│   │   ├── __init__.py
│   │   └── supabase.py          # Supabase client
│   └── main.py                  # FastAPI app
├── supabase/
│   ├── migrations/
│   └── config.toml
├── alembic/                     # Alembic migrations (alternative)
├── alembic.ini
├── pyproject.toml
└── .env
```

---

## Setup

### Install Dependencies
```bash
pip install fastapi uvicorn supabase python-dotenv sqlmodel asyncpg alembic
```

### pyproject.toml
```toml
[project]
name = "my-app"
version = "0.1.0"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "supabase>=2.0.0",
    "python-dotenv>=1.0.0",
    "sqlmodel>=0.0.14",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
    "pydantic-settings>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.26.0",
]
```

### Environment Variables
```bash
# .env
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=<from supabase start>
SUPABASE_SERVICE_ROLE_KEY=<from supabase start>
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:54322/postgres
```

---

## Configuration

### src/core/config.py
```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    # Database
    database_url: str

    # App
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## Database Setup

### src/db/session.py
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### src/db/models.py
```python
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class ProfileBase(SQLModel):
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None


class Profile(ProfileBase, table=True):
    __tablename__ = "profiles"

    id: UUID = Field(primary_key=True)  # References auth.users
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProfileCreate(ProfileBase):
    id: UUID


class ProfileRead(ProfileBase):
    id: UUID
    created_at: datetime


class PostBase(SQLModel):
    title: str
    content: Optional[str] = None
    published: bool = False


class Post(PostBase, table=True):
    __tablename__ = "posts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    author_id: UUID = Field(foreign_key="profiles.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: UUID
    author_id: UUID
    created_at: datetime
```

---

## Supabase Client

### src/services/supabase.py
```python
from supabase import create_client, Client
from src.core.config import get_settings

settings = get_settings()


def get_supabase_client() -> Client:
    """Get Supabase client with anon key (respects RLS)."""
    return create_client(
        settings.supabase_url,
        settings.supabase_anon_key
    )


def get_supabase_admin() -> Client:
    """Get Supabase client with service role (bypasses RLS)."""
    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key
    )
```

---

## Auth Dependencies

### src/api/deps.py
```python
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from supabase import Client

from src.db.session import get_db
from src.services.supabase import get_supabase_client

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    """Validate JWT and return user."""
    supabase = get_supabase_client()

    try:
        # Verify token with Supabase
        user = supabase.auth.get_user(credentials.credentials)
        if not user or not user.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return user.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# Type alias for dependency injection
CurrentUser = Annotated[dict, Depends(get_current_user)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
```

---

## API Routes

### src/api/routes/auth.py
```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from src.services.supabase import get_supabase_client

router = APIRouter(prefix="/auth", tags=["auth"])


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str


@router.post("/signup", response_model=AuthResponse)
async def sign_up(request: SignUpRequest):
    supabase = get_supabase_client()

    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
        })

        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Signup failed",
            )

        return AuthResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=str(response.user.id),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/signin", response_model=AuthResponse)
async def sign_in(request: SignInRequest):
    supabase = get_supabase_client()

    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })

        return AuthResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=str(response.user.id),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.post("/signout")
async def sign_out():
    supabase = get_supabase_client()
    supabase.auth.sign_out()
    return {"message": "Signed out"}
```

### src/api/routes/posts.py
```python
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from src.api.deps import CurrentUser, DbSession
from src.db.models import Post, PostCreate, PostRead

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostRead])
async def list_posts(
    db: DbSession,
    published_only: bool = True,
):
    query = select(Post)
    if published_only:
        query = query.where(Post.published == True)
    query = query.order_by(Post.created_at.desc())

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/me", response_model=list[PostRead])
async def list_my_posts(
    db: DbSession,
    user: CurrentUser,
):
    query = select(Post).where(Post.author_id == UUID(user.id))
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    db: DbSession,
    user: CurrentUser,
    post_in: PostCreate,
):
    post = Post(
        **post_in.model_dump(),
        author_id=UUID(user.id),
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    db: DbSession,
    post_id: UUID,
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    db: DbSession,
    user: CurrentUser,
    post_id: UUID,
):
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.author_id == UUID(user.id))
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    await db.delete(post)
    await db.commit()
```

---

## Main Application

### src/main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import auth, posts

app = FastAPI(title="My API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api")
app.include_router(posts.router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## Alembic Migrations

### Initialize Alembic
```bash
alembic init alembic
```

### alembic/env.py (key changes)
```python
from src.db.models import SQLModel
from src.core.config import get_settings

settings = get_settings()

# Use async engine
config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = SQLModel.metadata


def run_migrations_online():
    # For async
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine

    connectable = create_async_engine(settings.database_url)

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations_sync)

    def do_run_migrations_sync(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(do_run_migrations())
```

### Migration Commands
```bash
# Create migration
alembic revision --autogenerate -m "create posts table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Storage

### Upload File
```python
from fastapi import UploadFile
from src.services.supabase import get_supabase_client


async def upload_avatar(user_id: str, file: UploadFile) -> str:
    supabase = get_supabase_client()

    file_content = await file.read()
    file_path = f"{user_id}/avatar.{file.filename.split('.')[-1]}"

    response = supabase.storage.from_("avatars").upload(
        file_path,
        file_content,
        {"content-type": file.content_type, "upsert": "true"},
    )

    # Get public URL
    url = supabase.storage.from_("avatars").get_public_url(file_path)
    return url
```

### Download File
```python
def get_avatar_url(user_id: str) -> str:
    supabase = get_supabase_client()
    return supabase.storage.from_("avatars").get_public_url(f"{user_id}/avatar.png")
```

---

## Realtime (Async)

```python
import asyncio
from supabase import create_client


async def listen_to_posts():
    supabase = create_client(
        settings.supabase_url,
        settings.supabase_anon_key
    )

    def handle_change(payload):
        print(f"Change received: {payload}")

    channel = supabase.channel("posts")
    channel.on_postgres_changes(
        event="*",
        schema="public",
        table="posts",
        callback=handle_change,
    ).subscribe()

    # Keep listening
    while True:
        await asyncio.sleep(1)
```

---

## Testing

### tests/conftest.py
```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.session import get_db
from src.db.models import SQLModel

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:54322/postgres_test"

engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
```

### tests/test_posts.py
```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_posts(client: AsyncClient):
    response = await client.get("/api/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

## Running the App

```bash
# Development
uvicorn src.main:app --reload --port 8000

# Production
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Anti-Patterns

- **Using Supabase client for DB queries** - Use SQLAlchemy/SQLModel
- **Sync database calls** - Use async with asyncpg
- **Hardcoded credentials** - Use environment variables
- **No connection pooling** - asyncpg handles this
- **Missing auth dependency** - Always validate JWT
- **Not closing sessions** - Use context managers
- **Blocking I/O in async** - Use async libraries
