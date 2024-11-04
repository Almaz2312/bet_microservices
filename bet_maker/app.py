from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bet_maker.core.config import settings
from bet_maker.api.base import api_router
from bet_maker.db.session import engine
from bet_maker.db.models import Base


def include_router(app):
    app.include_router(api_router)


async def create_tables():
    await Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION,
                  openapi_url="/api/bet-maker/openapi.json", docs_url="/api/bet-maker/docs")

    app.add_middleware(CORSMiddleware, allow_origins=["*"],
                       allow_credentials=True, allow_methods=["*"],
                       allow_headers=["*"])
    include_router(app)
    create_tables()
    return app


app = start_application()