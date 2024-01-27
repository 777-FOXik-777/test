import requests
import subprocess
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import socket

# Получение IP-адреса клиента
def get_client_ip():
    try:
        ip = requests.get('https://api64.ipify.org?format=json').json()['ip']
    except Exception as e:
        print(f"Ошибка при получении IP-адреса: {str(e)}")
        ip = "unknown"
    return ip

# Логирование IP и текста
def log_ip_and_text(ip, text):
    log_file_path = 'log.txt'
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"IP: {ip}, Text: {text}\n")

# Шаг 1: Скачивание страницы

# Введите URL
url = input('\nВыбери URL ➤ ')

# Скачиваем страницу по ссылке
response = requests.get(url)
html_content = response.text

# Преобразуем относительные ссылки в абсолютные
soup = BeautifulSoup(html_content, 'html.parser')
base_url = response.url

# ... (остальной код не изменяется)

# Сохраняем HTML-код в файл
file_path = 'downloaded_page.html'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup.prettify()))  # Используем prettify для более красивого форматирования

# Получаем IP и введенный текст
client_ip = get_client_ip()
input_text = input('\nВведите текст для логирования ➤ ')

# Логируем IP и введенный текст
log_ip_and_text(client_ip, input_text)

print(f"Страница успешно скачана и сохранена в файл {file_path}")

# Шаг 2: Запуск локального сервера

# Создаем копию soup для сохранения в index.html
soup_copy = soup

# Копируем содержимое файла в файл index.html в текущей рабочей директории
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(str(soup_copy.prettify()))

# Выполняем команду для запуска локального сервера на порту 8000 (или другом свободном порту)
local_server_command = 'python -m http.server 8000'

# Запускаем команду для локального сервера с помощью subprocess
local_server_process = subprocess.Popen(local_server_command, shell=True, stdout=subprocess.PIPE)

# Печатаем сообщение о запуске локального сервера
print("Локальный сервер запущен на порту 8000")

# Шаг 3: Запуск Serveo.net

# Используем оригинальную команду Serveo.net без изменений
tru_201 = '8000'  # Замените на нужный вам порт
serveo_command = f"ssh -q -R 80:localhost:{tru_201} serveo.net -T"
serveo_process = subprocess.Popen(serveo_command, shell=True, stdout=subprocess.PIPE)

# Получаем public URL из вывода процесса Serveo
serveo_url = serveo_process.stdout.readline().strip().decode('utf-8').split()[-1]

print(f"Файл доступен по следующему public URL: {serveo_url}")

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процессы локального сервера и Serveo.net
    local_server_process.terminate()
    serveo_process.terminate()

    # Удаляем все скачанные файлы
    if os.path.exists('images'):
        for file in os.listdir('images'):
            file_path = os.path.join('images', file)
            os.remove(file_path)
        os.rmdir('images')

    os.remove('index.html')
    os.remove('downloaded_page.html')

    print("Скрипт завершен. Все скачанные файлы удалены.")
