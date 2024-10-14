# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение в контейнер
COPY . .
#
#ENV SPOTIFY_CLIENT_ID=b842adc8cbd9466eba761cd80b1626c7
#ENV SPOTIFY_CLIENT_SECRET=8f6ebfc4a37d4e67a6432b5b091c1ae1
#ENV SPOTIFY_REDIRECT_URI=http://localhost:8000/callback
#ENV YANDEX_TOKEN=y0_AgAAAAA0f6pNAAG8XgAAAAEUKU1tAAANDUHE1xlE2psLwc2E9BNo_F8n2A


# Команда по умолчанию для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
