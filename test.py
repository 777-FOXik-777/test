import requests
import subprocess
import time
import os
from bs4 import BeautifulSoup

# Шаг 1: Скачивание страницы

# Замените 'http://example.com' на нужную вам ссылку
url = 'https://www.olx.ua/uk'

# Скачиваем страницу по ссылке
response = requests.get(url)
html_content = response.text

# Преобразуем относительные ссылки в абсолютные
soup = BeautifulSoup(html_content, 'html.parser')
base_url = response.url
for tag in soup.find_all(['a', 'link', 'img', 'script'], href=True):
    if not tag['href'].startswith(('http://', 'https://', '//')):
        tag['href'] = base_url + tag['href']
for tag in soup.find_all(['img', 'script'], src=True):
    if not tag['src'].startswith(('http://', 'https://', '//')):
        tag['src'] = base_url + tag['src']

# Сохраняем HTML-код в файл
file_path = 'downloaded_page.html'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

print(f"Страница успешно скачана и сохранена в файл {file_path}")

# Шаг 2: Запуск локального сервера

# Копируем содержимое файла в файл index.html в текущей рабочей директории
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

# Выполняем команду для запуска локального сервера на порту 8000 (или другом свободном порту)
local_server_command = 'python -m http.server 8000'

# Запускаем команду для локального сервера с помощью subprocess
local_server_process = subprocess.Popen(local_server_command, shell=True, stdout=subprocess.PIPE)

# Печатаем сообщение о запуске локального сервера
print("Локальный сервер запущен на порту 8000")

# Шаг 3: Запуск Serveo.net

# Добавляем задержку, чтобы сервер успел запуститься
time.sleep(2)

# Запускаем команду для Serveo.net с помощью subprocess
serveo_command = """ssh -R 80:localhost:8000 serveo.net -T -n 2>&1 | awk '/serveo.net/ {print $5}'"""
serveo_process = subprocess.Popen(serveo_command, shell=True, stdout=subprocess.PIPE)

# Получаем вывод команды (URL Serveo)
serveo_output = serveo_process.stdout.read().decode('utf-8').strip()

# Печатаем URL Serveo
print(f"Ваша страница теперь доступна по ссылке Serveo: {serveo_output}")

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процесс локального сервера
    local_server_process.terminate()

    # Завершаем процесс Serveo.net
    serveo_process.terminate()

    print("Скрипт завершен.")
