from fastapi import APIRouter

from bet_maker.api import login, bets, users


api_router = APIRouter(prefix="/api/bet-maker")
api_router.include_router(login.api_router, prefix="/accounts", tags=["accounts"])
api_router.include_router(bets.api_router, prefix="/bets", tags=["bets"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
