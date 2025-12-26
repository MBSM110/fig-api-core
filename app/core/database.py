from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# 1. engine setup with your environment-aware logging and connection check
engine = create_async_engine(
    str(settings.DATABASE_URL),
    # Automatically shows SQL in terminal only during development
    echo=True if settings.ENVIRONMENT == "dev" else False,
    # Checks connection health before use (standard for professional DB ops)
    pool_pre_ping=True
)

# 2. Restoring your session maker name
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 3. Standard Base for SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

# 4. Your original get_db dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()