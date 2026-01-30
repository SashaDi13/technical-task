FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt

FROM base as dev
COPY requirements-dev.txt /app
RUN pip install -r requirements-dev.txt

COPY src /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
