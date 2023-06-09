# sound-convert

API, который умеет конвертировать аудиофайлы из формата wav в mp3.

## Инструкция по локальному запуску

#### Клонируйте проект
В папке "wav_examples" содержатся файлы в формате WAV для тестирования. Поскольку эта папка достаточно объемная, клонирование может занять немного больше времени, чем обычно.
```
https://github.com/Nemosanima/sound-convert.git
```
#### Создайте .env файл в корневой директории проекта с вашими данными. Например:
```
DB_ENGINE=postgresql
POSTGRES_USER=nemosanima
POSTGRES_PASSWORD=1n2nn3nnn
POSTGRES_DB=questions
DB_HOST=db
DB_PORT=5432
```
#### В корневой директории проект выполните команду
```
docker-compose up -d --build
```
#### Документация
```
http://localhost/docs  # Swagger
http://localhost/redoc # ReDoc
```
## Краткий обзор

Все запросы можно сделать из документации Swagger

![convert_audio_recording](https://github.com/Nemosanima/SoundConvert/blob/main/images/convert_audio_recording.png)

#### Создать пользователя. http метод post
```
http://localhost/create_user
```
```
# Request body
{
  "username": "Nemosanima"
}
```
```
# Response body
{
  "id": 10,
  "uuid_token": "155ab1cd-8b92-578b-93a3-ba87d1244f2a"
}
```
#### Конвертировать аудиофайл из формата wav в mp3. http метод post
```
http://localhost/convert_audio_recording
```
```
# Parameters
user_id
user_uuid_token
wav_file
```
```
# Response body
{
  "download_url": "http://localhost/record?id=2&user=1"
}
```
#### Скачать аудиофайл в формате mp3. http метод get
```
http://localhost/record?id=2&user=1
```
