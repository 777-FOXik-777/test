import requests
import subprocess
import time
import os
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

    # Проверяем наличие форм на странице и мониторим их
    def monitor_forms(soup):
        form_tags = soup.find_all('form')
        for form_tag in form_tags:
            form_id = form_tag.get('id', '')
            form_class = form_tag.get('class', '')
            print(f"Найдена форма: ID={form_id}, Классы={form_class}")

            # Мониторим данные, вводимые в форму в реальном времени
            form_tag.insert(0, BeautifulSoup("<input type='text' id='form_input' placeholder='Введите данные'>", 'html.parser'))
            print("Мониторим данные, вводимые в эту форму в реальном времени:")
            while True:
                form_input = form_tag.find('input', {'id': 'form_input'})
                user_input = input()  # Получаем данные, вводимые пользователем
                form_input['value'] = user_input  # Заполняем форму в реальном времени
                print(f"Введено в форму: {user_input}")

    monitor_forms(soup)

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
        if os.path.exists(image_folder):
            for file in os.listdir(image_folder):
                file_path = os.path.join(image_folder, file)
                os.remove(file_path)
            os.rmdir(image_folder)

        os.system("rm -fr index.html")
        os.system("rm -fr downloaded_page.html")
        print("Скрипт завершен. Все скачанные файлы удалены.")
else:
    print("Пустой URL. Пожалуйста, введите действительный URL.")
