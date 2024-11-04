from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.core.hashing import Hasher
from bet_maker.db.models import User
from bet_maker.schemas.users import UserCreate


def create_new_user(user: UserCreate, db: AsyncSession):
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def get_users(db: AsyncSession):
    users = await db.execute(select(User))
    return users.fetchall()


async def get_user(username: str, db: AsyncSession):
    query = select(User).where(User.username == username)
    user = await db.execute(query).scalars().first()
    return user


async def get_profile(current_user, db: AsyncSession):
    profile = await db.get(User, current_user.id)
    return profile
