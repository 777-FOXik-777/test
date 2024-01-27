import requests
import subprocess
import time
import os
from bs4 import BeautifulSoup

def download_page(url):
    # Шаг 1: Скачивание страницы
    response = requests.get(url)
    html_content = response.text

    # Преобразуем относительные ссылки в абсолютные
    soup = BeautifulSoup(html_content, 'html.parser')
    base_url = response.url
    for tag in soup.find_all(['a', 'link'], href=True):
        tag['href'] = urljoin(base_url, tag['href'])
    for tag in soup.find_all(['img', 'script'], src=True):
        tag['src'] = urljoin(base_url, tag['src'])
    for tag in soup.find_all('img', {'data-src': True}):
        tag['data-src'] = urljoin(base_url, tag['data-src'])

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

    return soup

def save_html_to_file(soup, file_path):
    # Сохраняем HTML-код в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Страница успешно скачана и сохранена в файл {file_path}")

def run_local_server():
    # Шаг 2: Запуск локального сервера
    local_server_command = 'python -m http.server 8000'
    local_server_process = subprocess.Popen(local_server_command, shell=True, stdout=subprocess.PIPE)

    # Печатаем сообщение о запуске локального сервера
    print("Локальный сервер запущен на порту 8000")

    # Добавляем задержку, чтобы сервер успел запуститься и обработать запросы
    time.sleep(5)

    return local_server_process

def expose_local_server(port):
    # Шаг 3: Запуск Serveo.net
    os.system(f"ssh -R 80:localhost:{port} serveo.net -T -n 2>&1 | awk '/serveo.net/ {{print $5}}'")

if __name__ == "__main__":
    url = input('\nВыбери url ➤ ')

    # Шаг 1: Скачивание страницы
    soup = download_page(url)

    # Шаг 2: Сохранение обработанного HTML в файл
    save_html_to_file(soup, 'downloaded_page.html')

    # Шаг 2: Запуск локального сервера
    local_server_process = run_local_server()

    # Шаг 3: Запуск Serveo.net
    expose_local_server(8000)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Прерываем выполнение при нажатии Ctrl+C

        # Завершаем процесс локального сервера
        local_server_process.terminate()

        print("Скрипт завершен.")
