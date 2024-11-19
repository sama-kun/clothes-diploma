# Базовый образ
FROM python:3.12-slim

# Установить системные зависимости
# Установить системные зависимости
RUN apt-get update && apt-get install -y \
  libjpeg-dev \
  zlib1g-dev \
  libpng-dev \
  libfreetype6-dev \
  libwebp-dev \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Установить рабочую директорию
WORKDIR /app

# Скопировать файлы проекта
COPY requirements.txt .

# Установить Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать остальной код
COPY . .

# Указать команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]