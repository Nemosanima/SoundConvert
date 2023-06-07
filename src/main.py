import uuid
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='Mp3'
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_uuid_token(username):
    uuid_token = str(uuid.uuid5(uuid.NAMESPACE_DNS, username))
    return uuid_token


def save_user_to_db(db, username, uuid_token):
    new_user = models.User(
        username=username,
        uuid_token=uuid_token
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def check_unique_username(db, username):
    user = db.query(models.User).filter_by(username=username).first()
    if not user:
        return username
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f'Пользователь c именем {username} уже существует'
    )


@app.post('/create_user', response_model=schemas.ResponseUser, tags=['Create user'])
def create_user(data: schemas.CreateUser, db: Session = Depends(get_db)):
    username = check_unique_username(db, data.username)
    uuid_token = generate_uuid_token(username)
    return save_user_to_db(db, username, uuid_token)
