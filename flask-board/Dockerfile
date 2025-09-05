# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=5000

WORKDIR /app

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

EXPOSE 5000

# 보안: 비루트 사용자
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 헬스체크: 루트 페이지 확인
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://127.0.0.1:$\{PORT\}/ || exit 1

# gunicorn으로 실행 (단일 워커, 개발용)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--access-logfile", "-", "--error-logfile", "-"]
