from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.core.hashing import Hasher
from bet_maker.db.models import User
from bet_maker.schemas.users import UserCreate


async def create_new_user(user: UserCreate, db: AsyncSession):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


async def get_user(username: str, db: AsyncSession):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def get_profile(current_user: User, db: AsyncSession):
    profile = await db.get(User, current_user.id)
    return profile


async def get_user_from_email(email: str, db: AsyncSession):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    return user
