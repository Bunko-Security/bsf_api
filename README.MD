# Что такое BSF
BSF – это безопасное хранилище данных со сквозным шифрованием. Это означает, что Ваши данные не могут получены без авторизации Вас или пользователя, которому был предназначен файл. Иначе говоря, даже если взломают наши сервера и базы данных, то конфиденциальность данных не нарушится.

Данный репозиторий - бэкенд BSF, представленный как REST API сервер.

# Запуск проекта
- Склонировать репозиторий
- Создать в корне проекта файл окружения со следующими полями:
```env
DB_HOST=сервер_базы_данных
DB_PORT=порт_сервера_базы_данных
DB_NAME=имя_базы_данных
DB_USER=имя_пользователя_базы_данных
DB_PASSWORD=пароль_пользователя_базы_данных

SECRET_KEY=секретный_ключ_jwt_токенов
ACCESS_TOKEN_ALIVE=время_жизни_access_токена_в_минутах # необязательное поле (по умолчанию 5)
REFRESH_TOKEN_ALIVE=время_жизни_refresh_токена_в_днях # необязательное поле (по умолчанию 7)

SERVER_SECRET_KEY=ключ_генерации_лже_хэшей

BACKEND_CORS_ORIGINS=разрешенные_хосты_(хост_фронтенда) # перечислять через запятую
```
Пример:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bunko_db
DB_USER=bunko_db_admin
DB_PASSWORD=bunko

SECRET_KEY=jwt-secret-key
ACCESS_TOKEN_ALIVE=60
REFRESH_TOKEN_ALIVE=7

SERVER_SECRET_KEY=server-secret-key

BACKEND_CORS_ORIGINS=http://localhost:3000,https:/localhost:3000
```
- Создать образ и запустить готовый контейнер
- Чтобы создать первого пользователя-администратора системы нужно запусить скрипт _createadmin.py_ командой `python3 createadmin.py` и ввести логин и пароль
- (Опционально) Если нужно инициализировать базу данных, то необходимо ввести команду `alembic upgrade head`

# Источники
- Frontend: [GitHub](https://github.com/Bunko-Security/Bunko_Security_frontend)

# Используемые технологии
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- PyCryptodome