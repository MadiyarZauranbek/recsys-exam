# Используем легкий образ Python
FROM python:3.10-slim

# Устанавливаем рабочую папку внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта внутрь контейнера
COPY . .

# Порты (для документации)
EXPOSE 8000
EXPOSE 8501

# Команда запуска по умолчанию (будет переопределена в docker-compose)
CMD ["python", "api.py"]