import requests
import subprocess

# Замените 'http://example.com' на нужную вам ссылку
url = 'https://www.olx.ua/uk'

# Скачиваем страницу по ссылке
response = requests.get(url)
html_content = response.text

# Сохраняем HTML-код в файл
with open('downloaded_page.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

# Замените 'your-serveo-subdomain' на ваш собственный поддомен на serveo.net
serveo_subdomain = 'your-serveo-subdomain'

# Выполняем команду для проброса порта
command = f'ssh -R 80:localhost:8080 {serveo_subdomain}.serveo.net -T -n 2>&1 | awk \'/serveo.net/ {{print $5}}\''

# Запускаем команду с помощью subprocess
subprocess.run(command, shell=True)
