import requests
import subprocess
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Введите URL
url = input('\nВыбери URL ➤ ')

# Проверяем, что URL не пустой
if url.strip():
    # Скачиваем страницу по ссылке
    response = requests.get(url)
    html_content = response.text

    # Преобразуем относительные ссылки в абсолютные
    soup = BeautifulSoup(html_content, 'html.parser')
    base_url = response.url

    # Функция для проверки, является ли строка IP-адресом
    def is_ip_address(s):
        parts = s.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True

    # Функция для фильтрации и вывода данных
    def filter_and_print(tag, attribute):
        if 'input' in tag:
            print(tag)
        elif attribute == 'src' and tag in ['img', 'script']:
            make_absolute_links(tag, attribute)
            print(tag)

    # Преобразуем относительные ссылки
    def make_absolute_links(tag, attribute):
        if not tag[attribute].startswith(('http://', 'https://', '//')):
            tag[attribute] = urljoin(base_url, tag[attribute])

    # Выводим теги с атрибутами src и input
    for tag in soup.find_all():
        if tag.name == 'img' and 'src' in tag.attrs:
            filter_and_print(tag.name, 'src')
        elif tag.name == 'script' and 'src' in tag.attrs:
            filter_and_print(tag.name, 'src')
        elif tag.name == 'input':
            filter_and_print(tag.name, None)

    # Сохраняем HTML-код в файл
    file_path = 'downloaded_page.html'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))  # Используем prettify для более красивого форматирования

    print(f"Страница успешно скачана и сохранена в файл {file_path}")

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
        os.remove(file_path)
        print("Скрипт завершен. Все скачанные файлы удалены.")
else:
    print("Пустой URL. Пожалуйста, введите действительный URL.")
