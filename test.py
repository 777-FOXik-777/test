import requests
import subprocess
import time
import os
from bs4 import BeautifulSoup

# Шаг 1: Скачивание страницы

# Замените 'http://example.com' на нужную вам ссылку
url = input('\n Выбери url ➤ ')

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

# Ждем некоторое время перед сохранением HTML-кода
time.sleep(5)

# Сохраняем HTML-код в файл
file_path = 'downloaded_page.html'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

print(f"Страница успешно скачана и сохранена в файл {file_path}")

# Шаг 2: Запуск локального сервера

# Создаем копию soup для сохранения в index.html
soup_copy = soup

# Копируем содержимое файла в файл index.html в текущей рабочей директории
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(str(soup_copy))

# Выполняем команду для запуска локального сервера на порту 8000 (или другом свободном порту)
local_server_command = 'python -m http.server 8000'

# Запускаем команду для локального сервера с помощью subprocess
local_server_process = subprocess.Popen(local_server_command, shell=True, stdout=subprocess.PIPE)

# Печатаем сообщение о запуске локального сервера
print("Локальный сервер запущен на порту 8000")

# Добавляем задержку, чтобы сервер успел запуститься и обработать запросы
time.sleep(5)

# Шаг 3: Запуск Serveo.net

# Используем оригинальную команду Serveo.net без изменений
tru_201 = '8000'  # Замените на нужный вам порт
os.system(f"""ssh -R 80:localhost:{tru_201} serveo.net -T -n 2>&1 | awk '/serveo.net/ {{print $5}}'""")

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процесс локального сервера
    local_server_process.terminate()

    print("Скрипт завершен.")
