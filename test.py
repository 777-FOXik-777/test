import requests
import subprocess
import time
import re

# Шаг 1: Скачивание страницы

# Замените 'http://example.com' на нужную вам ссылку
url = 'https://www.olx.ua/uk'

# Скачиваем страницу по ссылке
response = requests.get(url)
html_content = response.text

# Сохраняем HTML-код в файл
with open('downloaded_page.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("Страница успешно скачана и сохранена в файл downloaded_page.html")

# Шаг 2: Запуск на Serveo.net

# Замените 'your-serveo-subdomain' на ваш собственный поддомен на serveo.net
serveo_subdomain = 'your-serveo-subdomain'

# Выполняем команду для проброса порта на serveo.net
serveo_command = f'ssh -R 80:localhost:8080 {serveo_subdomain}.serveo.net -T -n'

# Запускаем команду для Serveo.net с помощью subprocess
serveo_process = subprocess.Popen(serveo_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Ждем, пока команда не завершится
serveo_output, serveo_error = serveo_process.communicate()

# Печатаем вывод и ошибки (если есть)
print("Вывод команды Serveo:", serveo_output.decode('utf-8'))
print("Ошибка команды Serveo:", serveo_error.decode('utf-8'))

# Пытаемся извлечь URL Serveo из вывода
serveo_match = re.search(r'https://\S+', serveo_output.decode('utf-8'))
if serveo_match:
    serveo_url = serveo_match.group()
    print(f"Ваша страница теперь доступна по ссылке Serveo: {serveo_url}")
else:
    print("Не удалось извлечь URL Serveo. Возможно, что-то пошло не так.")
    serveo_process.terminate()

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C
    print("Скрипт завершен.")
