from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# ----------------------------------------------------
# 1. SQLAlchemy Engine Setup (Keep this the same)
# ----------------------------------------------------
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=True if settings.ENVIRONMENT == "dev" else False,
    pool_pre_ping=True
)

# ----------------------------------------------------
# 2. Database Session Setup (Updated to use async_sessionmaker)
# ----------------------------------------------------
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

# 3. Base Class (Keep the same)
Base = declarative_base()

# ----------------------------------------------------
# 4. Dependency for FastAPI Routes (The missing piece)
# ----------------------------------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()