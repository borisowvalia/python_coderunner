FROM python:3.12-slim

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка необходимых утилит
RUN apt-get update && apt-get install -y \
    sudo \
    psmisc \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash student \
    && echo "student:student" | chpasswd

# Копируем исходники
COPY . .

# Копируем датасеты внутрь контейнера
COPY datasets ./datasets

# Запуск uvicorn
CMD ["python", "app/main.py"]