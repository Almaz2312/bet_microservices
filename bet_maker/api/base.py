from fastapi import APIRouter

from bet_maker.api import login, bets


api_router = APIRouter(prefix="/api/bet-maker")
api_router.include_router(login.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(bets.api_router, prefix="/bets", tags=["bets"])
