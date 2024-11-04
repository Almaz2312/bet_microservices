from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from typing import Generator

from bet_maker.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_session() -> Generator:
    try:
        session = SessionLocal()
        yield session

    except Exception:
        await session.rollback()

    finally:
        await session.close()


