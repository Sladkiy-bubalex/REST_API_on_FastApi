# REST API on FastApi

## Описание

Сервис для создания\удаления\обновления\получения\поиска обяъвлений купли и продажи.

## Функционал

- CRUD операции по объявлениям и пользователям
- Поиск объявлений по описанию и заголовку
- Авторизация и аутентификация
- Ограничение прав
- Миграции в БД
- Контейниризация и оркестрация

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
9. PyJWT