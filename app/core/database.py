from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# ----------------------------------------------------
# 1. SQLAlchemy Engine Setup
# ----------------------------------------------------

# create_async_engine is essential for FastAPI's non-blocking performance.
engine = create_async_engine(
    # The URL comes from the securely loaded settings object
    str(settings.DATABASE_URL),
    # echo=True is useful in dev for seeing SQL queries, disable in production.
    echo=True if settings.ENVIRONMENT == "dev" else False,
    # For Neon, connect_args is often not strictly necessary, but good practice
    # to explicitly define the connection behavior.
    pool_pre_ping=True
)

# ----------------------------------------------------
# 2. Database Session Setup
# ----------------------------------------------------

# AsyncSession is the class used to communicate with the database
# expire_on_commit=False prevents objects from being "detached" after commit
# This is crucial for working with models outside the session scope.
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ----------------------------------------------------
# 3. Base Class for Models
# ----------------------------------------------------

# This is the base class for all of your database models (tables)
Base = declarative_base()