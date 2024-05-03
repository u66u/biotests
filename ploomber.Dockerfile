FROM python:3.12.0-slim-bullseye

ENV PYTHONUNBUFFERED 1

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .

RUN wget -O app/static/js/htmx.js https://raw.githubusercontent.com/bigskysoftware/htmx/master/src/htmx.js
RUN pip install -r requirements.txt

RUN pip install uvicorn

COPY app app
COPY alembic alembic
COPY alembic.ini .
COPY pyproject.toml .

ENTRYPOINT ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]
