# Dockerfile для repomix с Python и генератором бандлов
FROM ubuntu:24.04

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем repomix глобально через npm
RUN npm install -g repomix

# Устанавливаем Python виртуальное окружение
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем скрипт генератора бандлов
WORKDIR /app
COPY repomix-regenerate_bundles.py /app/repomix-regenerate_bundles.py

# Делаем скрипт исполняемым
RUN chmod +x /app/repomix-regenerate_bundles.py

# Устанавливаем рабочую директорию по умолчанию
WORKDIR /workspace

# Команда по умолчанию - запуск скрипта генерации бандлов
CMD ["python3", "/app/repomix-regenerate_bundles.py"]