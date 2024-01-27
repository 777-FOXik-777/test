import time
import os
import subprocess
from bs4 import BeautifulSoup

# Шаг 1: Скачивание страницы

# Введите URL
url = input('\nВыбери URL ➤ ')

# Используем wget для загрузки HTML-кода страницы
subprocess.run(['wget', '--recursive', '--convert-links', '--page-requisites', '--no-parent', '-nc', url])

# Ждем некоторое время перед обработкой HTML-кода
time.sleep(5)

# Преобразуем относительные ссылки в абсолютные
soup = BeautifulSoup(open("index.html"), 'html.parser')
base_url = url

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

# Добавляем JavaScript-скрипт для обработки асинхронной загрузки изображений
script = """
<script>
    setTimeout(function() {
        var lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(function(img) {
            if (img.hasAttribute('data-src')) {
                img.setAttribute('src', img.getAttribute('data-src'));
            }
        });
    }, 5000);
</script>
"""

# Вставляем скрипт в конец тега <head>
head_tag = soup.head
if head_tag:
    head_tag.append(BeautifulSoup(script, 'html.parser'))
else:
    # Если нет тега <head>, добавляем его в начало документа
    soup.insert(0, BeautifulSoup('<head></head>', 'html.parser'))
    soup.head.append(BeautifulSoup(script, 'html.parser'))

# Сохраняем обновленный HTML-код в файл
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

# Шаг 2: Запуск локального сервера

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
serveo_command = f'ssh -R 80:localhost:{tru_201} serveo.net -T -n'
serveo_process = subprocess.Popen(serveo_command, shell=True, stdout=subprocess.PIPE)

# Получаем public URL из вывода процесса Serveo
serveo_url = serveo_process.stdout.readline().strip().decode('utf-8').split()[-1]

print(f"Приложение доступно по следующему public URL: {serveo_url}")

# Проверяем, есть ли изображения на странице, и скачиваем их
image_dir = os.path.join(os.getcwd(), 'images')
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

image_tags = soup.find_all('img', {'src': True})
for idx, image_tag in enumerate(image_tags):
    image_url = image_tag['src']
    image_filename = os.path.join(image_dir, f'image_{idx+1}.png')
    subprocess.run(['wget', '--no-clobber', '--quiet', '-P', image_dir, image_url])

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процессы локального сервера и Serveo
    local_server_process.terminate()
    serveo_process.terminate()

    print("Скрипт завершен.")
