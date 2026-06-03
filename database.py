import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Humne yahan aapka naya password 'NayaPassword123' direct set kar diya hai
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://root:NayaPassword123@localhost:3306/polling_db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session