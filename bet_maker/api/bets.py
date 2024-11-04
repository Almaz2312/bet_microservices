from bet_maker.api.login import get_current_user_form_token
from bet_maker.schemas.bet import CreateBetSchema
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from bet_maker.db.session import get_session
from bet_maker.db.models import User, Bet
from bet_maker.db.utils.bets import get_events, make_a_bet


api_router = APIRouter()


@api_router.get("/events/")
async def events():
    return await get_events()


@api_router.post("/bet/")
async def make_bet(bet: CreateBetSchema, db: AsyncSession = Depends(get_session), user: User = Depends(get_current_user_form_token)):
    bet = await make_a_bet(db, user, bet=bet)
    return bet
