import asyncio
from app.core.database import engine, Base
# We MUST import the models here so SQLAlchemy knows they exist
from app.models.coin import Coin 

async def create_tables():
    print("Connecting to Neon to create tables...")
    async with engine.begin() as conn:
        # This command looks at 'Base' and creates any tables it doesn't find
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())