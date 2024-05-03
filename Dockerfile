FROM python:3.12.0-slim-bullseye

ENV PYTHONUNBUFFERED 1
WORKDIR /build

RUN apt-get update -y && apt-get install -y gcc
# Create venv, add it to path and install requirements
RUN python -m venv .venv
ENV PATH=".venv/bin:$PATH"

COPY .env .env
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# Copy the rest of app
COPY app app
COPY alembic alembic
COPY alembic.ini .
COPY pyproject.toml .
COPY init.sh .

ENTRYPOINT ["gunicorn", "app.main:app", "-w 4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
EXPOSE 8000
