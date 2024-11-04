from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bet_maker.db.session import get_session
from bet_maker.db.models import User, Bet
from bet_maker.api.utils import get_events


api_router = APIRouter()


@api_router.get("/events/")
async def events():
    return await get_events()


@api_router.post("/bet/")
async def make_bet(db: AsyncSession = Depends(get_session), user: User = Depends(get_current_user_form_token)):
    bet = await make_bet(db)
    return bet
