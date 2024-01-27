import requests
import subprocess
import time
import os
from bs4 import BeautifulSoup

# Шаг 1: Скачивание страницы

# Введите URL
url = input('\nВыбери URL ➤ ')

# Скачиваем страницу по ссылке
response = requests.get(url)
html_content = response.text

# Преобразуем относительные ссылки в абсолютные
soup = BeautifulSoup(html_content, 'html.parser')
base_url = response.url

def make_absolute_links(tag, attribute):
    if not tag[attribute].startswith(('http://', 'https://', '//')):
        tag[attribute] = base_url + tag[attribute]

# Преобразуем относительные ссылки
for tag in soup.find_all(['a', 'link'], href=True):
    make_absolute_links(tag, 'href')

for tag in soup.find_all(['img', 'script'], src=True):
    make_absolute_links(tag, 'src')

for tag in soup.find_all('img', {'data-src': True}):
    make_absolute_links(tag, 'data-src')

# Ждем некоторое время перед сохранением HTML-кода
time.sleep(5)

# Добавляем JavaScript-скрипт для обработки асинхронной загрузки изображений
script = """
<script>
    document.addEventListener("DOMContentLoaded", function() {
        var lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(function(img) {
            img.setAttribute('src', img.getAttribute('data-src'));
        });
    });
</script>
"""

# Вставляем скрипт в конец HTML-страницы
soup.body.append(BeautifulSoup(script, 'html.parser'))

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
