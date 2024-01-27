import requests
import subprocess
import time
import os
from bs4 import BeautifulSoup

# Шаг 1: Скачивание страницы

url = input('\nВыберите URL ➤ ')

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Ошибка при запросе страницы: {e}")
    exit()

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

# Копируем содержимое файла в файл index.html в текущей рабочей директории
index_file_path = 'index.html'
with open(index_file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

# Шаг 2: Запуск локального сервера

local_server_command = 'python -m http.server 8000'

try:
    subprocess.run(local_server_command, shell=True, check=True)
    print("Локальный сервер успешно запущен на порту 8000")
except subprocess.CalledProcessError as e:
    print(f"Ошибка при запуске локального сервера: {e}")
    exit()

# Добавляем задержку, чтобы сервер успел запуститься
time.sleep(2)

# Шаг 3: Запуск Serveo.net

try:
    subprocess.run("""ssh -R 80:localhost:8000 serveo.net -T -n 2>&1 | awk '/serveo.net/ {print $5}'""", shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Ошибка при запуске Serveo.net: {e}")

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процесс локального сервера
    subprocess.run(["pkill", "-f", "python -m http.server"])
    print("Скрипт завершен.")
