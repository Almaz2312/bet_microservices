import requests
from bet_maker.api.login import oauth2_schema
from bet_maker.core.config import settings
from bet_maker.db.session import get_session
from bet_maker.schemas.bet import CreateBetSchema, EventSchema
from fastapi import HTTPException, Depends
from requests.adapters import HTTPAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from urllib3 import Retry

from bet_maker.db.models import User, Bet


class AutoClosingSession:
    def __init__(self):
        retry_strategy = Retry(
            total=4,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def __getattr__(self, attr):
        return getattr(self.session, attr)

    def request(self, *args, **kwargs):
        try:
            return self.session.request(*args, **kwargs)
        finally:
            self.session.close()


async def get__rq_session():
    return AutoClosingSession()


async def get_events():
    session = await get__rq_session()
    url = settings.LINE_PROVIDER_URL + "events/"
    response = session.get(url=url)
    data = response.json()
    return [EventSchema(**event) for event in data]


async def get_event(event_id: int) -> EventSchema|None:
    session = await get__rq_session()
    url = settings.LINE_PROVIDER_URL + f"event/{event_id}/"
    response = session.get(url=url)
    if response.json() and response.status_code == 200:
        return EventSchema(**response.json())
    return None


async def make_a_bet(db: AsyncSession, user: User, bet: CreateBetSchema):
    event = await get_event(bet.event_id)
    if not event:
        return None

    new_bet = Bet(
        event_id=bet.event_id,
        coefficient=event.coefficient,
        deadline=event.deadline.replace(tzinfo=None),
        state=event.state.name,
        user_id=user.id,
        bet_sum=bet.bet_sum
    )
    db.add(new_bet)
    await db.commit()
    await db.refresh(new_bet)
    return new_bet


async def get_a_bet(bet_id: int, db: AsyncSession):
    result = await db.execute(select(Bet, bet_id))
    bet = result.scalars().first()
    return bet
