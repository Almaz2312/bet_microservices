import requests
from bet_maker.api.login import oauth2_schema
from bet_maker.core.config import settings
from bet_maker.db.session import get_session
from fastapi import HTTPException, Depends
from requests.adapters import HTTPAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from urllib3 import Retry

from bet_maker.db.models import User


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
    url = settings.LINE_PROVIDER_URL
    response = session.get(url=url)
    return response.json()


async def make_bet(db: AsyncSession):
    return None
