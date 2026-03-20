# Dockerfile

# --- Этап 1: Сборщик (Builder) ---
# На этом этапе мы устанавливаем зависимости в отдельную директорию
FROM python:3.11-slim as builder

WORKDIR /app

# Устанавливаем переменные окружения для pip
ENV PIP_NO_CACHE_DIR=off PIP_DISABLE_PIP_VERSION_CHECK=on
# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-warn-script-location -r requirements.txt


# --- Этап 2: Финальный образ (Final Image) ---
# Здесь мы создаем легкий образ с уже установленными зависимостями
FROM python:3.11-slim

WORKDIR /app

# Копируем установленные пакеты из сборщика
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Устанавливаем curl для healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Копируем код нашего приложения
COPY . .

# HEALTHCHECK для проверки работоспособности приложения
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 CMD curl -f http://localhost:8000/health || exit 1

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
