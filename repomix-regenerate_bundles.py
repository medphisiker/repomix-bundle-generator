#!/usr/bin/env python3
"""
Скрипт для перегенерации всех бандлов repomix на основе конфигурации в .repomix/bundles.json
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

def check_repomix_installed():
    """Проверяет, установлен ли repomix"""
    try:
        subprocess.run(["repomix", "--version"],
                      check=True,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def generate_bundle(files, bundle_name):
    """Генерирует бандл с помощью repomix"""
    if not files:
        print(f"Нет файлов для генерации бандла {bundle_name}")
        return False

    # Создаем временный файл со списком файлов
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write("\n".join(files))
        temp_file_path = temp_file.name

    try:
        # Формируем команду repomix с форматом markdown
        output_file = f"repomix-{bundle_name}-output.md"
        command = ["repomix", "--stdin", "--output", output_file, "--style", "markdown"]

        print(f"Генерация бандла {bundle_name}...")

        # Запускаем repomix
        with open(temp_file_path, 'r') as f:
            result = subprocess.run(command,
                                  stdin=f,
                                  check=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

        print(f"Сгенерирован файл: {output_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при генерации бандла {bundle_name}:")
        print(e.stderr)
        return False
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)

def main():
    # Проверяем наличие repomix
    if not check_repomix_installed():
        print("Ошибка: repomix не установлен. Установите его с помощью:")
        print("npm install -g repomix")
        sys.exit(1)

    # Путь к файлу конфигурации
    bundles_file = Path(".repomix/bundles.json")

    if not bundles_file.exists():
        print(f"Ошибка: файл {bundles_file} не найден")
        sys.exit(1)

    # Читаем конфигурацию
    try:
        with open(bundles_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)

    # Обрабатываем каждый бандл
    bundles = config.get("bundles", {})
    if not bundles:
        print("В конфигурации не найдены бандлы")
        return

    print(f"Найдено бандлов: {len(bundles)}")

    for bundle_key, bundle_data in bundles.items():
        bundle_name = bundle_data.get("name", bundle_key)
        files = bundle_data.get("files", [])

        # Проверяем существование файлов
        valid_files = []
        for file_path in files:
            if os.path.exists(file_path):
                valid_files.append(file_path)
            else:
                print(f"Предупреждение: файл или директория {file_path} не найден")

        # Генерируем бандл
        generate_bundle(valid_files, bundle_name)

    print("Генерация бандлов завершена")

if __name__ == "__main__":
    main()