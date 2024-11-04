from typing import Any
import enum

from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, Float, DateTime, Enum
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class State(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)


class Bet(Base):
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, primary_key=True)
    coefficient = Column(Float, nullable=False)
    deadline = Column(DateTime, nullable=False)
    state = Column(Enum(State), nullable=False)
