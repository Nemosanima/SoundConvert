# SoundConvert

SoundConvert - api, который умеет конвертировать аудиофайлы из формата wav в mp3.

## Инструкция по локальному запуску

#### Клонируйте проект
```
git clone 
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