import os
import uuid

import soundfile as sf
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='SoundConvert',
    description='API, который конвертирует аудиозапись из формата wav в mp3'
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_uuid(name):
    uuid_token = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
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


def check_id_and_uuid_token(db, user_id, uuid_token):
    user = db.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    user_token = user.uuid_token
    if user_token != uuid_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неверный токен'
        )
    return True


@app.post('/create_user', response_model=schemas.ResponseUser, tags=['Create user'])
def create_user(data: schemas.CreateUser, db: Session = Depends(get_db)):
    username = check_unique_username(db, data.username)
    uuid_token = generate_uuid(username)
    return save_user_to_db(db, username, uuid_token)


@app.post('/convert_audio_recording', tags=['Convert audio recording'])
def convert_audio_recording(
        user_id: int,
        user_uuid_token: str,
        wav_file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    if check_id_and_uuid_token(db, user_id, user_uuid_token):
        new_name = generate_uuid(wav_file.filename) + '.mp3'
        output_dir = "./audiofiles"
        mp3_file = os.path.join(output_dir, new_name)
        try:
            audio, sample_rate = sf.read(wav_file.file)
            os.makedirs(output_dir, exist_ok=True)

            with open(mp3_file, 'wb') as f:
                sf.write(f, audio, sample_rate, format="MP3")

        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ошибка. Проверьте, что формат файла WAV'
            )
        audio_recording = models.AudioRecording(
            uuid_name=new_name,
            path=mp3_file,
            user_id=user_id
        )
        db.add(audio_recording)
        db.commit()
        db.refresh(audio_recording)
        audio_id = audio_recording.id
        audio_user_id = audio_recording.user_id
        download_url = f'http://localhost/record?id={audio_id}&user={audio_user_id}'
        return {"download_url": download_url}


@app.get('/record', tags=['Download audio recording'])
def download_audio_recording(id: int, user: int, db: Session = Depends(get_db)):
    audio_recording = db.query(models.AudioRecording).filter(
        models.AudioRecording.id == id,
        models.AudioRecording.user_id == user).first()
    if not audio_recording:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ссылка недействительна'
        )

    file_path = audio_recording.path
    file_name = audio_recording.uuid_name
    return FileResponse(file_path, filename=file_name, media_type="application/octet-stream")
