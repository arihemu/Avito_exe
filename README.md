# Avito Helper Lite

Skeleton application to collect stats, track competitors and manage descriptions on Avito.

## Requirements
- Docker and docker-compose

## Quick start
```bash
cp .env.example .env
# fill credentials

# build and run services
docker-compose up --build
```
The GUI window will appear from the `app` container. Use it to update API keys or descriptions.

## Development

Install Poetry and Python 3.12.
```bash
poetry install
poetry run python -m avito_helper_lite.app.gui.main_window
```

Run formatting and tests:
```bash
poetry run black .
poetry run mypy avito_helper_lite
pytest
```

Database migrations managed by Alembic:
```bash
poetry run alembic revision --autogenerate -m "message"
poetry run alembic upgrade head
```


