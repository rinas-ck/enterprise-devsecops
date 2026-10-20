FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY services/ ./services/

RUN useradd --system --uid 10001 appuser

USER 10001

EXPOSE 8000

CMD ["python3", "services/api/app.py"]
