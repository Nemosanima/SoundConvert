from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
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
    audio_recordings = relationship(
        'AudioRecording',
        back_populates='user'
    )
    created = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
        name='Дата создания'
    )


class AudioRecording(Base):
    __tablename__ = 'audio_recordings'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    uuid_name = Column(
        String,
        nullable=False,
        name='UUID имя для файла'
    )
    path = Column(
        String,
        nullable=False,
        name='Ссылка на mp3 файл'
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        name='Пользователь'
    )
    user = relationship(
        'User',
        back_populates='audio_recordings'
    )
    created = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
        name='Дата создания'
    )
