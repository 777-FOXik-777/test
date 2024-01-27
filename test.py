import requests
import subprocess
import time
import os

# Шаг 1: Скачивание страницы

# Замените 'http://example.com' на нужную вам ссылку
url = 'https://www.olx.ua/uk'

# Скачиваем страницу по ссылке
response = requests.get(url)
html_content = response.text

# Сохраняем HTML-код в файл
file_path = 'downloaded_page.html'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f"Страница успешно скачана и сохранена в файл {file_path}")

# Шаг 2: Запуск локального сервера

# Копируем содержимое файла в файл index.html в текущей рабочей директории
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

# Выполняем команду для запуска локального сервера на порту 8080
local_server_command = 'python -m http.server 8080'

# Запускаем команду для локального сервера с помощью subprocess
local_server_process = subprocess.Popen(local_server_command, shell=True, stdout=subprocess.PIPE)

# Печатаем сообщение о запуске локального сервера
print("Локальный сервер запущен на порту 8080")

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процесс локального сервера
    local_server_process.terminate()

    print("Скрипт завершен.")
