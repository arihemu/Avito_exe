FROM python:3.12-slim

WORKDIR /app

ENV POETRY_VERSION=1.6.1
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml README.md /app/
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --only main

COPY . /app

RUN playwright install --with-deps chromium

CMD ["python", "-m", "avito_helper_lite.app.gui.main_window"]
