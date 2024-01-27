import time
import subprocess
import os
import requests

# Шаг 1: Скачивание страницы

# Введите URL
url = input('\nВыбери URL ➤ ')

# Используем requests для загрузки HTML-кода страницы
response = requests.get(url)
html_content = response.text

# Определяем переменную downloaded_folder
downloaded_folder = os.path.abspath('index.html')

# Сохраняем HTML-код в файл
with open(downloaded_folder, 'w', encoding='utf-8') as file:
    file.write(html_content)

# Ждем некоторое время перед обработкой HTML-кода
time.sleep(5)

# Шаг 2: Запуск Serveo.net для тунелирования файла

# Используем оригинальную команду Serveo.net без изменений
tru_port = '8081'  # Замените на нужный вам порт
file_to_tunnel = 'index.html'  # Замените на нужный вам файл

serveo_command = f'ssh -R 80:localhost:{tru_port} serveo.net -T -n {downloaded_folder}/{file_to_tunnel}'
serveo_process = subprocess.Popen(serveo_command, shell=True, stdout=subprocess.PIPE)

# Получаем public URL из вывода процесса Serveo
serveo_url = serveo_process.stdout.readline().strip().decode('utf-8').split()[-1]

print(f"Файл {file_to_tunnel} доступен по следующему public URL: {serveo_url}")

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процесс Serveo
    serveo_process.terminate()

    print("Скрипт завершен.")
