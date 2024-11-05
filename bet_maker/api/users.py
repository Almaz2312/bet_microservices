from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.api.login import get_current_user_form_token
from bet_maker.db.models import User
from bet_maker.schemas.users import UserCreate, Profile
from bet_maker.db.utils.users import create_new_user, get_users, get_profile
from bet_maker.db.session import get_session

router = APIRouter()


@router.post("/register/", response_model=Profile)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    user = await create_new_user(user=user, db=db)
    return user


@router.get('/profile_list/', response_model=List[Profile])
async def list_users(db: AsyncSession = Depends(get_session)):
    users = await get_users(db=db)
    return users


@router.get('/profile', response_model=Profile)
async def profile(current_user: User = Depends(get_current_user_form_token), db: AsyncSession = Depends(get_session)):
    profile = await get_profile(current_user, db)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Profile with this user id {current_user.id} was not found')
    return profile
