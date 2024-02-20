import requests
import subprocess
import time
import os
import random
import string
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Генерация случайной строки для заполнения полей ввода
def random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

try:
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

        # Находим все формы на странице
        forms = soup.find_all('form')

        # Перебираем формы
        for form in forms:
            # Находим все поля ввода в форме
            input_fields = form.find_all('input')
            # Создаем словарь для хранения данных формы
            form_data = {}
            # Заполняем поля ввода случайными данными
            for input_field in input_fields:
                if input_field.get('name'):  # Проверяем наличие атрибута 'name'
                    field_name = input_field['name']
                    field_value = random_string()
                    form_data[field_name] = field_value

            # Отправляем данные формы
            response = requests.post(form['action'], data=form_data)
            
            # Выводим результаты
            print(f"Результаты отправки данных формы на URL {form['action']}:")
            print(response.text)

        # Запуск локального сервера
        local_server_command = 'python -m http.server 8000'
        local_server_process = subprocess.Popen(local_server_command, shell=True, stdout=subprocess.PIPE)
        print("Локальный сервер запущен на порту 8000")

        # Запуск Serveo.net
        tru_201 = '8000'  # Замените на нужный вам порт
        serveo_command = f"ssh -q -R 80:localhost:{tru_201} serveo.net -T"
        serveo_process = subprocess.Popen(serveo_command, shell=True, stdout=subprocess.PIPE)

        # Получение public URL из вывода процесса Serveo
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

except Exception as e:
    print(f"Произошла ошибка: {str(e)}")
