import requests
import subprocess

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
serveo_process = subprocess.Popen(serveo_command, shell=True, stdout=subprocess.PIPE)

# Получаем вывод команды (URL Serveo)
serveo_output = serveo_process.stdout.read().decode('utf-8').strip()

# Печатаем URL Serveo
print(f"Ваша страница теперь доступна по ссылке Serveo: {serveo_output}")

# Шаг 3: Запуск на локальном сервере

# Если ваш локальный сервер уже запущен на порту 8080, его можно открыть в браузере напрямую:
local_url = 'http://localhost:8080'
print(f"Ваш локальный сервер доступен по ссылке: {local_url}")

# Ждем, пока пользователь не закроет программу (или можно добавить какую-то логику завершения программы)
input("Нажмите Enter для завершения программы...")
