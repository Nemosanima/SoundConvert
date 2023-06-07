from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    username = Column(
        String,
        unique=True,
        nullable=False,
        name='Имя'
    )
    uuid_token = Column(
        String,
        nullable=False,
        name='UUID токен'
    )
    created = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
        name='Дата создания'
    )
