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
    window.onload = function() {
        var lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(function(img) {
            if (img.hasAttribute('data-src')) {
                img.setAttribute('src', img.getAttribute('data-src'));
            }
        });
    };
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

# Сохраняем HTML-код в файл
file_path = 'downloaded_page.html'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

print(f"Страница успешно скачана и сохранена в файл {file_path}")

# Остальной код остается без изменений
