# REST API on FastApi

## Описание

Сервис для создания\удаления\обновления\получения\поиска обяъвлений купли и продажи.

## Функционал

- CRUD операции
- Создание: POST /advertisement
- Обновление: PATCH /advertisement/{advertisement_id}
- Удаление: DELETE /advertisement/{advertisement_id}
- Получение по id: GET  /advertisement/{advertisement_id}
- Поиск по полям: GET /advertisement?{query_string}

## Начало работы

- Необходимо установить [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Запустить команду ```docker-compose up -d```

## Стэк

1. FastApi
2. FastApi-filter
3. Alembic
4. SQLAlchemy
5. Pydantic
6. Docker
7. Docker-compose
8. Logging